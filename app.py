#imports
from flask import Flask, render_template
import pickle
#import sklearn

# Use pickle to load in the pre-trained model.
#with open(f'machine_learning/housing_regressor.pkl', 'rb') as f:
#    model = pickle.load(f)


#Set up Flask
app = Flask(__name__)

#Set up app routes
@app.route("/")
def index():
   return render_template("index.html")

if __name__ == '__main__':
    app.run()