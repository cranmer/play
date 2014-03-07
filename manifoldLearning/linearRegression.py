print(__doc__)


# Code source: Jaques Grobler
# License: BSD 3 clause


import pylab as pl
import numpy as np
from sklearn import svm

nTest=100
X=np.reshape(np.linspace(0,1,2*nTest),[2*nTest,1])
Y=X**2

# Split the data into training/testing sets
diabetes_X_train = X[:-nTest]
diabetes_X_test = X[-nTest:]

# Split the targets into training/testing sets
diabetes_y_train = Y[:-nTest]
diabetes_y_test = Y[-nTest:]

# Create linear regression object
regr = svm.SVR()
# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((regr.predict(diabetes_X_test) - diabetes_y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))

# Plot outputs
pl.scatter(diabetes_X_test, diabetes_y_test,  color='black')
pl.plot(diabetes_X_test, regr.predict(diabetes_X_test), color='blue',
        linewidth=3)

pl.scatter(diabetes_X_train, diabetes_y_train,  color='black')
pl.plot(diabetes_X_train, regr.predict(diabetes_X_train), color='blue',
        linewidth=3)

pl.xticks(())
pl.yticks(())

pl.show()
