'''
Polling places

Thomas Wilson, Tyson Miller

Main file for polling place simulation
'''
import sys
import random
import queue
import click
import util

### YOUR Voter, VoterGenerator, and Precinct classes GO HERE.

class Voter(object):
    def __init__(self, arrival_time, voting_duration, voter_id):
        self.arrival_time = arrival_time
        self.departure_time = None
        self.voting_duration = voting_duration
        self.start_time = None
        self.voter_id = voter_id
        
    def get_start_time(self):
        '''
        returns a voter's start time
        '''
        return self.start_time

    def get_departure_time(self):
        '''
        returns a voter's departure time
        '''
        self.departure_time = self.arrival_time - self.voting_duration
        return self.departure_time

    def start_voting(self, time):
        '''
        assign a voter a start and departure time
        '''
        self.start_time = time
        self.departure_time = self.start_time + self.voting_duration

class VoterGenerator(object):
    def __init__(self, arrival_rate, voting_duration_rate):
        self.time = 0
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate
        self.num_voters = 0

    def activate(self):
        '''
        Generates a voter object
        '''
        gap, duration = util.gen_poisson_voter_parameters(self.arrival_rate, \
            self.voting_duration_rate)
        self.time += gap
        v = Voter(self.time, duration, self.num_voters)
        self.num_voters += 1
        return v

def test_0(precinct):
    '''
    This functions tests whethers you are properly generating voter objects
    '''
    random.seed(1468604453)
    precinct = util.load_precincts(precinct)
    generator = VoterGenerator(precinct[0][0]['voter_distribution']\
        ['arrival_rate'], precinct[0][0]['voter_distribution']\
        ['voting_duration_rate'])
    lst = []
    for i in range(precinct[0][0]['num_voters']):
        lst.append(generator.activate())
    for voter in lst:
        print([voter.arrival_time, voter.voting_duration, voter.start_time, \
            voter.departure_time, voter.voter_id])

class Precinct(object):
    def __init__(self, i):
        self.name = i['name']
        self.hours_open = i['hours_open']
        self.num_booths = i['num_booths']
        self.num_voters = i['num_voters']
        self.arrival_rate = i['voter_distribution']['arrival_rate']
        self.voting_duration_rate = i['voter_distribution']\
        ['voting_duration_rate']
        self.gen = VoterGenerator(self.arrival_rate,\
         self.voting_duration_rate)
        self.time = 0
        self.voters = VoterGenerator(self.arrival_rate, \
            self.voting_duration_rate)
        self.queue = queue.PriorityQueue(maxsize=self.num_booths)

    def run(self):
        '''
        simulates election day. Returns a list of voters
        '''
        voter = None
        last_voter = None
        lst = []
        j = 0
        while(j < self.num_voters):
            if voter == None:
                voter = self.gen.activate()

            full = self.queue.full()
            if not self.queue.empty():
                (last_time, last_voter) = self.queue.get(block=False)

            if (last_voter != None) and (last_voter.departure_time < \
                voter.arrival_time or full):
                self.time = last_voter.departure_time
                voter.start_voting(self.time)
                last_voter = None
                last_time = None

            elif (voter.arrival_time) <= self.hours_open * 60:
                if self.time < voter.arrival_time:
                    self.time = voter.arrival_time
                voter.start_voting(self.time)
                self.queue.put((voter.departure_time, voter), block=False)
                lst.append(voter)
                voter = None
                j+= 1
                if (last_voter != None):
                    self.queue.put((last_voter.departure_time, last_voter), \
                        block=False)
            else:
                break

        while not self.queue.empty():
            some_time, voter = self.queue.get(block=False)
            time = voter.departure_time
        return lst

def simulate_election_day(precincts, seed=0):
    # YOUR CODE HERE.
    d = {}
    for i in precincts:
        random.seed(seed)
        p = Precinct(i)
        d[p.name] = p.run()
    return d


def find_avg_wait_time(precinct, num_booths, ntrials, initial_seed=0):
    '''
    find the average wait time of voters for a precinct
        imput: precinct and number of trials
        output:float
    '''
    # YOUR CODE HERE.
    seed = initial_seed
    precinct['num_booths'] = num_booths
    wait_times = []
    for i in range(ntrials):
        random.seed(seed)
        total_wait = 0
        iprecinct = Precinct(precinct)
        voters = iprecinct.run()
        for j in voters:
            total_wait += (j.start_time - j.arrival_time)
        wait_times.append(total_wait / iprecinct.num_voters)
        seed += 1

    # REPLACE 0.0 with the waiting time this function computes
    wait_times.sort()
    return wait_times[ntrials//2]


def find_number_of_booths(precinct, target_wait_time, max_num_booths, ntrials,\
 seed=0):
    # YOUR CODE HERE
    # Replace (0,0) with a tuple containing the optimal number of booths
    # and the average waiting time for that number of booths
    booths = 1
    wait_time = find_avg_wait_time(precinct, booths, ntrials, seed)
    while (wait_time > target_wait_time ):
        booths += 1
        wait_time = find_avg_wait_time(precinct, booths, ntrials, seed)
        if (booths > max_num_booths):
            return (0, None)

    return (booths, wait_time)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals

@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--max-num-booths', type=int)
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, max_num_booths, target_wait_time, print_voters):
    '''
    Run the command.
    '''

    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = simulate_election_day(precincts, seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    return -1
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        if max_num_booths is None:
            max_num_booths = precinct["num_voters"]

        nb, avg_wt = find_number_of_booths(precinct, target_wait_time, max_num_booths, 20, seed)

        if nb is 0:
            msg = "The target wait time ({:.2f}) is infeasible"
            msg += " in precint '{}' with {} or fewer booths"
            print(msg.format(target_wait_time, precinct["name"], max_num_booths))
        else:
            msg = "Precinct '{}' can achieve average waiting time"
            msg += " of {:.2f} with {} booths"
            print(msg.format(precinct["name"], avg_wt, nb))
    return 0


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter
