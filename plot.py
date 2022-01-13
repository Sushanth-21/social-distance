import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from random import randint


# creating a blank window
# for the animation
fig = plt.figure()
axis=fig.add_subplot(111, projection='3d')
#axis = plt.axes(xlim =(-50, 50),ylim =(-50, 50))
axis.set_xlim(0,200)

axis.set_ylim(0,160)

axis.set_zlim(0,100)
line = axis.scatter([], [],[])

# what will our line dataset
# contain?
def init():
    line._offsets3d=([], [],[])
    return line,

# initializing empty values
# for x and y co-ordinates
xdata, ydata, zdata = [], [], []

# animation function
def animate(i):
    x=randint(0,100)
    y=randint(0,100)
    z=randint(0,100)
    # xdata, ydata, zdata = [1], [1], [1]
    xdata.append(x)
    ydata.append(y)
    zdata.append(z)
    line._offsets3d=(xdata, ydata,zdata)
    
    return line,

# calling the animation function
anim = animation.FuncAnimation(fig, animate,
                            init_func = init,
                            frames = 100,
                            blit = False, cache_frame_data=False)

# saves the animation in our desktop
#anim.save('growingCoil.mp4', writer = 'ffmpeg', fps = 30)
plt.show()
#anim.save('animation.gif', writer='PillowWriter', fps=30)
