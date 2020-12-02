import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
#from sklearn.externals import joblib

data=pd.read_csv('./auto-mpg.csv')
data=data.drop('car name',axis=1)
data['origin']=data['origin'].replace({1:'America',2:'Europe',3:'Asia'})
data=pd.get_dummies(data,columns=['origin'])
print(data.isnull().sum())
data['horsepower']=data['horsepower'].fillna(data.horsepower.median())
print(data.isnull().sum())
X=data.drop(['mpg','origin_Europe'],axis=1)
y=data[['mpg']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=1)
model = LinearRegression()
model.fit(X_train,y_train)
yhat=model.predict(X_test)
#print(yhat)
pickle.dump(model,open('./mpgmodel.pkl','wb'))

# =============================================================================
# conn.execute('''CREATE TABLE MPGTABLE
# (
# carID TEXT PRIMARY KEY,
# cylinders REAL,
# displacement INT,
# horsepower INT,
# weight INT,
# acceleration REAL,
# model year INT,
# origin INT,
# mpg REAL NOT NULL);''')
# =============================================================================
