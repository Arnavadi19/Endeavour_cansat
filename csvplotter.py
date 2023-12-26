import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
class CsvPlot():
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1,1,1)

        self.list_pressure=[]
        self.list_time=[]
        self.lines = []

        def animate(i):

            pressure,time = (s.strip() for s in lines[i].split(','))
            self.list_pressure.append(int(pressure))
            self.list_time.append(int(time))
            self.ax.clear()
            self.ax.plot(self.list_time,self.list_pressure)


        with open(os.path.join(os.path.realpath('.'), 'sample.csv'),'r') as f:
            next(f) # skip header
            lines = f.readlines()

        anim = animation.FuncAnimation(self.fig, animate, interval=500, frames=len(lines)) 
        plt.show()
    #anim.save(os.path.join(os.path.realpath('.'), 'livetime.gif'), writer='imagemagick')
CsvPlot()