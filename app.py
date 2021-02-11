#imports
from flask import Flask, render_template, request
import pickle
import pandas as pd
import sys
#import sklearn

# Use pickle to load in the pre-trained model.
with open(f'machine_learning/housing_regressor.pkl', 'rb') as f:
    model = pickle.load(f)

#import our county housing data set
data = pd.read_csv('machine_learning/counties.csv')


#Set up Flask
app = Flask(__name__)

#Set up app routes
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        #Create our default table
        default = data.loc[data['fips']== 6081]
        default = default[["NAME", "% Housing Units Occupied", "% Unemployment Rate", "% Born in State", "Median Income", "Median Home Value"]]
        default.set_index(['NAME'], inplace=True)
        default.index.name=None
        default = default.rename(columns={"% Housing Units Occupied": "Housing Unit Occupancy Rate", "% Unemployment Rate": "Unemployment Rate", "% Born in State": "Native to State Residency Rate"})

        default["Housing Unit Occupancy Rate"] = default["Housing Unit Occupancy Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        default["Unemployment Rate"] = default["Unemployment Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        default["Native to State Residency Rate"] = default["Native to State Residency Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        default["Median Income"] = default["Median Income"].to_string(float_format ='${:,.2f}'.format, index = False)
        default["Median Home Value"] = default["Median Home Value"].to_string(float_format ='${:,.2f}'.format, index = False)



        print(default, file=sys.stderr)

        return render_template("index.html", tables = [default.to_html(classes='bg-dark')], titles = ['na', "Real Values"])

    if request.method == 'POST':
        #Extract the input
        try:
            fips = int(request.form['fips'])
        except ValueError:
            fips = 6081
        occup = int(request.form['occup'])/100 + 1
        unemp = int(request.form['unemp'])/100 + 1
        inState = int(request.form['inState'])/100 + 1
        medInc = int(request.form['medInc'])/100 + 1

        real = data.loc[data['fips'] == fips]

        if len(real) == 0:
            real = data.loc[data['fips']== 6081]

        hypo = real.copy()
        hypo["% Housing Units Occupied"] = hypo["% Housing Units Occupied"]*occup
        hypo["% Unemployment Rate"] = hypo["% Unemployment Rate"]*unemp
        hypo["% Born in State"] = hypo["% Born in State"]*inState
        hypo["Median Income"] = hypo["Median Income"]*medInc


        real_drop = real.drop(columns = ["NAME", "fips", "Median Home Value"])
        hypo_drop = hypo.drop(columns = ["NAME", "fips", "Median Home Value"])

        print(len(real.columns))
        print(len(real_drop.columns))
        
        predicted_real = model.predict(real_drop)
        predicted_hypo = model.predict(hypo_drop)

        print(predicted_real, file=sys.stderr)
        print(predicted_hypo, file=sys.stderr)

        hypo["Median Home Value"] = hypo["Median Home Value"] * (predicted_hypo/predicted_real)


        real = real[["NAME", "% Housing Units Occupied", "% Unemployment Rate", "% Born in State", "Median Income", "Median Home Value"]]
        real.set_index(['NAME'], inplace=True)
        real.index.name=None
        real = real.rename(columns={"% Housing Units Occupied": "Housing Unit Occupancy Rate", "% Unemployment Rate": "Unemployment Rate", "% Born in State": "Native to State Residency Rate"})
        
        real["Housing Unit Occupancy Rate"] = real["Housing Unit Occupancy Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        real["Unemployment Rate"] = real["Unemployment Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        real["Native to State Residency Rate"] = real["Native to State Residency Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        real["Median Income"] = real["Median Income"].to_string(float_format ='${:,.2f}'.format, index = False)
        real["Median Home Value"] = real["Median Home Value"].to_string(float_format ='${:,.2f}'.format, index = False)
        
        
        print(real, file=sys.stderr)

        hypo = hypo[["NAME", "% Housing Units Occupied", "% Unemployment Rate", "% Born in State", "Median Income", "Median Home Value"]]
        hypo.set_index(['NAME'], inplace=True)
        hypo.index.name=None
        hypo = hypo.rename(columns={"% Housing Units Occupied": "Housing Unit Occupancy Rate", "% Unemployment Rate": "Unemployment Rate", "% Born in State": "Native to State Residency Rate"})

        hypo["Housing Unit Occupancy Rate"] = hypo["Housing Unit Occupancy Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        hypo["Unemployment Rate"] = hypo["Unemployment Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        hypo["Native to State Residency Rate"] = hypo["Native to State Residency Rate"].to_string(float_format ='{:,.2%}'.format, index = False)
        hypo["Median Income"] = hypo["Median Income"].to_string(float_format ='${:,.2f}'.format, index = False)
        hypo["Median Home Value"] = hypo["Median Home Value"].to_string(float_format ='${:,.2f}'.format, index = False)


        return render_template('index.html', tables = [real.to_html(classes='bg-dark'), hypo.to_html(classes='bg-dark')], titles = ['na', "Real Values", "Hypothetical Values"])

if __name__ == '__main__':
    app.run()