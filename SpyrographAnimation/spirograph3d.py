import numpy as np
from scipy import integrate
from numpy import sin, cos

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation
from fractions import gcd




#def lorentz_deriv((x, y, z), t0, sigma=10., beta=8./3, rho=28.0):
#    """Compute the time-derivative of a Lorentz system."""
#    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]

class spirograph():
    def __init__(self,a,b,f,noZ=False):
        self._a=a
        self._b = b
        self._rho = f*a
        self._f = f  
        self._noZ = noZ 
    def inspect(self):
        print self._a, self._b, self._f
    def graph(self,t0):
        if t0==0: self.inspect()
        a=self._a
        b=self._b
        rho=self._rho
        f=self._f
        lengthscale=5.*2*np.pi/b 
        timescale=min(a,b)/gcd(a,b)
        return (lengthscale*((b-a)*cos(timescale*t0)+rho*cos(-(1.*b/a -1.)*timescale*t0)),
                lengthscale*((b-a)*sin(timescale*t0)+rho*sin(-(1.*b/a -1.)*timescale*t0)),
                0 if self._noZ else 5*t0 )

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = [[10,0,0]]


# Solve for the trajectories
t = np.linspace(0, 2*np.pi, 500)
#x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
#                  for x0i in x0])

noZswitch=True
myspiros = [spirograph(a=63,b=96,f=0.8,noZ=noZswitch),spirograph(a=63,b=96,f=0.6,noZ=noZswitch),
            spirograph(a=51,b=96,f=0.8,noZ=noZswitch),spirograph(a=51,b=96,f=0.6,noZ=noZswitch)]
N_trajectories = len(myspiros)


x_t = np.asarray([[myspiro.graph(t0) for t0 in t] for myspiro in myspiros])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    i = (2 * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(90*cos(np.pi*i/500.), 0.3 * i)
    fig.canvas.draw()
    return lines + pts

# instantiate the animator.
#anim = animation.FuncAnimation(fig, animate, init_func=init,
#                               frames=500, interval=30, blit=True)

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=30,blit=True)
# Save as mp4. This requires mplayer or ffmpeg to be installed

#FFMpegWriter = animation.writers['ffmpeg']
#metadata = dict(title='Movie Test', artist='Matplotlib',
#        comment='Movie support!')
#writer = FFMpegWriter(fps=15, metadata=metadata)
#anim.save("spyro.mp4", fps=15, extra_args=['-vcodec', 'libx264'])
#anim.save("spyro.mp4", fps=15, extra_args=["-c:v", "h264"])
#anim.save("spyro.mp4", fps=15,codec='libx264')
anim.save("spyro.mp4", fps=15,extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])

#with writer.saving(plt.figure, "spiro_test.mp4", 100):
#    print "in side with"

#plt.show()
