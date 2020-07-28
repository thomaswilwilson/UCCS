from mrjob.job import MRJob

class Task_One(MRJob):
    def mapper(self, _, line):
        row = line.split(',')
        NAME_LAST = str(row[0]).strip()
        NAME_FIRST = str(row[1]).strip()
        NAME_FULL = ' '.join([NAME_FIRST, NAME_LAST]).lower()
        yield NAME_FULL, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        total_visits = sum(values)
        if total_visits >= 10:
           yield key, total_visits

if __name__ == '__main__':
    Task_One.run()
