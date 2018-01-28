from flask import Flask, render_template
import pymongo
import mission_to_mars


app = Flask(__name__)


client = pymongo.MongoClient()

db = client.mission_to_mars_db
collection = db.mars_data

#create route that renders index.HTML template
@app.route("/scrape")
def scrape():
    mars = mission_to_mars.scrape()
    db.mars_data(mars)
    db.mars_data.insert_one(mars)

    return "Scraped some data"

#create route that renders index.html templates
@app.route("/")
    def home():
        mars = list(db.mars_data.find())
        print(mars)
        return render_template("index.html", mars = mars)


if __name__=="__main__"
    app.run(debug=True)