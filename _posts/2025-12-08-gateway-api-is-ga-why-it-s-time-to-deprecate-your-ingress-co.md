---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">
  <channel>
    <title>{{ site.title | xml_escape }}</title>
    <description>{{ site.description | xml_escape }}</description>
    <link>{{ site.url }}</link>
    <atom:link href="{{ site.url }}/feed.xml" rel="self" type="application/rss+xml"/>
    <pubDate>{{ site.time | date_to_rfc822 }}</pubDate>
    <lastBuildDate>{{ site.time | date_to_rfc822 }}</lastBuildDate>
    <generator>Jekyll</generator>
    {% for post in site.posts limit:10 %}
      <item>
        <title>{{ post.title | xml_escape }}</title>
        <description>{{ post.excerpt | strip_html | xml_escape }}</description>
        <pubDate>{{ post.date | date_to_rfc822 }}</pubDate>
        <link>{{ site.url }}{{ post.url }}</link>
        <guid isPermaLink="true">{{ site.url }}{{ post.url }}</guid>
        
        {% comment %} --- LOGIC START: Handle Image URL Construction --- {% endcomment %}
        
        {% comment %} 1. Get the image filename (supports string or object format) {% endcomment %}
        {% assign post_image = post.image.path | default: post.image %}

        {% if post_image %}
          {% comment %} 2. Check if it's already an absolute URL (e.g. external image) {% endcomment %}
          {% if post_image contains "://" %}
            {% assign final_image_url = post_image %}
          
          {% else %}
            {% comment %} 3. Start with site URL {% endcomment %}
            {% assign final_image_url = site.url %}

            {% comment %} 4. Append media_subpath if it exists (e.g. /assets/img) {% endcomment %}
            {% if post.media_subpath %}
              {% assign final_image_url = final_image_url | append: post.media_subpath %}
            {% endif %}

            {% comment %} 5. Append the image filename (adding a slash to be safe) {% endcomment %}
            {% assign final_image_url = final_image_url | append: "/" | append: post_image %}
          {% endif %}

          <media:content url="{{ final_image_url }}" medium="image" />
        {% endif %}
        {% comment %} --- LOGIC END --- {% endcomment %}
        
      </item>
    {% endfor %}
  </channel>
</rss>
