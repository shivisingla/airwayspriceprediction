# -*- coding: utf-8 -*-
"""Flight Fare Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OTnnWRM3lf4XcSRUGaSRosOHVyoAu42g
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn

"""# Reading data from the excel file"""

dataset=pd.read_excel("Data_flight.xlsx")

dataset.head()

## checking for the number of airlines available
np.unique(dataset['Airline'])

np.unique(dataset['Airline']).size

## looing at the number of opbservations for each airline
dataset['Airline'].value_counts()

dataset['Price'].describe()

"""# finding the null values in the dataset if they exist """

dataset.info()

#obserbving the relation between prices over the source and destination

sns.catplot(y = "Price", x = "Source", data = dataset.sort_values("Price", ascending = False), kind="boxen", height = 4, aspect = 3)
plt.show()

sns.catplot(y = "Price", x = "Airline", data = dataset.sort_values("Price", ascending = False), kind="boxen", height = 6, aspect = 3)
plt.show()

dataset.isnull().sum()

## filling the NA values
dataset.dropna(inplace=True)

dataset.isnull().sum()

#Extracting journey day,month from the date_of_journey into journey_day and journey_month
#deleting the date_of_journey as it is not useful after extraction of day and month

dataset["Journey_day"] = pd.to_datetime(dataset.Date_of_Journey, format="%d/%m/%Y").dt.day
dataset["Journey_month"] = pd.to_datetime(dataset.Date_of_Journey, format = "%d/%m/%Y").dt.month
dataset.drop(["Date_of_Journey"],axis=1,inplace=True)

dataset.head()

#similarly extracting departure hours and minutes from the departure time

dataset["Dep_hour"]=pd.to_datetime(dataset.Dep_Time).dt.hour
dataset["Dep_min"]=pd.to_datetime(dataset.Dep_Time).dt.minute
dataset.drop(["Dep_Time"],axis=1,inplace=True)

dataset

#similarly extracting arrival hour and minute fromm the arrival time

dataset["Arrival_hour"] = pd.to_datetime(dataset.Arrival_Time).dt.hour
dataset["Arrival_min"] = pd.to_datetime(dataset.Arrival_Time).dt.minute
dataset.drop(["Arrival_Time"], axis = 1, inplace = True)

dataset.head()

dataset["Additional_Info"].describe()

#we can observe that more than 90% of the additional info is same as "no_info"
#so we can eliminate the additional info

dataset.drop(["Additional_Info"],axis=1,inplace=True)

#since we have source and destination the route column doesn't make value

dataset.drop(["Route"],axis=1,inplace=True)

dataset.head()

duration = list(dataset["Duration"])

for i in range(len(duration)):
    if len(duration[i].split()) < 2:   
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"   
        else:
            duration[i] = "0h " + duration[i]          
print(duration)
duration_hours = []
duration_mins = []
for i in range(len(duration)):
    duration_hours.append(int(duration[i].split(sep = "h")[0]))    
    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))

# Adding duration_hours and duration_mins list to train_data dataframe
dataset["Duration_hours"] = duration_hours
dataset["Duration_mins"] = duration_mins

dataset.drop(["Duration"], axis = 1, inplace = True)

dataset

#since source,destination,airlines are the nominal categorical data
#we need to perform one-hot encoding

dataset[['Airline']].value_counts()

Airline = dataset[["Airline"]]
Airline = pd.get_dummies(Airline)
Airline.head()

Airline.shape

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

dataset[['Destination']].value_counts()

Destination = dataset[["Destination"]]
Destination = pd.get_dummies(Destination)
Destination.head()

Destination.shape

dataset[['Source']].value_counts()

Source = dataset[["Source"]]
Source = pd.get_dummies(Source)
Source.head()

Source.shape

#The prices vary depends on the number of stops so the stop columns fall in ordinal data
#we need to perform label encoding for stops

dataset[['Total_Stops']].value_counts()

