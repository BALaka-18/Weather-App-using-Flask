from flask import Flask, render_template,request
import requests
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Creating a configuration value for the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

# Instantiating SQLAlchemy
db = SQLAlchemy(app)

# Class to define table inside database
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # City id, PRIMARY KEY
    name = db.Column(db.String(50), nullable=False) # City name, NOT NULL 



@app.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        # Get city name from form and add it to the database for further work(i.e, fetching the info etc.)
        input_city = request.form.get('city')

        # If user has provided input, work. Else, idle.
        if input_city:
            city_obj_db = City(name=input_city)
            db.session.add(city_obj_db)
            db.session.commit()

        # Variable to hold all the cities. Type : Query.
        cities = City.query.all()
        # Weather API
        url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9ba31528eac7a1f98a007ffa70f9aed1"  

        # city = "Kolkata"
        # List to hold weather data for all cities we'll loop through
        w_data = []
        # Loop over the cities inside 'cities' variable, to get info of all cities
        for city in cities:
        
            r = requests.get(url.format(city.name)).json()
            # print(r)

            # Create dictionary to hold specific weather features
            weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['main'],
                'icon' : r['weather'][0]['icon'],
            }
            w_data.append(weather)       # Append the weather for that particular city to the list

            # print(weather)

        return render_template('index.html', w_data = w_data)    #= w_data
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


