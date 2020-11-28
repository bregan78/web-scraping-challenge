from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def home():
     # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_info)


@app.route("/scrape")
def scrape():


    # Run the scrape function

    mars_info = mongo.db.mars_info
    mission = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_info.update({}, mission, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)