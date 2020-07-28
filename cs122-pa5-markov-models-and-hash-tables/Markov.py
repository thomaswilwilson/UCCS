# CS122 W'19: Markov models and hash tables
# Thomas Wilson

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        ### YOUR CODE HERE ###
        self.k = k
        self.s = s
        self.table = Hash_Table.Hash_Table(HASH_CELLS, 'key error')
        self.unique_chars = len(''.join(set(s)))
        self.populate_model()


    def kth_markov(self, k):
        '''
        Generates a kth order Markov Model. Fills hash table with each subset
         of the string along with a value pair that represents the count.

        inputs:
            k (int): "order" for markov model

        outputs:
            None
        '''
        for count, letter in enumerate(self.s):
            index = count - k
            if index < 0:
                string = self.s[index:] + self.s[0:count]
            else:
                string = self.s[index:count]

            val =  self.table.lookup(string)
            if type(val) == str:
                self.table.update(string, 1)
            else:
                self.table.update(string, val + 1)


    def populate_model(self):
        '''
        populates the hash table with a kth order markov model as well as a kth
        1 order markov model
        '''
        self.kth_markov(self.k)
        self.kth_markov(self.k+1)


    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        ### YOUR CODE HERE ###
        log_probs = []
        for count, letter in enumerate(s):

            index = count - self.k
            jindex = count - self.k + 1

            if index < 0:
                n_str = s[index:] + s[0:count]

            else:
                n_str = s[index:count]

            m_str = n_str + letter
            n = self.table.lookup(n_str)
            m = self.table.lookup(m_str)

            if n == self.table.defval:
                n = 0

            if m == self.table.defval:
                m = 0

            log_probs.append(math.log((m+1)/(n + self.unique_chars)))

        return sum(log_probs)




def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    ### YOUR CODE HERE ###
    Speech1_Markov = Markov(order, speech1)
    Speech2_Markov = Markov(order, speech2)
    prob_1 = Speech1_Markov.log_probability(speech3) / len(speech3)
    prob_2 = Speech2_Markov.log_probability(speech3) / len(speech3)

    if prob_1 > prob_2:
        conclusion = 'A'
    else:
        conclusion = 'B'

    return (prob_1, prob_2, conclusion)


def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)

