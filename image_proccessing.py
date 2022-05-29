import math as m
import os
from copy import deepcopy

import cv2
import matplotlib.pyplot as plt
import numpy as np

images_dir = 'Dataset_BUSI_with_GT'


def center(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 + x2) / 2, (y1 + y2) / 2


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return m.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def standard_error(sample):
    sd = 0
    mean = np.mean(sample)
    n = len(sample)
    for i in sample:
        sd += (i - mean) ** 2
    sd /= (n - 1)
    sd = m.sqrt(sd)
    return sd / m.sqrt(n)


def equation_by_corner_and_dot(dot, corner):
    x, y = dot
    if corner not in (0, 180):
        corner = np.radians(corner)
        k = m.tan(corner)
        b = y - k * x
        return k, b
    return x


def equation_by_two_dots(dot1, dot2):
    x1, y1 = dot1
    x2, y2 = dot2
    if x1 != x2:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
        return k, b
    return x1


def intersection(eq1, eq2):
    if type(eq1) == tuple and type(eq2) == tuple:
        a, c = eq1
        b, d = eq2
        if a == b:
            return None
        x = (d - c) / (a - b)
        y = a * x + c
        return x, y
    elif type(eq1) != tuple and type(eq2) == tuple:
        x = eq1
        k, b = eq2
        y = k * x + b
        return x, y
    elif type(eq1) == tuple and type(eq2) != tuple:
        x = eq2
        k, b = eq1
        y = k * x + b
        return x, y
    else:
        return None


def find_radiuses(contour):
    x, y = list(), list()
    for point in contour:
        x.append(point[0][0])
        y.append(point[0][1])
        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)
    center_point = center((min_x, min_y), (max_x, max_y))

    intersections = list()
    for corner in range(1, 361, 2):
        intersections_for_current_corner = list()
        e1 = equation_by_corner_and_dot(center_point, corner)
        for i in range(len(contour)):
            if i < len(contour) - 1:
                point1, point2 = contour[i][0], contour[i + 1][0]
            else:
                point1, point2 = contour[-1][0], contour[0][0]
            e2 = equation_by_two_dots(point1, point2)
            inter = intersection(e1, e2)
            if inter:
                x_i, y_i = inter
                if y_i >= center_point[1] and corner < 180:
                    if type(e2) != tuple:
                        if min(point1[1], point2[1]) <= y_i < max(point1[1], point2[1]):
                            intersections_for_current_corner.append(inter)
                    else:
                        if e2[0] == 0:
                            if min(point1[0], point2[0]) <= x_i < max(point1[0], point2[0]):
                                intersections_for_current_corner.append(inter)
                        else:
                            if min(point1[1], point2[1]) <= y_i < max(point1[1], point2[1]) and min(point1[0], point2[0]) <= x_i < max(point1[0], point2[0]):
                                intersections_for_current_corner.append(inter)
                if y_i <= center_point[1] and corner > 180:
                    if type(e2) != tuple:
                        if min(point1[1], point2[1]) <= y_i < max(point1[1], point2[1]):
                            intersections_for_current_corner.append(inter)
                    else:
                        if e2[0] == 0:
                            if min(point1[0], point2[0]) <= x_i < max(point1[0], point2[0]):
                                intersections_for_current_corner.append(inter)
                        else:
                            if min(point1[1], point2[1]) <= y_i < max(point1[1], point2[1]) and min(point1[0], point2[0]) <= x_i < max(point1[0], point2[0]):
                                intersections_for_current_corner.append(inter)
        try:
            intersections.append(
                sorted(intersections_for_current_corner, key=lambda x: distance(center_point, x))[0])
        except IndexError:
            continue

    radiuses = list()
    for i in intersections:
        radiuses.append(distance(center_point, i))

    return radiuses, intersections


