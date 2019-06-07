import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split

X = np.loadtxt('features.csv', delimiter=',')
y = np.loadtxt('labels.csv', delimiter=',')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=42)
# rf = HistGradientBoostingRegressor()
rf.fit(X_train, y_train)
print('r2 training score', rf.score(X_train, y_train))
print('r2 test score', rf.score(X_test, y_test))
