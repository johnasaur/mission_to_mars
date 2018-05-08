from flask import Flask, render_template, redirect
from flask_pymongo import MongoClient
from rover.scrape_mars_BS import scrape
import os


app = Flask(__name__)
url = os.environ["MONGODB_URI"]

client = MongoClient(url)
db = client["mars"]


@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def get():
    mars = db.mars
    data = scrape()
    mars.update({}, data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run()