#!/usr/bin/python3
import sys
import re
import atexit
import numpy as np
from datetime import datetime
from shapely.geometry import Point, Polygon

if len(sys.argv) != 2:
    print('invalid number of arguments', file=sys.stdout)
    exit(1)

try:
    with open(sys.argv[1], 'r') as fp:
        data = fp.readlines()
        line_count = len(data)
except IOError:
    print('could not open file ' + sys.argv[1], file=sys.stdout)
    exit(1)

log_file_name = 'result_file.txt'
log_file = open(log_file_name, 'w+')

def validate_data(data):
    line_pattern = re.compile('^((-?)([0-9]+):(-?)([0-9]+)(,?))+.$')
    for line in data:
        if not re.match(line_pattern, line) or re.match(re.compile('(.*),.$'), line):
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

def azimuth(point1, point2):
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return np.degrees(angle)if angle>0 else np.degrees(angle) + 360

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

def find_square(line):
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        shape = Polygon(sh)
        if (shape.is_valid
            and abs(Point(sh[0]).distance(Point(sh[1]))) ==
                abs(Point(sh[1]).distance(Point(sh[2])))):
            log(str(sh) + ' points form a square')

def find_parallelogram(line):
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        shape = Polygon(sh)
        if (shape.is_valid
            and abs(Point(sh[0]).distance(Point(sh[1]))) ==
                abs(Point(sh[2]).distance(Point(sh[3])))
            and abs(Point(sh[0]).distance(Point(sh[3]))) ==
                abs(Point(sh[1]).distance(Point(sh[2])))
            and abs(azimuth(Point(sh[0]), Point(sh[1]))
                - azimuth(Point(sh[2]), Point(sh[1]))) != 90.0):
            log(str(sh) + ' points form a parallelogram')

def find_trapezoid(line):
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        shape = Polygon(sh)
        if shape.is_valid:
            first_angle_pair_sum = abs((azimuth(Point(sh[1]), Point(sh[0]))
                                    - azimuth(Point(sh[3]), Point(sh[0])))
                                    + (azimuth(Point(sh[2]), Point(sh[1]))
                                    - azimuth(Point(sh[0]), Point(sh[1]))))

            second_angle_pair_sum = abs((azimuth(Point(sh[1]), Point(sh[0]))
                                    - azimuth(Point(sh[3]), Point(sh[0])))
                                    + (azimuth(Point(sh[0]), Point(sh[3]))
                                    - azimuth(Point(sh[2]), Point(sh[3]))))

            if first_angle_pair_sum == 180.0 or second_angle_pair_sum == 180.0:
                log(str(sh) + ' points form a trapezoid')

if __name__ == '__main__':

    validate_data(data)

    points_list = [[] for i in range(0, line_count)]
    point_pattern = re.compile('(-?[0-9]+):(-?[0-9]+)')

    for i, line in enumerate(data):
        line_points = re.findall(point_pattern, line)
        for point in line_points:
            points_list[i].append([float(idx) for idx in point])

    for line in range(0, line_count):
        find_triangle(points_list[line])
        find_square(points_list[line])
        find_parallelogram(points_list[line])
        find_trapezoid(points_list[line])