---
layout: home
title: Welcome
---

I'm Tuncay Kayaoglu, a technical writer specializing in software documentation, API documentation, and user guides. Experienced in creating clear, concise, and user-friendly documentation.

## Featured Work
- [Project Documentation](/projects)
- [About Me](/about)
- [Contact](/contact)

## Recent Posts
{% for post in site.posts limit:3 %}
* [{{ post.title }}]({{ post.url | relative_url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}