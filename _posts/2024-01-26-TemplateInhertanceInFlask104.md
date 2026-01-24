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
title: "Customize HTML Template and Template Inheritance using Jinja"
permalink: customize-html-template-and-inheritance-using-jinja
date: 2024-01-26 00:00 +0530
categories: ["Python Web Development"]
tags: ["Python", "Flask", "Jinja"]
image: https://img.youtube.com/vi/8OOH_uKnW6U/maxresdefault.jpg
description: Setting up a Flask project, organizing files, using template inheritance for reusable layouts, and linking static assets, with plans to add more features in future tutorials.

# Variables
video_id: 8OOH_uKnW6U
playlist_id: PL2JBbPWIA_TqArc5Iqc6v6Y9ggL598llV
github_repo: flask-blog
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

#### Project Setup

- The video begins by setting up a Flask web project.
- An HTML5 template is downloaded and placed in the project's folder.
- The project structure includes folders for templates (HTML files) and static files (CSS, JavaScript, images).

#### Folder and File Organization

- A templates folder is created to store HTML files, following Flask’s convention.
- A static folder is created to hold static assets like CSS, JavaScript, and images.
- The video shows how to extract the downloaded template and place the relevant files in the correct folders.

#### Basic Flask Application Setup

- A main.py file is created to initialize a Flask application.
- The Flask app is set up to run in debug mode, allowing for automatic reloading when changes are made.
- The root route (/) is defined to serve the main HTML file (index.htm).

#### Handling Static Files

- Paths to CSS and JavaScript files are updated to reflect their new location in the static folder.
- Flask’s url_for function is used to dynamically generate paths for static files, ensuring that the app can locate them correctly.

#### Template Inheritance

- The concept of template inheritance is introduced.
- A base template (base.html) is created, containing the common structure like the header and footer.
- The index.htm file is modified to extend the base template and define a block for the main content.
- This approach allows reusing the header and footer across multiple pages without duplication.

#### Testing and Debugging

- The video demonstrates running the Flask server and accessing the application through a browser.
- Common issues, like missing images (due to file deletions), are highlighted and resolved.
- The importance of correctly linking CSS and JavaScript files is emphasized.

#### Future Proofing with Dynamic Paths

- Dynamic path generation is encouraged using Flask’s url_for, making it easier to handle future changes.
- The video shows how to update paths in HTML files for better maintainability.

#### Adding Additional Pages

- The video briefly touches on adding new pages to the Flask app.
- A new route (/dashboard) is created to serve a different template, demonstrating the flexibility of the setup.

#### Extending the Base Template

- The video explains how to extend the base template for new pages by defining content blocks.
- This method ensures that all pages have a consistent look and feel with the same header and footer.

#### Next Steps and Future Content

- The video concludes by mentioning plans for the next tutorial.
- The upcoming content will focus on removing unwanted elements from the template and setting up a blogging dashboard where all blog posts will be displayed.

#### Recommendations

- Viewers are encouraged to experiment with different templates to gain a better understanding.
- The importance of practicing with various templates for a deeper grasp of Flask and web development is highlighted.
