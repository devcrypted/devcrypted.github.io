---
layout: post
authors: ["kamal"]
media_subpath: /assets/img/posts
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
youtube_logo: <i class="fa-brands fa-youtube"></i>

# Should be changed according to post
published: true
title: "How to Use Poetry and Understand Jinja Templating Engine"
permalink: poetry-and-jinja-templates-in-flask
date: 2024-01-20 00:00 +0530
categories: ["Python Web Development"]
tags: ["Python", "Flask", "Jinja", "Poetry"]
image: https://img.youtube.com/vi/O2u_7E-XKkU/maxresdefault.jpg
description: Learn Poetry for package management in Python, separating HTML from Python code using templates, and structuring projects for cleaner, more maintainable code.

# Variables
video_id: O2u_7E-XKkU
playlist_id: PL2JBbPWIA_TqArc5Iqc6v6Y9ggL598llV
github_repo: flask-blog
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

## Brief Summary

- Introduction to Flask Routes: Recap from the last video about creating routes in Flask.
- Managing Packages with Poetry:
  - Discussed how to manage Python packages more efficiently using Poetry instead of pip.
  - Demonstrated installing Poetry and setting up a project with it.
  - Explained the benefits of using Poetry, such as managing dependencies in a single file.

- Separating HTML from Python Code:
  - Discussed why it's important to separate HTML from Python code for better organization.
  - Demonstrated creating a 'templates' folder in Flask to store HTML files separately.
  - Showed how to use the render_template function to link the HTML file with the Flask route.

- Practical Implementation:
  - Created a basic HTML template and integrated it into a Flask project.
  - Explained how to structure the project for clean and maintainable code, avoiding the mess of mixing HTML with Python.

- Running the Project:
  - Showed how to run the Flask project using Poetry and confirmed that the setup works correctly by displaying the webpage in a browser.
