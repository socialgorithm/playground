import random as rand
import sympy as sy
import math

NUMBER_OF_RANDOM_POINTS = 25
TRACK_BORDER_WIDTH = 20
class Track:

    def __init__(self, windowSize=(800, 600), minLines=10):
        self.randomPoints = []
        self.width = windowSize[0] - TRACK_BORDER_WIDTH
        self.height = windowSize[1] - TRACK_BORDER_WIDTH
        self._generateRandomPoints()
        self._generateConvexHull()
        # checking for intersections
        hasIntersections = self.hasIntersections()
        toFewLines = len(self.track_lines) < minLines
        while hasIntersections or toFewLines:
            if toFewLines:
                print("Too few lines ({})!".format(minLines))
            if hasIntersections:
                print("Track has intersections!")
            self._generateRandomPoints()
            self._generateConvexHull()
            hasIntersections = self.hasIntersections()
            toFewLines = len(self.track_lines) < minLines
        # expanding to window size
        self._resizeTrack()
        # smoothing
        self.track_points = self._smooth(self.track_points)

    @staticmethod
    def _smooth(track_points):
        new_points = [0 for i in range(len(track_points)*2)]
        for index1 in range(0,len(new_points), 2):
            index2 = index1 + 2
            mid_point_index = index1 + 1
            point1 = track_points[int(index1/2)]
            point2 = track_points[int(index2/2)]
            if point1.x > point2.x:
                mid_point_x = point1.x - point2.x
            elif point1.x < point2.x:
                mid_point_x = point2.x - point1.x
            if point1.y > point2.y:
                mid_point_y = point1.y - point2.y
            elif point1.y < point2.y:
                mid_point_y = point2.y - point1.y
            new_points[index1] = point1
            new_points[mid_point_index] = sy.Point2D(mid_point_x, mid_point_y)
        return new_points

    def _generateRandomPoints(self):
        self.randomPoints.clear()
        self.startingPoint = sy.Point2D(self.width, self.height)
        point = None
        for num in range(NUMBER_OF_RANDOM_POINTS):
            # generating unique random point on grid
            while point is None or point in self.randomPoints:
                point = sy.Point2D(rand.randrange(0, self.width),
                                   rand.randrange(0, self.height))
            self.randomPoints.append(point)
            # selecting the starting point of the track
            if point.x < self.startingPoint.x:
                self.startingPoint = point

    def _generateConvexHull(self):
        print("GENERATING...")
        current_point = self.startingPoint
        free_points = self.randomPoints[:]  # points that can still be used for track formation
        self.track_points = []  # points that form the track
        closed_loop = False
        x_delta = 1  # if track is going forwards or backwards
        while not closed_loop:
            self.track_points.append(current_point)
            if current_point != self.startingPoint:
                free_points.remove(current_point)
            # determine point with smallest angle to current point
            ref_point = sy.Point2D(current_point.x, current_point.y - 1)
            sAng_point = {'Point': None, 'Angle': None}
            starting_search_dist = 120
            while True:
                for point in free_points:
                    if current_point == point:
                        continue
                    curr2ref = math.atan2(ref_point.y - current_point.y, ref_point.x - current_point.x)
                    curr2point = math.atan2(point.y - current_point.y, point.x - current_point.x)
                    angle = ((curr2point - curr2ref) * (180 / math.pi))
                    if angle < 0:
                        angle += 360
                    # restrict maximum distance to look for connecting point
                    mag = math.sqrt((point.x - current_point.x)**2 + (point.y - current_point.y)**2)
                    if mag > starting_search_dist and len(free_points) > 1:
                        continue
                    # prevent going backwards
                    if x_delta < 0 and current_point.x <= point.x and point != self.startingPoint:
                        continue
                    # update point
                    if sAng_point['Point'] is None or sAng_point['Angle'] > angle:
                        sAng_point['Point'] = point
                        sAng_point['Angle'] = angle
                if sAng_point['Point'] is None:
                    # no point found, increasing search distance
                    starting_search_dist += 10
                else:
                    x_delta = sAng_point['Point'].x - current_point.x
                    break
            current_point = sAng_point['Point']
            # checking if loop is closed
            if current_point == self.startingPoint:
                self.track_points.append(self.startingPoint)
                closed_loop = True

    def hasIntersections(self):
        prev_track_point = None
        self.track_lines = []
        for track_point in self.track_points:
            if prev_track_point is None:
                prev_track_point = track_point
                continue
            newSegment = sy.Segment2D(prev_track_point, track_point)
            self.track_lines.append(newSegment)
            prev_track_point = track_point
        print("CHECKING-------------------")
        for i in range(0,len(self.track_lines)-1):
            line1 = self.track_lines[i]
            for j in range(i+1, len(self.track_lines)):
                if i == j:
                    continue
                line2 = self.track_lines[j]
                intersections = line1.intersection(line2)
                if len(intersections) == 0:
                    continue
                elif 0 <= len(intersections) < 2:
                    if intersections[0] not in [line1.p1, line1.p2, line2.p1, line2.p2]:
                        if intersections[0] != self.startingPoint:
                            print("INTERSECTION: {}".format(intersections))
                            return True
                    continue
                else:
                    print("MULTIPLE_INTERSECTIONS: {}".format(intersections))
                    return True
        print("Passed.")
        return False

    # from stack overflow, sympy line intersection is broken !
    def line_intersection(self, line1, line2):
        xdiff = (line1.p1.x - line1.p2.x, line2.p1.x - line2.p2.x)
        ydiff = (line1.p1.y - line1.p2.y, line2.p1.y - line2.p2.y)  # Typo was here

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            return []

        d = (det(*[[line1.p1.x,line1.p1.y],[line1.p2.x,line1.p2.y]]),
             det(*[[line2.p1.x,line2.p1.y],[line2.p2.x,line2.p2.y]]))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        # test if intersection if within line segment
        return [sy.Point2D(x, y)]

    def _resizeTrack(self):
        self._determine_edge_points()
        # align track with window edges
        x_offset_edge = self.leftPoint.x - TRACK_BORDER_WIDTH
        y_offset_edge = self.bottomPoint.y - TRACK_BORDER_WIDTH
        self.track_points = [sy.Point2D(point.x-x_offset_edge,point.y-y_offset_edge) for point in self.track_points]
        self._determine_edge_points()
        # determining bounding box of track
        track_width = self.rightPoint.x - self.leftPoint.x
        track_height = self.topPoint.y - self.bottomPoint.y
        width_multiplier = (self.width - 2*TRACK_BORDER_WIDTH)/track_width
        height_multiplier = (self.height - 2*TRACK_BORDER_WIDTH)/track_height
        self.track_points = [sy.Point2D(int(point.x*width_multiplier), int(point.y*height_multiplier))
                             for point in self.track_points]

    def _determine_edge_points(self):
        self.topPoint = None
        self.bottomPoint = None
        self.leftPoint = None
        self.rightPoint = None
        for point in self.track_points:
            if self.topPoint is None or point.y > self.topPoint.y:
                self.topPoint = point
            if self.bottomPoint is None or point.y < self.bottomPoint.y:
                self.bottomPoint = point
            if self.leftPoint is None or point.x < self.leftPoint.x:
                self.leftPoint = point
            if self.rightPoint is None or point.x > self.rightPoint.x:
                self.rightPoint = point