dict_Stops = {'non-stop':0, '1 stop':1, '2 stops':2, '3 stops':3, '4 stops':4}

dataset['Total_Stops'] = dataset['Total_Stops'].map(dict_Stops)

dataset.head()

dtrain = pd.concat([Source, Destination, dataset, Airline], axis = 1)

dtrain.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)

dtrain.head()

dtrain.shape

"""## TEST SET"""

dtest=pd.read_excel("Flight_Test_set.xlsx")

dtest.head()

dtest.shape

dtest.columns

dtest['Additional_Info'].value_counts()

dtest['Additional_Info'].count()

## of 2671 observations 2148 observations contain No info... so its better to 
## remove the additional info column

dtest.drop(['Additional_Info'],axis=1,inplace=True)
dtest.columns

## preprocessing

print("test data info")
print("-"*75)
print(dtest.info())

print()
print()

print("the null values")
print("-"*75)
dtest.dropna(inplace=True)
print(dtest.isnull().sum())

## EDA

## Date of journey
dtest['day']=pd.to_datetime(dtest['Date_of_Journey'],format="%d/%m/%Y").dt.day
dtest['month']=pd.to_datetime(dtest['Date_of_Journey'],format="%d/%m/%Y").dt.month
dtest.drop(['Date_of_Journey'],axis=1,inplace=True)

##departure time
dtest['dep_hour']=pd.to_datetime(dtest['Dep_Time']).dt.hour
dtest['dep_min']=pd.to_datetime(dtest['Dep_Time']).dt.minute
dtest.drop(['Dep_Time'],axis=1,inplace=True)

## Arrival time
dtest['Arr_hour']=pd.to_datetime(dtest['Arrival_Time']).dt.hour
dtest['Arr_min']=pd.to_datetime(dtest['Arrival_Time']).dt.minute
dtest.drop(['Arrival_Time'],axis=1,inplace=True)

## Duration
duration=list(dtest['Duration'])
dur_hr=[]
dur_min=[]

for i in range(len(duration)):
    if len(duration[i].split())!=2:
        if "h" in duration[i]:
            duration[i]=duration[i].strip()+" 0m"
        else:
            duration[i]="0h "+duration[i]

for i in range(len(duration)):
    dur_hr.append(int(duration[i].split(sep= "h")[0]))
    dur_min.append(int(duration[i].split(sep= "m")[0].split()[-1]))
    
## Adding duration hours and duration mins columns
dtest['dur_hr']=dur_hr
dtest['dur_min']=dur_min
dtest.drop(['Duration'],axis=1,inplace=True)

dtest[['Airline']].value_counts()

Airline = dtest[["Airline"]]
Airline = pd.get_dummies(Airline)
Airline.head()

Airline.shape

dtest[['Destination']].value_counts()

Destination = dtest[["Destination"]]
Destination = pd.get_dummies(Destination)
Destination.head()

Destination.shape

dtest[['Source']].value_counts()

Source = dtest[["Source"]]
Source = pd.get_dummies(Source)
Source.head()

Source.shape

## dealing with categorical data

## Route and total stops are related to each other..so remove route
dtest.drop(['Route'],axis=1,inplace=True)

## Replacing total stops
dict_Stops = {'non-stop':0, '1 stop':1, '2 stops':2, '3 stops':3, '4 stops':4}
dtest['Total_Stops'] = dtest['Total_Stops'].map(dict_Stops)

dtest.head()

test_data = pd.concat([Source, Destination, dtest, Airline], axis = 1)
test_data.drop(["Airline", "Source", "Destination"], axis = 1, inplace = True)

test_data.head()

test_data.shape

"""## Feature Selection
#### Following are some of feature selection methods:
#### 1. Heatmap
#### 2.feature_importance
#### 3.SelectKBest
"""

## dtrain -- Train data
## test_data -- Test data

dtrain.shape

dtrain.columns

