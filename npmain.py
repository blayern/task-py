#!/usr/bin/python3
import sys
import re
from shapely.geometry import Point, Polygon

with open(sys.argv[1], 'r') as fp:
	data = fp.readlines()
	line_count = len(data)

points_list = [[] for i in range(0, line_count)]
point_pattern = re.compile('([0-9]+):([0-9]+)')

for i, lne in enumerate(data):
	line_points = re.findall(point_pattern, data[i])
	for point in line_points:
		points_list[i].append([float(idx) for idx in point])

def batch(iterable, count=1):
	iterable_len = len(iterable)
	for idx in range(0, iterable_len, count):
		yield iterable[idx:min(idx+count, iterable_len)]

def find_triangle(line):
	for sh in batch(line, 3):
		if len(sh)<3:
			return
		shape = Polygon(sh)
		if shape.is_valid:
			print('is triangle')
		else:
			print('not triangle')

def find_square(line):
	for sh in batch(line, 4):
		if len(sh)<4:
			return
		shape = Polygon(sh)
		if shape.is_valid and Point(sh[0]).distance(Point(sh[1]))**2 == shape.area:
			print('is square')
		else:
			print('not square')

print(points_list[2])
for line in range(0, line_count):
	find_triangle(points_list[line])
	find_square(points_list[line])

# for line in range(0, line_count):
# 	print(points_list[line][:3])

# shape = Polygon(points_list[0])
# print(shape.is_valid)

# triangle = Polygon([(1, 1), (2, 3), (3, 1)])

