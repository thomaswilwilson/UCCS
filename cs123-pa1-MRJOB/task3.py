from mrjob.job import MRJob

class Task_Three(MRJob):
    def mapper(self, _, line):
        row = line.split(',')
        NAME_LAST = str(row[0]).strip()
        NAME_FIRST = str(row[1]).strip()
        NAME_FULL = ' '.join([NAME_FIRST, NAME_LAST]).lower()
        year = row[27][5:].strip('/')
        yield NAME_FULL, year

    def combiner(self, key, values):
        value_set = set(values)
        for value in value_set:
            yield key, value

    def reducer(self, key, values):
        years = set(values)
        if ('2009' in years) and ('2010' in years):
            yield key, "Has visited in 2009 and 2010"

if __name__ == '__main__':
    Task_Three.run()
