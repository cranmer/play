# Author: Kyle Cranmer <kyle.cranmer@nyu.edu>
# Licence: BSD

print(__doc__)
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA

# Next line to silence pyflakes.
Axes3D

#make some random samples in 2d
n_samples = 20
seed = np.random.RandomState(seed=3)

#this one looks cool
#gridMuSigma = np.array([np.linspace(0,1,n_samples),np.linspace(.1,3,n_samples)]).T

#create a set of Gaussians in a grid of mean (-1.5,1.5) and standard devaition (0.2,5)
gridMuSigma=[]
for i in np.linspace(-1.5,1.5,n_samples):
    for j in np.linspace(.2,5,n_samples):
        gridMuSigma.append([i,j])
gridMuSigma=np.array(gridMuSigma)

#probably an easier way to do with meshgrid, but needs to be reshaped
#gridMuSigma=np.meshgrid(np.linspace(-1.5,1.5,n_samples),np.linspace(0.2,5,n_samples))

# choose a different color for each point
colors = plt.cm.jet(np.linspace(0, 1, len(gridMuSigma)))

#use 2-d Gaussian information metric for distances
# see equation 7 from http://arxiv.org/abs/0802.2050 ("FINE" paper)
def getDistance(x,y):
    #going to define a measure here
    #print 'in getSim', x, y
    aa = x[0]-y[0]
    ab = x[1]+y[1]
    bb = x[1]-y[1]
    num = np.sqrt((aa**2+ab**2))+np.sqrt((aa**2+bb**2))
    den = np.sqrt((aa**2+ab**2))-np.sqrt((aa**2+bb**2))
    ret = np.log(num/den)
    return ret

# Create the array of "similarities" (distances) between points
tempSim=[]
for x in gridMuSigma:
    temp = []
    for y in gridMuSigma:
        temp.append(getDistance(x,y))
    tempSim.append(temp)
distances=np.array(tempSim)

#make 3d embedding 
mds = manifold.MDS(n_components=3, metric=True, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
embed3d = mds.fit(distances).embedding_

#make 2d embedding
mds2 = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
embed2d = mds2.fit(distances).embedding_

#Setup plots
fig = plt.figure(figsize=(5*3,4.5))

#make original grid plot
gridsubpl = fig.add_subplot(131)
gridsubpl.scatter(gridMuSigma[:, 0], gridMuSigma[:, 1], s=20, c=colors)
gridsubpl.set_xlabel('mean')
gridsubpl.set_ylabel('standard deviation')
plt.title('Original grid in mean and std. dev.')
plt.axis('tight')

# plot 3d embedding
#since it is a surface of constant negative curvature (hyperbolic geometry)
#expect it to look like the pseudo-sphere
#http://mathworld.wolfram.com/Pseudosphere.html
subpl = fig.add_subplot(132,projection='3d')
subpl.scatter(embed3d[:, 0], embed3d[:, 1], embed3d[:, 2],s=20, c=colors)
subpl.view_init(42, 101) #looks good when njobs=-1
subpl.view_init(-130,-33)#looks good when njobs=1

plt.suptitle('3D Multidim. Scailing Embedding')
plt.axis('tight')

# plot 2d embedding
subpl2 = fig.add_subplot(133)
subpl2.set_autoscaley_on(False)
subpl2.scatter(embed2d[:, 0], embed2d[:, 1],s=20, c=colors)
plt.title('2D Multidim. Scailing Embedding')
plt.axis('tight')

plt.savefig('gaussianInfoGeom.pdf')
plt.show()
