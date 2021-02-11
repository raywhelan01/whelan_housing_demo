# Import the dependencies.
import pandas as pd
import json
import pandas.io.json as pd_json
import censusdata
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,OneHotEncoder

import pickle
#import xgboost as xgb

# Import the requests library.
import requests

api_key = "24f7bba880a1af36816cec59796a7e4f07da5789"

# Import ACS Data Profile variables
dp_var_url = "https://api.census.gov/data/2018/acs/acs5/profile/variables.json"
dp_acs_vars = requests.get(dp_var_url).json()
dp_acs_vars = dp_acs_vars["variables"]

dp_vars_df = pd.DataFrame.from_dict(dp_acs_vars, orient = 'index')
dp_vars_df.index.name = 'code'

#Import ACS Detail variables
b_var_url = "https://api.census.gov/data/2018/acs/acs5/variables.json"
b_acs_vars = requests.get(b_var_url).json()
b_acs_vars = b_acs_vars["variables"]

b_vars_df = pd.DataFrame.from_dict(b_acs_vars, orient = 'index')
b_vars_df.index.name = 'code'

# URL for ACS Data Profile call
dp_var_list = ["DP02_0122E", "DP02_0001E", "DP02_0015E", "DP03_0001E", "DP03_0005PE",
               "DP04_0001E", "DP04_0050E"]

dp_url_start = "https://api.census.gov/data/2018/acs/acs5/profile?get=NAME"
dp_url_end =  "&for=county:*&in=state:*&key=" + api_key

dp_url = dp_url_start

for var in dp_var_list:
    dp_url = dp_url + ',' + var

dp_url = dp_url + dp_url_end

print(dp_url)

# URL for ACS Detail call
b_var_list = ["B01001_001E", "B01002_001E","B06001_013E","B06009_002E","B06009_003E","B06009_004E","B06009_005E","B06009_006E",
              "B06012_002E","B08133_001E","B19013_001E","B19301_001E","B19326_001E","B25071_001E",
              "B25077_001E"]

b_url_start = "https://api.census.gov/data/2018/acs/acs5?get=NAME"
b_url_end =  "&for=county:*&in=state:*&key=" + api_key

b_url = b_url_start

for var in b_var_list:
    b_url = b_url + ',' + var

b_url = b_url + b_url_end

print(b_url)

#Print variable code names
dp_codes = []
b_codes = []

for var in dp_var_list:
    dp_codes.append(dp_vars_df.loc[var, 'label'])

for var in b_var_list:
    b_codes.append(b_vars_df.loc[var, 'label'])
    
print(dp_codes, b_codes)

codes_dict = {'code' : dp_var_list + b_var_list, 'label' : dp_codes + b_codes}
codes_df = pd.DataFrame(data = codes_dict)
codes_df

# Request the Data Profile table
dp_call = requests.get(dp_url).json()
dp_df = pd.DataFrame(dp_call[1:len(dp_call)], columns = dp_call[0], dtype = float)

# Request the Detail table
b_call = requests.get(b_url).json()
b_df = pd.DataFrame(b_call[1:len(b_call)], columns = b_call[0], dtype = float)

# Merge the ACS tables
acs_df = dp_df.merge(b_df, left_on = ['NAME', 'state', 'county'], right_on = ['NAME', 'state', 'county'])

acs_df= acs_df.astype({'state': 'object', 'county':'object'})
acs_df['fips'] = acs_df['state']*1000 + acs_df['county']

acs_df["% Housing Units Occupied"] = acs_df["DP02_0001E"]/acs_df["DP04_0001E"]
acs_df["% Unemployment Rate"] = acs_df["DP03_0005PE"]/100
acs_df["% Born in State"] = acs_df["B06001_013E"]/acs_df["B01001_001E"]
acs_df["% <HS"] = acs_df["B06009_002E"]/acs_df["B01001_001E"]
acs_df["% HS Grad"] = acs_df["B06009_003E"]/acs_df["B01001_001E"]
acs_df["% Some College"] = acs_df["B06009_004E"]/acs_df["B01001_001E"]
acs_df["% Bach Degree"] = acs_df["B06009_005E"]/acs_df["B01001_001E"]
acs_df["% Grad Degree"] = acs_df["B06009_006E"]/acs_df["B01001_001E"]
acs_df["% Below Pov Level"] = acs_df["B06012_002E"]/acs_df["B01001_001E"]
acs_df["Commute Time"] = acs_df["B08133_001E"]
acs_df["Median Income"] = acs_df["B19326_001E"]
acs_df["Median Home Value"] = acs_df["B25077_001E"]

model_df = acs_df[["state", "% Housing Units Occupied", "% Unemployment Rate", "% Born in State", "% <HS", "% HS Grad",
                  "% Some College", "% Bach Degree", "% Grad Degree", "% Below Pov Level", "Commute Time", "Median Income", "Median Home Value"]]

model_df = model_df.dropna()
model_df = pd.get_dummies(model_df)

# Split our preprocessed data into our features and target arrays
y = model_df["Median Home Value"]
X = model_df.drop(["Median Home Value"],1)

# Split the preprocessed data into a training and testing dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=78)

# Train the Logistic Regression model using the resampled data
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 50, random_state=0)
regressor.fit(X_train, y_train)

# Calculate the R^2 Score score
from sklearn.metrics import r2_score
y_pred = regressor.predict(X_test)
print("R^2 Score")
r2_score(y_test, y_pred)

#Explained variance score
from sklearn.metrics import explained_variance_score
print("Explained variance")
explained_variance_score(y_test, y_pred)

with open('housing_regressor.pkl', 'wb') as file:
    pickle.dump(regressor, file)