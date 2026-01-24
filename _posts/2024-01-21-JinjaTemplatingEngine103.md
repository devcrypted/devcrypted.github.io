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
title: "Pass Python Variables in HTML Template using Jinja2"
permalink: embedding-python-code-in-html-using-jinja
date: 2024-01-21 00:00 +0530
categories: ["Python Web Development"]
tags: ["Python", "Flask", "Jinja"]
image: https://img.youtube.com/vi/yva5oUk4gTw/maxresdefault.jpg
description: Python basics, including variable assignment, lists, loops, conditionals, and integrating Python with HTML to dynamically generate web content

# Variables
video_id: yva5oUk4gTw
playlist_id: PL2JBbPWIA_TqArc5Iqc6v6Y9ggL598llV
github_repo: flask-blog
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

## Covered Topics in This Video

1. Basic Variable Assignment in Python:
   - Assigning Values: The video shows how to assign a value to a variable. For example, name = "John", where name is the variable, and "John" is the assigned value.
   - Dynamic Assignment: The video briefly touches on dynamically updating the variable in the code and reflecting the change in the output.

2. Executing Python Code:
   - Running a Python Script: The video demonstrates how to run a Python script using the command python main.py.
   - Browser Integration: The output or result of running the script is shown to be integrated or updated on a web page, which is likely connected to the script via some web framework or tool.

3. Working with Lists in Python:
   - Passing a List: The concept of passing a list (e.g., names = ["Alice", "Bob", "Charlie"]) instead of a single variable is shown.
   - List Output: The video displays how the output changes when a list is used, particularly when dealing with HTML output.

4. HTML List Generation with Python:
    - Creating an Unordered List (UL): The video walks through generating an unordered list (`<ul>`) in HTML using Python.
    - Looping Through a List: A loop is created using a for loop in Python (for item in names:) to generate each list item (`<li>`) dynamically in HTML.
    - Loop Syntax: Emphasis on correct syntax, such as using end to properly close the loop in the context used.

5. Conditional Statements in Python:
    - If-Else Statements: The video covers the use of conditional statements (if, else) in Python.
    - Checking Conditions: An example is shown where a condition is checked, and based on whether it’s true or false, different outputs are generated.
    - Condition Syntax: The syntax for writing conditions and ensuring the logic is correctly executed is highlighted, with mention of using endif to properly close the condition block.

6. Upcoming Content Teaser:
    - Next Steps: The video concludes by mentioning that the next video will involve building a website from scratch, indicating a progression from basic concepts to a more advanced project.

## Explanation of Concepts

- Variable Assignment: This is the process of storing a value in a named location in memory, allowing the program to refer to this value later by the variable's name.
- Lists: A list in Python is a collection of items that can be accessed by index. It allows you to store multiple items in a single variable.
- Loops: Loops are used to repeat a block of code multiple times. In this case, the for loop iterates over each item in a list.
- HTML Unordered List: In web development, an unordered list (`<ul>`) is a way to display items in a list format with bullet points.
- Conditionals: Conditional statements allow a program to execute certain pieces of code based on whether a condition is true or false.
- Python and Web Integration: The video seems to integrate Python backend logic with HTML front-end, demonstrating how Python can be used to dynamically generate web content.
- These concepts form the foundation of both Python programming and basic web development.
