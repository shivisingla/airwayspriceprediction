#!python3
from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("flight.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        input = [[0 for i in range(32)]]
        
        #['Source_Banglore', 'Source_Chennai', 'Source_Delhi', 'Source_Kolkata','Source_Mumbai', 'Destination_Banglore', 
        #'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad', 'Destination_Kolkata', 'Destination_New Delhi', 
        #'Journey_day', 'Journey_month', 'Dep_hour', 'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours', 'Duration_mins',
        #'Total_Stops','Airline_Air Asia', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo', 'Airline_Jet Airways', 
        #'Airline_Jet Airways Business', 'Airline_Multiple carriers', 'Airline_Multiple carriers Premium economy', 
        #'Airline_SpiceJet', 'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy']
        
        # Source
        s_prev = 0
        Source = request.form["Source"]
        if (Source == 'Banglore'):
            input[0][s_prev] = 0
            input[0][0] = 1
            s_prev = 0
            
        elif (Source == 'Chennai'):
            input[0][s_prev] = 0
            input[0][1] = 1
            s_prev = 1
            
        elif (Source == 'Delhi'):
            input[0][s_prev] = 0
            input[0][2] = 1
            s_prev = 2

        elif (Source == 'Kolkata'):
            input[0][s_prev] = 0
            input[0][3] = 1
            s_prev = 3

        elif (Source == 'Mumbai'):
            input[0][s_prev] = 0
            input[0][4] = 1
            s_prev = 4

        else:
            input[0][s_prev] = 0


        # Destination
        d_prev=5
        Source = request.form["Destination"]
        if (Source == 'Bangalore'):
            input[0][d_prev] = 0
            input[0][5] = 1
            d_prev = 5
            
        elif (Source == 'Cochin'):
            input[0][d_prev] = 0
            input[0][6] = 1
            d_prev = 6
        
        elif (Source == 'Delhi'):
            input[0][d_prev] = 0
            input[0][7] = 1
            d_prev = 7
            
        elif (Source == 'Hyderabad'):
            input[0][d_prev] = 0
            input[0][8] = 1
            d_prev = 8
            
        elif (Source == 'Kolkata'):
            input[0][d_prev] = 0
            input[0][9] = 1
            d_prev = 9
            
        elif (Source == 'New_Delhi'):
            input[0][d_prev] = 0
            input[0][10] = 1
            d_prev = 10
        
        else:
            input[0][d_prev] = 0
            
        
        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        input[0][11] = Journey_day
        input[0][12] = Journey_month

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        input[0][13] = Dep_hour
        input[0][14] = Dep_min

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arr_day = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").day)
        Arr_month = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").month)
        
        Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        input[0][15] = Arrival_hour
        input[0][16] = Arrival_min
        
        
        # Duration
        dur = (Arrival_hour*60 + Arrival_min) - (Dep_hour*60 + Dep_min)
        if dur<0 and  (Arr_month<Journey_month or ((Arr_month==Journey_month) and (Arr_day<Journey_day))):
            return render_template('index.html',prediction_text="Recheck your Arrival and Departure time")
        dur_hour = dur//60
        dur_min = dur%60
        input[0][17] = dur_hour
        input[0][18] = dur_min

        # Total Stops
        Total_stops = int(request.form["stops"])
        input[0][19] = Total_stops
        
        
        
        # Airline
        a_prev = 20
        airline=request.form['airline']
        if(airline=='Air Asia'):
            input[0][a_prev] = 0
            input[0][20] = 1
            a_prev = 20
            
        elif (airline=='Air India'):
            input[0][a_prev] = 0
            input[0][21] = 1
            a_prev = 21
            
        elif (airline=='GoAir'):
            input[0][a_prev] = 0
            input[0][22] = 1
            a_prev = 22
            
        elif (airline=='IndiGo'):
            input[0][a_prev] = 0
            input[0][23] = 1
            a_prev = 23
            
        elif(airline=='Jet Airways'):
            input[0][a_prev] = 0
            input[0][24] = 1
            a_prev = 24

        elif (airline=='Jet Airways Business'):
            input[0][a_prev] = 0
            input[0][25] = 1
            a_prev = 25
            
        elif (airline=='Multiple carriers'):
            input[0][a_prev] = 0
            input[0][26] = 1
            a_prev = 26
            
        elif (airline=='Multiple carriers Premium economy'):
            input[0][a_prev] = 0
            input[0][27] = 1
            a_prev = 27
            
        elif (airline=='SpiceJet'):
            input[0][a_prev] = 0
            input[0][28] = 1
            a_prev = 28
            
        elif (airline=='Trujet'):
            input[0][a_prev] = 0
            input[0][29] = 1
            a_prev = 29
            
        elif (airline=='Vistara'):
            input[0][a_prev] = 0
            input[0][30] = 1
            a_prev = 30

        elif (airline=='Vistara Premium economy'):
            input[0][a_prev] = 0
            input[0][31] = 1
            a_prev = 31
            
        else:
            input[0][a_prev] = 0
            
        
        prediction=model.predict(input)

        output=round(prediction[0],2)

        return render_template('index.html',prediction_text="Your estimated Flight fare is Rs. {}".format(output))


    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)


