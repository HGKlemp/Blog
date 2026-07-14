from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def read_json():
    with open("data.json", "r") as file:
        return json.load(file)


def write_json(blog_posts):
    with open("data.json", "w") as file:
        json.dump(blog_posts, file, indent=4)


@app.route("/")
def index():
    blog_posts = read_json()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        blog_posts = read_json()

        new_post = {
            "id": max((post["id"] for post in blog_posts), default=0) + 1,
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"]
        }

        blog_posts.append(new_post)
        write_json(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)