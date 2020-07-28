'''
Epidemic modeling

Thomas Wilson

Functions for running epidemiological simulation
'''

import random
import os.path
import sys

import util

# A few constants to simplify debugging
TEST_SEED = 20170217
INFECTION_RATE_LIST = [0, 0.25, 0.5, 0.75, 1.0]



def count_infected(city):
    '''
    Purpose: Count the number of infected people

    Inputs:
        city (list): the state of all people in the simulation
            at the start of the day

    Returns (int): number of infected people in the city
    '''

    # YOUR CODE HERE
    num_infected = 0
    for i in city:
        if i == "I0" or i == "I1":
            num_infected += 1
    # REPLACE 0 WITH THE APPROPRIATE RETURN VALUE
    return num_infected


def has_an_infected_neighbor(city, position):
    '''
    Purpose: determine whether a person has an infected neighbor

    Inputs:
        city (list): the state of all people in the simulation
            at the start of the day
        position (int): the position of the person to check
    Returns:
        True, if the person has an infected neighbor, False otherwise.
    '''

    # YOUR CODE HERE
    if position == 0:
        if (city[len(city) - 1] == "I0" or city[len(city) - 1] == "I1") or \
         (city[position + 1] == "I0" or city[position + 1] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    elif position == (len(city) - 1):
        if (city[position - 1] == "I0" or city[position - 1] == "I1") or \
         (city[0] == "I0" or city[0] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    else:
        if (city[position - 1] == "I0" or city[position - 1] == "I1") or \
         (city[position + 1] == "I0" or city[position + 1] == "I1"):
            neighbor_infected = True
        else:
            neighbor_infected = False

    return neighbor_infected

    # REPLACE False WITH THE APPROPRIATE RETURN VALUE
    return neighbor_infected


def gets_infected_at_position(city, position, infection_rate):
    '''
    Purpose: Determine whether the person at position gets infected.

    Inputs:
        city (list): the state of all people in the simulation
            at the start of the day
        position (int): the position of the person to check
        infection_rate (float): the chance of getting infected if one of your
            neighbors is infected

    Returns:
         True, if the person should be infected, False otherwise.
    '''

    # YOUR CODE HERE
    if has_an_infected_neighbor(city, position) == True:
            
            immunity_level = random.random()
            if immunity_level >= infection_rate:
                infected = False
            else:
                infected = True
    else:
        infected = False
    # REPLACE False WITH THE APPROPRIATE RETURN VALUE
    return infected


def simulate_one_day(city, infection_rate):
    '''
    Purpose: to move the simulation forward a single day.

    Inputs:
        city (list of strings): the starting state of the
            simulation, i.e., what disease state each person is. A
            starting state of ['S', 'I', 'R'] means that person 0
            starts the day susceptible to disease, person 1 starts the
            day infected by the disease, and person 2 has starts the
            day protected from disease

        t (int): the duration of the infected state (i.e., how many
            days it will take someone in state 'I' to turn into state
            'R')

        infection_rate (float): the chance of getting infected if one of your
            neighbors is infected

    Returns:
        tuple (new_city, new_timing) of
          new_city (list): disease state of the city after one day
          new_timing (list): timings for the city after one day
    '''

    # YOUR CODE HERE
    old  = city[:]
    for i in range(len(city)):
        if old[i] == "I1":
            city[i] = "I0"

        elif old[i] == "I0":
            city[i] = "R"

        elif old[i] == "R":
            city[i] = "R"

        else:
            if (gets_infected_at_position(old, i, infection_rate)) == True:
                city[i] = "I1"

    # REPLACE [] WITH THE APPROPRIATE RETURN VALUE
    return city


def run_simulation(starting_state, random_seed, max_num_days, infection_rate):
    '''
    Purpose: to run the entire simulation.

    Inputs:
        starting_state (list of strings): the starting states of all
            members of the simulation
        random_seed (int): the random seed to use for the simulation
        d (int): the maximum days of the simulation
        infection_rate (float): the chance of getting infected if one of your
            neighbors is infected

    Returns:
        tuple (city, d) of
            city (list): the final state of the simulation
            d (int): days of the simulation
    '''

    assert max_num_days >= 0
    
    if count_infected(starting_state) == 0:
        return starting_state, 1
    random.seed(random_seed)
    d = 0
    city = starting_state[:]
    for i in range(max_num_days):

        if count_infected(city) != 0:
            city = simulate_one_day(city, infection_rate)
            d += 1
            random_seed += 1
        else:
            return city, d

    return city, d


def compute_average_num_infected(
        starting_state, random_seed, max_num_days, infection_rate,
        num_trials):
    '''
    Purpose: to conduct N trials with one infection probability and calculate
        how many people on average get infected over time

    Inputs:
        starting_state (list of strings): the starting states of all
            members of the simulation
        random_seed (int): the random seed to set the simulation to for
            every single time the simulation runs. This is what the FIRST s
            simulation will use, and then will be incremented every time the
            simulation runs
        max_num_days (int): the maximum days of the simulation
        infection_rate (float): the chance of getting infected if one of your
            neighbors is infected
        num_trials (int): the number of trials to run

    Returns:
        (int): the average number of people infected over time
    '''

    assert num_trials > 0

    num_infected = 0

    for i in range(num_trials):
        city, d = run_simulation(starting_state, random_seed, max_num_days,
        infection_rate)
        for i in city:
            if i == "I0" or i == "I1" or i == "R":
                num_infected += 1
        random_seed += 1
    return num_infected / num_trials


def infection_rate_param_sweep(
        starting_state, random_seed, d, infection_rate_list, num_trials):
    '''
    Purpose: run trials where the starting state and random_seed are
        constant, but the infection rate is changing

    Inputs:
        starting_state (list of strings): the starting states of all
            members of the simulation
        random_seed (int): the random seed to set the simulation to for
            every single time the simulation runs. This is what the FIRST s
            simulation will use, and then will be incremented every time the
            simulation runs
        max_num_days (int): the maximum days of the simulation
        num_trials (int): the number of trials to run
        infection_rate_list (list of floats): a list of the chance of getting
            infected if one of your neighbors is infected per trial

    Returns:
        infected_number_list (list of ints): the number of people infected
            indexed by trial
    '''

    # YOUR CODE HERE

    infected_number_list = []
    for i in range(len(infection_rate_list)):
        num = compute_average_num_infected(starting_state, random_seed,
            d, infection_rate_list[i], num_trials)
        infected_number_list.append(num)
    return infected_number_list


################ Do not change the code below this line #####################


def run():
    '''
    Process the command-line arguments and do the work.
    '''
    usage = ("usage: python simulation.py <data_filename>")

    if len(sys.argv) != 2:
        print(usage)
        return

    input_filename = sys.argv[1]
    if not os.path.isfile(input_filename):
        print(usage)
        print("error: file not found: {}".format(input_filename))
        return

    # check that state number is valid -- no key error
    try:
        starting_state, random_seed, max_num_days, \
            infection_rate, num_trials = util.get_config(input_filename)
    except KeyError:
        print(usage)
        return

    print("Running initial simulation...")
    (final_state, sim_days) = run_simulation(
        starting_state, random_seed, max_num_days, infection_rate)
    print("The starting state of the simulation was {}.".format(
        starting_state))
    print("The final state of the simulation is {}.". format(
        final_state))
    print("The simulation ended after day {}.".format(sim_days))

    print("Running multiple trials...")
    avg_infected = compute_average_num_infected(
        starting_state, random_seed, max_num_days, infection_rate, num_trials)
    print("Over {} trial(s), on average, {:3.1f} people were infected".format(
        num_trials, avg_infected))

    print("Varying infection parameter...")
    infected_list = infection_rate_param_sweep(
        starting_state, random_seed, max_num_days,
        INFECTION_RATE_LIST, num_trials)
    printstr = "Rate | Infected"
    for rate, infected_number in zip(INFECTION_RATE_LIST, infected_list):
        printstr += "\n{:4.1f} | {:2.2f}".format(rate, infected_number)
    print(printstr)

if __name__ == "__main__":
    run()
