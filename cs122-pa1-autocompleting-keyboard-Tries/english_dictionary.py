# CS122: Auto-completing keyboard using Tries
# Distribution
#
# Matthew Wachs
# Autumn 2014
#
# Revised: August 2015, AM
#   December 2017, AMR
#
# Thomas Wilson

import os
import sys
from sys import exit
import autocorrect_shell


class EnglishDictionary(object):
    def __init__(self, wordfile):
        '''
        Constructor

        Inputs:
          wordfile (string): name of the file with the words.
        '''
        self.words = TrieNode()

        with open(wordfile) as f:
            for w in f:
                w = w.strip()
                if w != "" and not self.is_word(w):
                    self.words.add_word(w)


    def is_word(self, w):
        '''
        Is the string a word?

        Inputs:
           w (string): the word to check

        Returns: boolean
        '''
        # ADD YOUR CODE HERE AND REPLACE THE False
        # IN THE RETURN WITH A SUITABLE RETURN VALUE.
        a = self.words.find_node(w)
        if a:
            return a.word_finished
        return False


    def num_completions(self, prefix):
        '''
        How many words in the dictionary start with the specified
        prefix?

        Inputs:
          prefix (string): the prefix

        Returns: int
        '''
        # IMPORTANT: When you replace this version with the trie-based
        # version, do NOT compute the number of completions simply as
        #
        #    len(self.get_completions(prefix))
        #
        # See PA writeup for more details.

        # ADD YOUR CODE HERE AND REPLACE THE ZERO IN THE RETURN WITH A
        # SUITABLE RETURN VALUE.
        a = self.words.find_node(prefix)
        if a:
            return a.count
        return 0
        

    def get_completions(self, prefix):
        '''
        Get the suffixes in the dictionary of words that start with the
        specified prefix.

        Inputs:
          prefix (string): the prefix

        Returns: list of strings.
        '''

        # ADD YOUR CODE HERE AND REPLACE THE EMPTY LIST
        # IN THE RETURN WITH A SUITABLE RETURN VALUE.
        
        a = self.get_all_words(prefix)
        a[:] = [x[len(prefix):] for x in a]
        return a

    def get_all_words(self, prefix):
        '''
        creates a list of all words that start with prefix

        inputs:
            prefix (string): we will find all words that start with this

        returns:
            a (list): list of all words that start with prefix
        '''
        prefix_node = self.words.find_node(prefix)
        a = list()
        if not prefix_node:
            return []
        if prefix_node.word_finished:
            a.append(prefix)
        for child_key in prefix_node.children.keys():
            a += self.get_all_words(prefix + prefix_node.children[child_key].char)
        return a


class TrieNode(object):
    def __init__(self):
        ### REPLACE pass with appropriate documentation and code
        self.char = ''
        self.count = 0
        self.word_finished = False
        self.children = {}

    def add_word(self, word):
        '''
        Add's a word to the trie

        inputs:
          word: a string

        Returns:
           the word added to the Trie
        '''
        ### REPLACE pass with appropriate documentation and code
        point = self
        point.count += 1
        for char in word:
            in_tree = False
            for letter, child in point.children.items():
                if letter == char:
                    child.count += 1
                    point = child
                    in_tree = True
                    break

            if not in_tree:
                node = TrieNode()
                node.count += 1
                node.char = char
                point.children[char] = node
                point = node
        point.word_finished = True


    ### ADD ANY EXTRA METHODS HERE.
    def find_node(self, string):
        '''
        Brings you to the TrieNode that corresponds to the last letter in the string
        
        inputs:
            string (string): the string that corresponds to the node that you want to find

        returns:
            node: node that corresponds to the last letter in string
        '''
        if string == '':
            return self
        if string[0] not in self.children:
            return None
        if len(string) == 1:
            return self.children[string]
        if len(string) > 1:
            return self.children[string[0]].find_node(string[1:])



if __name__ == "__main__":
    autocorrect_shell.go("english_dictionary")
