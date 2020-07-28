from mrjob.job import MRJob
import heapq
from bintrees import AVLTree
import datetime
import random

def line_intersection(l1, l2):
    a1 = l1[1][1] - l1[0][1]
    b1 = l1[0][0] - l1[1][0]
    c1 = a1 * l1[0][0] + b1 * l1[0][1]
    a2 = l2[1][1] - l2[0][1]
    b2 = l2[0][0] - l2[1][0]
    c2 = a2 * l2[0][0] + b2 * l2[0][1]
    det = a1*b2 - a2*b1
    max_x = min(l1[1][0], l2[1][0])
    min_x = max(l1[0][0], l2[0][0])
    if det == 0:
        return False
    else:
        x, y = (b2*c1 - b1*c2)/det, (a1*c2 - a2*c1)/det
        if min_x <= x <= max_x:
            return x, y
        else:
            return False

class Task_One(MRJob):
	def mapper(self, _, line):
		row = line.split(',')
		time_start = row[1]
		date = time_start[:10]
		time = time_start[11:]
		if row[0] != "":
			day = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%A')
			pickup_x = float(row[2]) + random.uniform(-.001, .003)
			pickup_y = float(row[3]) + random.uniform(-.001, .003)
			dropoff_x = float(row[4]) + random.uniform(-.001, .003)
			dropoff_y = float(row[5]) + random.uniform(-.001, .003)
			if pickup_x < dropoff_x:
				yield [day, time], ((pickup_x, pickup_y), (dropoff_x, dropoff_y))
			else:
				yield [day, time], ((dropoff_x, dropoff_y), (pickup_x, pickup_y))


	def combiner(self, key, values):
		heap = []
		for val in values:
			heapq.heappush(heap, (val[0][0], True, val))
			heapq.heappush(heap, (val[1][0], False, val))
		yield key, heap
	def reducer(self, key, values):
		tree = AVLTree()
		points = set()
		for items in values:
			for val in items:
				y = val[2][0][1]

				if val[1]:
					tree.insert(y, val[2])
					try:
						i = line_intersection(val[2], tree.succ_item(y)[1])
						if i:
							points.add(i)
					except KeyError:
						pass
					try:
						i = line_intersection(val[2], tree.prev_item(y)[1])
						if i:
							points.add(i)
					except KeyError:
						pass
				else:
					try:
						i = line_intersection(tree.prev_item(y)[1], tree.succ_item(y)[1])
						if i:
							points.add(i)
					except KeyError:
						pass
					try:
						tree.remove(y)
					except KeyError:
						pass
		yield key, list(points)

if __name__ == '__main__':
	Task_One.run()
