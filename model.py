import numpy as np
from sklearn.ensemble import RandomForestRegressor

X = np.loadtxt('features.csv', delimiter=',')
y = np.loadtxt('labels.csv', delimiter=',')

rf = RandomForestRegressor(n_estimators=500, n_jobs=-1, oob_score=True)
rf.fit(X, y)
print('r2 training score', rf.score(X, y))
print('oob score', rf.oob_score)
