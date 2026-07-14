import json

def read_json():
    with open('data.json', 'r') as f:
        return json.load(f)
blog_posts = read_json()
print(blog_posts)