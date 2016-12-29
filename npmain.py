#!/usr/bin/python3
import sys
import re
from shapely.geometry import Point, Polygon

with open(sys.argv[1], 'r') as fp:
	data = fp.readlines()
	line_count = len(data)

print(data)

points_list = [[] for i in range(0, line_count)]
point_pattern = re.compile('([0-9]+):([0-9]+)')

for i, lne in enumerate(data):
	line_points = re.findall(point_pattern, data[i])
	print(line_points)
	for point in line_points:
		points_list[i].append([float(idx) for idx in point])

for line in range(0, line_count):
	print(points_list[line])


shape = Polygon(points_list[0])
print(shape.is_valid)

triangle = Polygon([(1, 1), (2, 3), (3, 1)])