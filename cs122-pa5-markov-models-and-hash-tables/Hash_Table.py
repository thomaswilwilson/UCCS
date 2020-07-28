# CS122 W'19: Markov models and hash tables
# Thomas Wilson


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self,cells,defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        ### YOUR CODE HERE ###
        self.cells = cells
        self.defval = defval
        self.length = 0
        self.table = [None] * cells

    def lookup(self,key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        ### YOUR CODE HERE ###
        hashed_key = hash(key) % self.cells

        for slot in self.table[hashed_key:]:

            if slot == None:
                return self.defval

            elif slot[0] == key:
                return slot[1]

        for slot in self.table[:hashed_key]:

            if slot == None:
                return self.defval

            elif slot[0] ==key:
                return slot[1]

        return self.defval


    def update(self,key,val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        ### YOUR CODE HERE ###
        hashed_key = hash(key) % self.cells
        for i, slot in enumerate(self.table[hashed_key:], start = hashed_key):

            if slot == None or slot[0] == key:
                self.table[i] = (key, val)

                if slot == None:
                    self.length += 1
                    self.rehash()
                    
                return


        for j, slot in enumerate(self.table[:hashed_key]):

            if slot == None or slot[0] == key:
                self.table[j] = (key, val)

                if slot == None:
                    self.length += 1
                    self.rehash()

                return

    def rehash(self):
        if (self.length / self.cells < TOO_FULL):
            return

        self.cells = self.cells * GROWTH_RATIO
        self.length = 0
        old_table = self.table
        self.table = [None] * self.cells
        for tuple in old_table:

            if tuple != None:
                self.update(tuple[0],tuple[1])


