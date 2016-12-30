#!/usr/bin/python3
import sys
import re
import atexit
from datetime import datetime
from shapely.geometry import Point, Polygon

log_file_name = 'results/log_file_' + str(datetime.now()).replace(" ", "_") + '.txt'
log_file = open(log_file_name, 'w+')

def validate_data(data):
    line_pattern = re.compile('^(([0-9]+):([0-9]+)(,?))+.$')
    for line in data:
        if not re.match(line_pattern, line):
            log('invalid file')
            exit(1)
    return

def log(string):
    log_file.write(string + '\n')
    print(string, file=sys.stdout)
    return

def close_log(log_file):
    log_file.close()

atexit.register(close_log, log_file)

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
            log(str(sh) + ' points form a triangle')
        # else:
        #     print('not triangle')

def find_square(line):
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        shape = Polygon(sh)
        if (shape.is_valid
            and (Point(sh[0]).distance(Point(sh[1]))) ==
                (Point(sh[1]).distance(Point(sh[2])))):
            log(str(sh) + ' points form a square')
        # else:
        #   print('not square')

def find_parallelogram(line):
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        shape = Polygon(sh)
        if (shape.is_valid
            and (Point(sh[0]).distance(Point(sh[1]))) ==
                (Point(sh[2]).distance(Point(sh[3])))):
            log(str(sh) + ' points form a parallelogram')

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as fp:
        data = fp.readlines()
        line_count = len(data)

    validate_data(data)

    points_list = [[] for i in range(0, line_count)]
    point_pattern = re.compile('([0-9]+):([0-9]+)')

    for i, line in enumerate(data):
        line_points = re.findall(point_pattern, line)
        for point in line_points:
            points_list[i].append([float(idx) for idx in point])

    for line in range(0, line_count):
        find_triangle(points_list[line])
        find_square(points_list[line])
        find_parallelogram(points_list[line])

# for line in range(0, line_count):
#   print(points_list[line][:3])

# shape = Polygon(points_list[0])
# print(shape.is_valid)

# triangle = Polygon([(1, 1), (2, 3), (3, 1)])

