from sympy import *
import sympy as sy
import tkinter as tk


class Track:

    def __init__(self, track_data: list):
        """
        creates instance of the track class which is used to store the layout of the track in a form that can be used to
        do the calculations needed for intersections etc.

        :param track_data: [ {'inner': (int,int), 'outer':(int,int)}, ... ]
        :type track_data: list
        """

        self.inner_points_raw = []  # points associated with inner part of track, (int x, int y)
        self.outer_points_raw = []  # point associated with outer part of track, (int x, int y)
        self.inner_points_sympy = []  # points associated with inner part of track, as sympy points
        self.outer_points_sympy = []  # point associated with outer part of track, as sympy points
        for item in track_data:
            self.inner_points_raw.append(item['inner'])
            self.outer_points_raw.append(item['outer'])
            inner_sympy_point = Point2D(item['inner'][0], item['inner'][1])
            outer_sympy_point = Point2D(item['outer'][0], item['outer'][1])
            self.inner_points_sympy.append(inner_sympy_point)
            self.outer_points_sympy.append(outer_sympy_point)
        # lines between the track points
        self.inner_segments_sympy = []
        self.outer_segments_sympy = []
        self.section_segments_sympy = []
        """
        section_lines:
        These are lines that go from the nth inner point to the nth outer point, drawing straight lines running perpen-
        dicular to the direction of the track. The idea is that these can be used to track the cars progress along the
        track (for the fitness func). it can also be used to remove previous and future pices of the track from the 
        intersection calculations to save processor cycles:
        
        ---------------------------------------------------------------------------------------------------------------
        |           A           |             B          |         C         |          D        |          E         |
        ---------------------------------------------------------------------------------------------------------------
        
        if all cars in the simulation have passed the section line at the end of B, but no car has passed line at end of
        C, then all points associated with sections A and E can be ignored in all calculations. The decision of what 
        sections to ignore could also be taken on a car by car basis
        """
        for index, curr_inner_point in enumerate(self.inner_points_sympy):
            curr_outer_point = self.outer_points_sympy[index]
            segment_section = Segment2D(curr_inner_point, curr_outer_point)
            self.section_segments_sympy.append(segment_section)
            if index == 0:
                # cannot form a line with just one point
                continue
            # creating inner and outer track segments
            prev_inner_point = self.inner_points_sympy[index - 1]
            prev_outer_point = self.outer_points_sympy[index - 1]
            segment_inner = Segment2D(prev_inner_point, curr_inner_point)
            segment_outer = Segment2D(prev_outer_point, curr_outer_point)
            self.inner_segments_sympy.append(segment_inner)
            self.outer_segments_sympy.append(segment_outer)
        # creating combined list of all sympy track geometry objects
        self.track_geometry_segments = []
        self.track_geometry_segments.extend(self.inner_segments_sympy)
        self.track_geometry_segments.extend(self.outer_segments_sympy)
        """
        OTHER CLASS ATTRIBUTES:
        """

        self.draw_ids_tk = [] # list of IDs of objects drawn to tkinter canvas, used for deleting them when redrawing

    def intersectsWithTrack(self, sympy_object):
        intersections = []
        for track_segment in self.track_geometry_segments:
            intersections.extend(sy.intersection(track_segment, sympy_object))
        return intersections


    def draw(self, canvas: tk.Canvas, redraw=False, draw_section_segments=False):
        if len(self.draw_ids_tk) != 0 and not redraw:
            return
        elif len(self.draw_ids_tk) != 0 and redraw:
            # remove all previous objects from canvas to prevent simulation grinding to a halt
            canvas.delete(self.draw_ids_tk)
            self.draw_ids_tk.clear()
        # Drawing lines first. points are drawn after so that lines don't overlap points
        for index in range(len(self.inner_points_sympy)):
            curr_point_inner = self.inner_points_raw[index]
            curr_point_outer = self.outer_points_raw[index]
            # section segments
            if draw_section_segments:
                section = canvas.create_line(curr_point_inner, curr_point_outer, fill="yellow")
                self.draw_ids_tk.append(section)
            # drawing the inner and outer track lines
            if index == 0:
                # index at first point, so there is no prev point to draw line with
                continue
            prev_point_inner = self.inner_points_raw[index - 1]
            prev_point_outer = self.outer_points_raw[index - 1]
            inner_section = canvas.create_line(prev_point_inner, curr_point_inner, fill="black")
            outer_section = canvas.create_line(prev_point_outer, curr_point_outer, fill="black")
            self.draw_ids_tk.append(inner_section)
            self.draw_ids_tk.append(outer_section)