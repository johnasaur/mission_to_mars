from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_new

app = Flask(__name__)

mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars 
    facts_m = scrape_mars_new.scrape()
    mars.update({}, facts_m, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
