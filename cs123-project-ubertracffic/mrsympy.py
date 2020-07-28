from mrjob.job import MRJob
import pandas as pd
from sympy import Point
from sympy.geometry import Segment, intersection

## Using MapReduce to generate intersection points of the large data set

class Task_One(MRJob):
    def mapper(self, _, line):
        row = line.split(',')
        time_start = row[1]
        date = time_start[:10]
        time = time_start[11:]
        if row[0] != "Trip ID":
            pickup_x = float(row[15])
            pickup_y = float(row[16])
            dropoff_x = float(row[18])
            dropoff_y = float(row[19])
            yield [date, time], ((pickup_x, pickup_y), (dropoff_x, dropoff_y))




    def reducer(self, key, values):
        lines = []
        for value in values:
            lines.append(Segment(Point(value[0], evaluate=False), Point(value[1], evaluate=False)))

        for i in range(len(lines)):
            for j in range(len(lines)):
                if j > i:
                    heat = lines[i].intersection(lines[j])
                    if len(heat) >0:
                        if isinstance(heat[0], Point):
                            yield str(heat[0].x), str(heat[0].y)


if __name__ == '__main__':
    Task_One.run()
