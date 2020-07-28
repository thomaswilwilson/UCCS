from mrjob.job import MRJob
import heapq
from bintrees import AVLTree
import datetime
import random
from shapely.geometry import Point
from shapely.wkt import loads
import pandas as pd
'''
MapReduce function used to cluster the data points with similar start times and
yield all intersection points for each date and time.
'''
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
def get_point(data):
	poly = loads(data)
	min_x, min_y, max_x, max_y = poly.bounds
	while True:
		pt = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))
		if poly.contains(pt):
			return pt.x, pt.y

class Task_One(MRJob):
	def mapper(self, _, line):
		row = line.split(',')
		time_start = row[0]
		date = time_start[:10]
		time = time_start[11:]
		if row[0] != "Trip Start Timestamp":
		# if row[0] != "Trip Start":
			day = datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%A')
			pickup = float(row[1])
			dropoff = float(row[2])
			yield [day, time], (int(pickup), int(dropoff))


	def combiner(self, key, values):
		heap = []
		df = pd.read_csv('geo.csv', index_col = 'GEOID10')
		for val in values:
			try:
				seg = (get_point(df.at[val[0], 'the_geom']),
				get_point(df.at[val[1], 'the_geom']))
				if seg[0][0] > seg[1][0]:
					seg = (seg[1], seg[0])
				heapq.heappush(heap, (seg[0][0], True, seg))
				heapq.heappush(heap, (seg[1][0], False, seg))
			except KeyError:
				pass
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
