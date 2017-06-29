from flask import *
import mlab
from mongoengine import *

app = Flask(__name__)
mlab.connect()

class Flower(Document):
    image = StringField()
    title = StringField()
    price = FloatField()

flower1 = Flower(image="https://www.vitacost.com/blog/wp-content/uploads/2016/05/Why-You-Need-More-Lavender-in-Your-Life-e1462955823730.jpg",
                 title="Lavender",
                 price=50000)

# flower1.save()

image = "https://www.vitacost.com/blog/wp-content/uploads/2016/05/Why-You-Need-More-Lavender-in-Your-Life-e1462955823730.jpg"
title = "Lavender"
price = 50000

flowers = [
    {
        "image": "http://www.emoji.co.uk/files/emoji-one/animals-nature-emoji-one/1542-rose.png",
        "title": "Red Rose",
        "price": 10000
    },
    {
        "image": "http://www.carithers.com/images/pageMakerImages/Tulip211061674409.jpg",
        "title": "Tulip",
        "price": 20000
    },
    {
        "image": "https://www.vitacost.com/blog/wp-content/uploads/2016/05/Why-You-Need-More-Lavender-in-Your-Life-e1462955823730.jpg",
        "title": "Lavender",
        "price": 50000
    }
]

@app.route('/add-flower', methods=["GET"])
def add_flower():
    return render_template("add_flower.html")

@app.route('/')
def index():
    return render_template("index.html", flowers=Flower.objects())


@app.route('/about')
def about():
    return "Welcome"

if __name__ == '__main__':
    app.run()
