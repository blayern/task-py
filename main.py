#!/usr/bin/python3
import sys
import re
import atexit
import math
import numpy as np
from operator import itemgetter
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
    """function for validating input data"""
    line_pattern = re.compile('^((-?)([0-9]+):(-?)([0-9]+)(,?))+.$')
    for line in data:
        if not re.match(line_pattern, line) or re.match(re.compile('(.*),.$'), line):
            log('invalid file')
            exit(1)
    return

def log(string):
    """function used for loggin results in log_file and on stdout"""
    log_file.write(string + '\n')
    print(string, file=sys.stdout)
    return

def close_log(log_file):
    """function for closing log_file"""
    log_file.close()

"""register close_log() on exit"""
atexit.register(close_log, log_file)

def azimuth(point1, point2):
    """function for calculating angle between points"""
    angle = np.arctan2(point2.x - point1.x, point2.y - point1.y)
    return np.degrees(angle)if angle>0 else np.degrees(angle) + 360

def batch(iterable, count=1):
    """function for getting count number coordinates from line"""
    iterable_len = len(iterable)
    for idx in range(0, iterable_len, count):
        yield iterable[idx:min(idx+count, iterable_len)]

def find_triangle(line):
    """function for finding shape triangle from given points"""
    for sh in batch(line, 3):
        if len(sh)<3:
            return
        # sh = sorted(sh, key=lambda sh: sh[1])
        shape = Polygon(sh)
        if shape.is_valid:
            log(str(sh) + ' points form a triangle')


def find_square(line):
    """function for finding shape square from given points"""
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        # p = Point(sh[0])
        # sh = sorted(sh, key=lambda sh: (p.y, p.x))
        print(sh, 'square-un')
        mx = sum(x[0] for x in sh) / len(sh)
        my = sum(x[1] for x in sh) / len(sh)
        def algo(x):
            return (math.atan2(x[0] - mx, x[1] - my) + 2 * math.pi) % (2*math.pi)
        sh.sort(key=algo)
        # sh = sorted(sh, key=lambda p: (p[1], p[0]), reverse=True)
        print(sh, 'square')
        # sh = sorted(sh, key=lambda p: p[0], reverse=False)
        # sh = sorted(sh, key=lambda p: p[1], reverse=False)
        shape = Polygon(sh)
        if (shape.is_valid
            and abs(Point(sh[0]).distance(Point(sh[1]))) ==
                abs(Point(sh[1]).distance(Point(sh[2])))):
            log(str(sh) + ' points form a square')

def find_parallelogram(line):
    """function for finding shape parallelogram from given points"""
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        p = Point(sh[0])
        mx = sum(x[0] for x in sh) / len(sh)
        my = sum(x[1] for x in sh) / len(sh)
        def algo(x):
            return (math.atan2(x[0] - mx, x[1] - my) + 2 * math.pi) % (2*math.pi)
        sh.sort(key=algo)
        # sh = sorted(sh, key=lambda sh: (p.y, p.x))
        # print(sh, 'para')
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
    """function for finding shape trapezoid from given points"""
    for sh in batch(line, 4):
        if len(sh)<4:
            return
        p = Point(sh[0])
        mx = sum(x[0] for x in sh) / len(sh)
        my = sum(x[1] for x in sh) / len(sh)
        def algo(x):
            return (math.atan2(x[0] - mx, x[1] - my) + 2 * math.pi) % (2*math.pi)
        sh.sort(key=algo)
        # sh = sorted(sh, key=lambda sh: (p.y, p.x))
        # print(sh, 'trap')
        shape = Polygon(sh)
        if shape.is_valid:
            if (abs(Point(sh[0]).distance(Point(sh[1]))) != abs(Point(sh[2]).distance(Point(sh[3])))) or (abs(Point(sh[0]).distance(Point(sh[3]))) != abs(Point(sh[1]).distance(Point(sh[2])))):
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