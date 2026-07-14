from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def read_json():
    with open("data.json", "r") as file:
        return json.load(file)


def write_json(blog_posts):
    with open("data.json", "w") as file:
        json.dump(blog_posts, file, indent=4)


def fetch_post_by_id(post_id):
    blog_posts = read_json()

    for post in blog_posts:
        if post["id"] == post_id:
            return post

    return None


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

    return render_template("add.html", post=None)


@app.route("/delete/<int:post_id>")
def delete(post_id):
    blog_posts = read_json()

    for post in blog_posts:
        if post["id"] == post_id:
            blog_posts.remove(post)
            break

    write_json(blog_posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        blog_posts = read_json()

        for blog_post in blog_posts:
            if blog_post["id"] == post_id:
                blog_post["author"] = request.form["author"]
                blog_post["title"] = request.form["title"]
                blog_post["content"] = request.form["content"]
                break

        write_json(blog_posts)

        return redirect(url_for("index"))

    return render_template("add.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)