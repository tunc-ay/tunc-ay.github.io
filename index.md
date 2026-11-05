---
layout: splash
title: "Tuncay Kayaoglu"
header:
  overlay_color: "#1f3a5f"
  actions:
    - label: "View portfolio"
      url: "/projects/"
    - label: "Contact me"
      url: "/contact.html"
excerpt: "Lead Technical Writer. Clear, concise documentation for complex software and hardware."

intro:
  - image_path: /assets/images/profile.jpg
    alt: "Photo of Tuncay Kayaoglu"
    title: "Hello, I'm Tuncay"
    excerpt: |-
      I’m a Lead Technical Writer at Analog Devices, where I’ve been documenting microcontrollers since June 2023. I’ve worked on products including the MAX32690, MAX32675C, and MAX32657/MAX32658, translating complex engineering information into documentation that helps people understand and use the technology.

      My work goes beyond individual products. I create onboarding resources for new team members, manage our Jira/Confluence content, improve documentation workflows, and explore how AI and automation can make technical writing more efficient and scalable. I’m also passionate about knowledge sharing and finding better ways for technical writers to collaborate.

      Before moving into technical writing, I worked as a journalist and editor. That background still shapes how I approach documentation today: start with the reader, understand what they need, and make the complex clear.
    url: "/about/"
    btn_label: "More about me"
    btn_class: "btn--primary"

featured:
  - image_path: /assets/images/projects/api-overview.png
    alt: "API Overview"
    title: "API Overview"
    excerpt: "Introduction to the Invicti REST API, published on Invicti's support site."
    url: "https://www.invicti.com/support/api-overview/"
    btn_label: "Read"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/quick-start.png
    alt: "Quick Start Guide"
    title: "Quick Start Guide"
    excerpt: "Onboarding guide that takes new users from first login to their first scan report."
    url: "/assets/projects/QuickStartGuide.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/step-by-step.png
    alt: "Installing Authentication Verifier Agents"
    title: "Step-by-step Guide"
    excerpt: "Task-based instructions for installing and configuring authentication verifier agents."
    url: "/assets/projects/InstallingAuthVerifier.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
---

{% include feature_row id="intro" type="left" %}

<h2 class="section-title">Featured work</h2>

{% include feature_row id="featured" %}

<p class="section-cta"><a href="/projects/" class="btn btn--inverse btn--large">See the full portfolio</a></p>
