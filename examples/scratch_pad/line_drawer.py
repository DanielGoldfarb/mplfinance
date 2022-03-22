import matplotlib.pyplot as plt

class LineDrawer(object):
    lines = []
    def draw_line(self):
        ax = plt.gca()
        xy = plt.ginput(2)

        x = [p[0] for p in xy]
        y = [p[1] for p in xy]

        print('x=',x,'y=',y)
        line = plt.plot(x,y)
        ax.figure.canvas.draw()
        self.lines.append(line)


plt.plot([1,2,3,4,5])
ld = LineDrawer()
ld.draw_line() # here you click on the plot
