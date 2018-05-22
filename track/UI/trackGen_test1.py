from tkinter import *
from src.trackGen.track import Track


# colors
blue = "#0000FF"
red = "#FF0000"
green = '#00FF00'
black = '#000000'

class trackGen:

    def __init__(self, window_size=(800, 600), loop=True):
        self.root = Tk()
        self.window_size = window_size
        self.canvas = Canvas(self.root, width=window_size[0], height=window_size[1])
        self.canvas.pack()
        self.genTrack(loop)
        self.root.mainloop()

    def genTrack(self,loop=True):
        track = Track(self.window_size, numberOfPoints=25)
        self.displayTrack(track)
        if loop:
            self.root.after(100,self.genTrack)


    def displayTrack(self,track):
        self.canvas.create_rectangle(0,0,self.window_size[0],self.window_size[1], fill=black)
        # drawing the points used to generate track
        for point in track.randomPoints:
            x1, y1 = int(point.x - 2), int(point.y - 2)
            x2, y2 = int(point.x + 2), int(point.y + 2)
            if point == track.startingPoint:
                self.canvas.create_oval(x1, y1, x2, y2, fill=red, width=0)
            else:
                self.canvas.create_oval(x1, y1, x2, y2, fill=blue, width=0)

        # drawing the lines that form the track
        first = True
        for index, point in enumerate(track.track_points):
            if index == 0:
                continue
            current_point = track.track_points[index]
            previous_point = track.track_points[index - 1]
            x1, y1 = previous_point.x, previous_point.y
            x2, y2 = current_point.x, current_point.y
            if first:
                self.canvas.create_line(x1, y1, x2, y2, fill=green, width=2)
                first = False
            else:
                self.canvas.create_line(x1, y1, x2, y2, fill=red, width=2)

if __name__ == "__main__":
    t = trackGen()