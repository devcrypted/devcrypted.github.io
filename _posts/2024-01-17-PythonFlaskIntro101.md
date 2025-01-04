---
layout: post
authors: ["devcrypted"]
media_subpath: /assets/img/posts
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
youtube_logo: <i class="fa-brands fa-youtube"></i>

# Should be changed according to post
published: true
title: "Getting Started With Flask Web Framework"
permalink: getting-started-with-flask
date: 2024-01-17 00:00 +0530 
categories: ["Python Web Development"]
tags: ["Python", "Flask"]
image: https://img.youtube.com/vi/jSiWuY24Ho8/maxresdefault.jpg
description: How to get started with Flask web framework to develop modern web applications

# Variables
video_id: jSiWuY24Ho8
playlist_id: PL2JBbPWIA_TqArc5Iqc6v6Y9ggL598llV
github_repo: flask-blog
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

## Installing Python & Pip

Python is a versatile, high-level programming language known for its readability and simplicity. Pip is its package manager, enabling easy installation and management of Python libraries and dependencies.

### Install Python

Python comes preinstalled on most Linux distributions. For Windows users, follow the steps below to install Python.

1. **Download & Install Python:**
   - You can [click here](https://www.python.org/downloads/release/python-3125/) to download the Python 3.12.5 installer.

2. **Or Using Windows Package Manager:**
   - Press `Windows + R` and run the following command in the dialog box:

     ```powershell
     winget install Python.Python.3.12
     ```

3. **Verify Installation:**
   - Open `Command Prompt` and run the command:

     ```powershell
     python --version
     pip --version
     ```

   - If you see the version number without any errors, Python & Pip are successfully installed!

## Installing Flask

Flask is a lightweight and flexible Python web framework used for building web applications. Follow these steps to install Flask:

### Create a Virtual Environment (Optional)

It's recommended to create a virtual environment to isolate Flask and its dependencies from other Python projects. You can use tools like `venv` or `pipenv` for this purpose.

1. **Create a virtual environment using `poetry`:**

   - Install Poetry

      ```powershell
      pip install poetry
      ```

   - Create a folder for your project
   - Right click on folder, `Open with VS Code`. If you don't have VS code, you can simply install it from [here](https://code.visualstudio.com/Download).
   - Press `Ctrl + ~` to open a terminal.
   - Type `poetry init` and answer few project details to get started with the project
   - Now you can install flask by typing `poetry add flask`.

## Getting Started With a Basic Flask App

Create a file named `main.py` or anything of your choice, but be sure you use `.py` extension.

```python
from flask import Flask

app = Flask(__name__)

app.run()
```

The above app will work when you open your VS Code integrated terminal by pressing `Ctrl + ~` and typing `poetry run python main.py`

Once your application start, it will available locally on `http://localhost:5000`. You can open it in your favorite browser. It will give an error that the page you're trying to reach is not found. This is intentional. Let's fix it.

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
  return '<h1>Hello World!</h1>'

app.run()
```

By simply adding one function named `home` for route `/`, you can stop your server by going back to terminal and hit `Ctrl + C`.
Rerun the command `poetry run python main.py` and go back to your browser, refresh the page, you'll see `Hello World!`.
Congratulations, you have built your first Flask Hello World Application.

## Let's Create One More Route

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
  return '<h1>Hello World!</h1>'

@app.route('/dashboard')
def home():
  return '<h1>Dashboard Page</h1>'

app.run()
```

This page can be accessible at `http://localhost:5000/dashboard`.

Enough for the day, let's learn more in next lecture 🙂