class Photo:
    def __init__(self, img):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = sorted(contours, key=lambda x: len(x))[-1]

        x, y = list(), list()
        for point in contour:
            x.append(point[0][0])
            y.append(point[0][1])
            min_x, max_x = min(x), max(x)
            min_y, max_y = min(y), max(y)

        center_point = center((min_x, min_y), (max_x, max_y))
        x_c = int(center_point[0])
        y_c = int(center_point[1])

        self.perimeter = 0
        for i in range(len(contour)):
            if i != len(contour) - 1:
                self.perimeter += distance(contour[i][0], contour[i + 1][0])
            else:
                self.perimeter += distance(contour[0][0], contour[-1][0])

        radiuses, intersections = find_radiuses(contour)

        self.radius_mean = np.mean(radiuses)
        self.radius_se = standard_error(radiuses)
        self.radius_worst = np.mean(sorted(radiuses)[-3:])

        areas = [np.pi * r ** 2 for r in radiuses]
        self.area_mean = np.mean(areas)
        self.area_se = standard_error(areas)
        self.area_worst = np.mean(sorted(areas)[-3:])

        compactnesses = [self.perimeter ** 2 / a for a in areas]
        self.compactness_mean = np.mean(compactnesses)
        self.compactness_se = standard_error(compactnesses)
        self.compactness_worst = np.mean(sorted(compactnesses)[-3:])

        symmetries = list()
        for i in range(len(radiuses) // 2):
            symmetries.append(
                min(radiuses[i], radiuses[len(radiuses) // 2 + i]) / max(radiuses[i], radiuses[len(radiuses) // 2 + i]))
        self.symmetry_mean = np.mean(symmetries)
        self.symmetry_se = standard_error(symmetries)
        self.symmetry_worst = np.mean(sorted(symmetries)[-3:])

        steps = (1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20)
        fractal_dimensions = list()

        # uncomment to draw fractal dimension
        for step in steps:
            L = 0
            # step_img = deepcopy(img)
            for i in range(0, len(intersections), step):
                if i + step < len(intersections):
                    L += distance(intersections[i], intersections[i + step])
                    # cv2.line(step_img, (int(intersections[i][0]), int(intersections[i][1])),
                    #          (int(intersections[i + step][0]), int(intersections[i + step][1])), (0, 255, 0), 4)
                else:
                    L += distance(intersections[i], intersections[0])
                    # cv2.line(step_img, (int(intersections[i][0]), int(intersections[i][1])),
                    #          (int(intersections[0][0]), int(intersections[0][1])), (0, 255, 0), 4)
            fractal_dimensions.append(L)
            # cv2.imshow(f'step={step}', step_img)
            # cv2.waitKey(0)

        self.fractal_dimension_mean = np.mean(fractal_dimensions)
        self.fractal_dimension_se = standard_error(fractal_dimensions)
        self.fractal_dimension_worst = np.mean(sorted(fractal_dimensions)[-3:])

        # uncomment to draw contour
        # cv2.drawContours(img, [contour], 0, (0, 255, 0), 3)
        # cv2.imshow('img', img)
        # cv2.waitKey(0)

        # uncomment to draw rectangle
        # cv2.line(img, (min_x, min_y), (min_x, max_y), (0, 255, 0), 3)
        # cv2.line(img, (min_x, max_y), (max_x, max_y), (0, 255, 0), 3)
        # cv2.line(img, (max_x, max_y), (max_x, min_y), (0, 255, 0), 3)
        # cv2.line(img, (max_x, min_y), (min_x, min_y), (0, 255, 0), 3)

        # uncomment to draw center point
        # cv2.circle(img, (x_c, y_c), 5, (0, 255, 0), 5)

        # uncomment to draw radiuses
        # for inter in intersections:
        #     cv2.line(img, (x_c, y_c), (int(inter[0]), int(inter[1])), (0, 255, 0), 1)

        # uncomment to show image
        # cv2.imshow('img', img)
        # cv2.waitKey(0)

        # uncomment to plot fractal dimension - step graph
        # plt.plot(steps, fractal_dimensions)
        # plt.xlabel('Step')
        # plt.ylabel('Length')
        # plt.show()


# img_path = os.path.join(images_dir, 'benign/benign (9)_mask.png')
# img = cv2.imread(img_path)
# img = Photo(img)