x=dtrain.loc[:,['Source_Banglore', 'Source_Chennai', 'Source_Delhi', 'Source_Kolkata','Source_Mumbai',
                'Destination_Banglore', 'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi',
                'Journey_day', 'Journey_month', 'Dep_hour', 'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours', 'Duration_mins', 'Total_Stops',
                'Airline_Air Asia', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways', 'Airline_Jet Airways Business',
                'Airline_Multiple carriers', 'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet', 'Airline_Trujet', 'Airline_Vistara', 
                'Airline_Vistara Premium economy']]
x.head()

x.shape

y=dtrain['Price']
y.head()

## heatmap generation between independent and dependent variables
plt.figure(figsize = (18,18))
sns.heatmap(dataset.corr(), annot=True)

plt.show()

## important feature using ExtraTreesRegressor

from sklearn.ensemble import ExtraTreesRegressor
selection=ExtraTreesRegressor()
selection.fit(x,y)

print(selection.feature_importances_)

## graph of feature importances
plt.figure(figsize=(12,8))
feat_importances=pd.Series(selection.feature_importances_,index=x.columns)
feat_importances.nlargest(20).plot(kind='barh')
plt.show()

"""## Fitting Random Forest"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=6)

from sklearn.ensemble import RandomForestRegressor
reg_rf=RandomForestRegressor()
reg_rf.fit(x_train,y_train)

y_pred=reg_rf.predict(x_test)

reg_rf.score(x_train,y_train)

reg_rf.score(x_test,y_test)

from sklearn import metrics
print("MAE:",metrics.mean_absolute_error(y_test,y_pred))
print("MSE:",metrics.mean_squared_error(y_test,y_pred))
print("RMSE:",np.sqrt(metrics.mean_squared_error(y_test,y_pred)))

metrics.r2_score(y_test,y_pred)

"""#Neural network"""

import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

x_train.shape

# Neural network
model = Sequential()
model.add(Dense(400, input_dim= 32, activation="relu"))
model.add(Dense(200, input_dim= 400, activation="relu"))
model.add(Dense(200, input_dim= 200, activation="relu"))
model.add(Dense(1, activation="linear"))

keras.optimizers.Adam()
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
model.summary()

history = model.fit(x_train, y_train, epochs=100, batch_size=64,validation_split=0.15,validation_data=None,verbose=1)

model.predict(x_test)

y_test

x_test.head(1)

user_input=[[0,	0	,0	,1	,0	,1	,0	,0	,0	,0	,0	,6	,6	,19,	55,	22,	25,	2,	30,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]
#user_input = SSC.fit_transform(user_input)
p=model.predict(user_input)
print(p)

plt.title('Loss')
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()

"""#Tflite"""

from tensorflow import lite

# Convert Keras model to TF Lite format.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_float_model = converter.convert()

# Show model size in KBs.
float_model_size = len(tflite_float_model) / 1024
print('Float model size = %dKBs.' % float_model_size)

# Commented out IPython magic to ensure Python compatibility.
# Re-convert the model to TF Lite using quantization.
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quantized_model = converter.convert()

# Show model size in KBs.
quantized_model_size = len(tflite_quantized_model) / 1024
print('Quantized model size = %dKBs,' % quantized_model_size)
print('which is about %d%% of the float model size.'\
#       % (quantized_model_size * 100 / float_model_size))

# Save the quantized model to file to the Downloads directory
f = open('FlightFare.tflite', "wb")
f.write(tflite_quantized_model)
f.close()

# Download the digit classification model
from google.colab import files
files.download('FlightFare.tflite')

print('`FlightFare.tflite` has been downloaded')

"""#Pkl file"""

import pickle
# open a file, where you ant to store the data
file = open('flight.pkl', 'wb')

# dump information to that file
pickle.dump(reg_rf, file)

model = open('flight.pkl','rb')
rfmodel = pickle.load(model)

y_prediction=rfmodel.predict(x_test)

metrics.r2_score(y_test,y_prediction)