from flask import *
import mlab
import os
from mongoengine import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
mlab.connect()

app.config["IMG_PATH"] = os.path.join(app.root_path, "images")
app.secret_key = "hahaha"

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



@app.route("/images/<image_name>")
def images(image_name):
    return send_from_directory(app.config["IMG_PATH"], image_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]

        if username == "admin" and password == "admin":
            #Valid credentials
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            #Invalid credentials
            return "Invalid credentials"


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


@app.route('/add-flower', methods=["GET", "POST"])
def add_flower():
    if "logged_in" in session and session["logged_in"]:
        if request.method == "GET": #FORM Requested
            return render_template("add_flower.html")
        elif request.method == "POST": #User submitted FORM
            #1: Get data (title, image, price)
            form = request.form
            title = form["price"]
            # image = form["image"]
            price = form["price"]

            image = request.files["image"]

            filename = secure_filename(image.filename)

            image.save(os.path.join(app.config["IMG_PATH"], filename))

            #2: Save data into database
            new_flower = Flower(title = title,
                                image = "/images/{0}".format(filename),
                                price = price)
            new_flower.save()

            return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))


@app.route('/')
def index():
    return render_template("index.html", flowers=Flower.objects())


@app.route('/about')
def about():
    return "Welcome"

if __name__ == '__main__':
    app.run()

