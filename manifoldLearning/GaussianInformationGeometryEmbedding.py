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
#X_true = np.array([np.linspace(0,1,n_samples),np.linspace(.1,3,n_samples)]).T

X_true=[]
for i in np.linspace(0,3,n_samples):
    for j in np.linspace(.2,5,n_samples):
        X_true.append([i,j])
X_true=np.array(X_true)

#print X_true

#use 2-d Gaussian information metric for distances
# see equation 7 from 0802.2050 ("FINE" paper)
def getSimilarities(x,y):
    #going to define a measure here
    #print 'in getSim', x, y
    aa = x[0]-y[0]
    ab = x[1]+y[1]
    bb = x[1]-y[1]
    num = np.sqrt((aa**2+ab**2))+np.sqrt((aa**2+bb**2))
    den = np.sqrt((aa**2+ab**2))-np.sqrt((aa**2+bb**2))
    ret = np.log(num/den)
    return ret


tempSim=[]
for x in X_true:
    temp = []
    for y in X_true:
        temp.append(getSimilarities(x,y))
    tempSim.append(temp)
similarities=np.array(tempSim)


mds = manifold.MDS(n_components=3, metric=True, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=-1)
pos = mds.fit(similarities).embedding_

# Rescale the data
pos *= np.sqrt((X_true ** 2).sum()) / np.sqrt((pos ** 2).sum())

# Rotate the data
#clf = PCA(n_components=3)
#pos = clf.fit_transform(pos)

fig = plt.figure(figsize=(8,8))
#subpl = fig.add_subplot(111,projection='3d')
subpl = fig.add_subplot(121,projection='3d')


#make 3d scatter
# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, len(X_true)))
#subpl.scatter(pos[:, 0], pos[:, 1], pos[:, 2],s=20, c='g')
subpl.scatter(pos[:, 0], pos[:, 1], pos[:, 2],s=20, c=colors)
plt.axis('tight')
#plt.savefig('gaussianInfoGeom-3dEmbed.pdf')
#plt.show()


#make 2d scatter
mds2 = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
pos2 = mds2.fit(similarities).embedding_

#fig2 = plt.figure(figsize=(8,8))
#subpl2 = fig2.add_subplot(111)
subpl2 = fig.add_subplot(122)
subpl2.scatter(pos2[:, 0], pos2[:, 1],s=20, c=colors)


plt.axis('tight')
plt.savefig('gaussianInfoGeom-2dEmbed.pdf')
plt.show()
