#!/usr/bin/python3

import re
from math import sqrt

# def get_data(file):
#     with open(file, 'r') as fp:
#         data = fp.read()
#     return data

# def validate_data(data):
#     valid_pattern = re.compile("^([0-9]+):([0-9]+)(,?)(\.)$")


line = "1:2,3:4,5:6." 
line.strip('.')
line_points_x = dict(('x' + v.strip(), x.strip()) for x,v in 
              (item.split(':') for item in line.split(',')))
print(line_points_x)

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def get_args(self):
        return (self.x, self.y,)

class Shape:

    def __init__(self, *args):
        self.args = args

    def is_triangle(self):
        points = self.args
        print(len(set(points)))
        if len(points)!=3 or len(set(points))!=len(points):
            return False
        else:
            side1 = sqrt((points[0][0] - points[1][0])**2 \
                       + (points[0][1] - points[1][1])**2)
            side2 = sqrt((points[1][0] - points[2][0])**2 \
                       + (points[1][1] - points[2][1])**2)
            side3 = sqrt((points[2][0] - points[0][0])**2 \
                       + (points[2][1] - points[0][1])**2)
            triangle = [side1, side2, side3,]
            triangle.sort()
            print(triangle)
            if triangle[2] < triangle[0] + triangle[1]:
                return True
            else:
                return False

    def get_args(self):
        return self.args

if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    p3 = Point(3, 3)
    sh = Shape(p1.get_args(), p2.get_args(), p3.get_args())
    print(sh.get_args())
    print(sh.is_triangle())