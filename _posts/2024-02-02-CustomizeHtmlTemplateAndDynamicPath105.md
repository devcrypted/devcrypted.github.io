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
published: false
title: "Customize HTML Template and Dynamic Path in Flask"
permalink: customize-html-template-and-dynamic-path-in-flask
date: 2024-02-02 00:00 +0530
categories: ["Python Web Development"]
tags: ["Python", "Flask", "HTML"]
image: https://img.youtube.com/vi/GQ1uh-ffHms/maxresdefault.jpg
description: How to get started with Flask web framework to develop modern web applications

# Variables
video_id: GQ1uh-ffHms
playlist_id: PL2JBbPWIA_TqArc5Iqc6v6Y9ggL598llV
github_repo: flask-blog
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

## Introduction

- The video focuses on customizing an HTML5 template used within a Python Flask application.
- Previous videos included downloading and using the template; this video will customize it further.

## Initial Customization

### Dashboard

- The default HTML5 template includes too many menu options.
- The goal is to simplify the menu and add branding.
- Example: Changing the header from "HTML5 UP" to "DevCrypted".

## Menu Customization

### Navigation Bar

- Remove unnecessary menu items.
- Rename "Welcome" to "Home".
- Update routes dynamically using url_for for consistency and future-proofing.

## Header and Footer Adjustments

### Header

- Replace placeholder text with actual branding.

### Footer

- Simplify the footer by removing unnecessary rows.
- Update footer links to point to GitHub instead of placeholder URLs.

## Content Customization

### Main Content

- Adjust the content displayed on the main page.
- Update static content to be dynamic, using data from Rails.
- Example: Replace hardcoded content with dynamic content using a loop.

## Dynamic Content with Rails

### Dynamic Blog List

- Implement a loop to generate a list of blog entries dynamically.
- Use variables to display blog title, subtitle, description, and thumbnail.

### Adding and Updating Blog Entries

- Demonstrate how to add new blog entries by updating the data structure in Rails.
- Example: Adding a new blog entry to the list without modifying the HTML template.

## Handling Routes

### Dynamic Routes

- Set up dynamic routes for individual blog posts.
- Implement a function to handle dynamic routing based on the blog ID.
- Ensure that the routing works correctly by verifying in the browser.

## Image Management

### Updating Images

- Change image sizes to fit the design.
- Replace placeholder images with actual content images.

## Final Adjustments

### Responsive Design

- Ensure the template is responsive and looks good on different devices.
- Verify that the hamburger menu and other responsive elements work as expected.
