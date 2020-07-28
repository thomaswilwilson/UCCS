from mrjob.job import MRJob

class Task_Four(MRJob):
    def mapper(self, _, line):
        row = line.split(',')
        NAME_LAST = str(row[0]).strip()
        NAME_FIRST = str(row[1]).strip()
        NAME_FULL = ' '.join([NAME_FIRST, NAME_LAST]).lower()
        v_namelast = str(row[19]).strip().lower()
        v_namefirst = str(row[20]).strip().lower()
        v_namefull = ' '.join([v_namefirst, v_namelast]).lower()
        yield NAME_FULL, "visitor"
        yield v_namefull, "visitee"

    def combiner(self, key, values):
        value_set = set(values)
        for value in value_set:
            yield key, value

    def reducer(self, key, values):
        years = set(values)
        if ('visitee' in years) and ('visitor' in years):
            yield key, "Is a visitee and a visitor"

if __name__ == '__main__':
    Task_Four.run()
