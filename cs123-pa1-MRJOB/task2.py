from mrjob.job import MRJob

class Task_Two(MRJob):
    def mapper(self, _, line):
        row = line.split(',')
        v_namelast = str(row[19]).strip().lower()
        v_namefirst = str(row[20]).strip().lower()
        v_namefull = ' '.join([v_namefirst, v_namelast]).lower().strip()
        if v_namefull != '':
            yield v_namefull, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer_init(self):
        self.top_ten = [(0,0) for x in range(10)]

    def reducer(self, key, values):
        total_visits = sum(values)
        top_ten = self.top_ten
        if total_visits:
            if total_visits > top_ten[0][1]:
                top_ten[0] = (key, total_visits)
                top_ten.sort(key=lambda x: x[1])
                self.top_ten = top_ten

    def reducer_final(self):
        yield "Name, Count:", self.top_ten


if __name__ == '__main__':
    Task_Two.run()
