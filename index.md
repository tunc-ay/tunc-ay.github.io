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
    excerpt: >-
      I'm a **lead technical writer** at Analog Devices. I write software documentation,
      REST API references, and user guides. Before technical writing I was a journalist and editor,
      and I still write the same way: start with what the reader needs.
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
