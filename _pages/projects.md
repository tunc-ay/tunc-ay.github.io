---
layout: splash
title: "Portfolio"
permalink: /projects/
header:
  overlay_color: "#1f3a5f"
excerpt: "Documenting user guide and datasheet for MCUs and writing tutorials, API documentation, conceptual explanations, and hardware guides."

api:
  - image_path: /assets/images/projects/api-overview.png
    alt: "API Overview"
    title: "API Overview"
    excerpt: "Introduction to the Invicti REST API, published on Invicti's support site."
    url: "https://www.invicti.com/support/api-overview/"
    btn_label: "Read"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/api-examples.png
    alt: "API documentation examples"
    title: "API Documentation Examples"
    excerpt: "Sample developer documentation I wrote, hosted on GitHub."
    url: "https://github.com/tunc-ay/developer-documentation"
    btn_label: "View on GitHub"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/fthr-board.png
    alt: "MAX32690 FTHR board documentation"
    title: "FTHR Board Documentation"
    excerpt: "Evaluation kit documentation for the MAX32690 FTHR microcontroller board."
    url: "https://developer.analog.com/api/media/file/2026-02-16-max32690fthr-evkit-27y1ty.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"

guides:
  - image_path: /assets/images/projects/step-by-step.png
    alt: "Installing Authentication Verifier Agents"
    title: "Step-by-step Guide"
    excerpt: "Task-based instructions for installing and configuring authentication verifier agents."
    url: "/assets/projects/InstallingAuthVerifier.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/quick-start.png
    alt: "Quick Start Guide"
    title: "Quick Start Guide"
    excerpt: "Onboarding guide that takes new users from first login to their first scan report."
    url: "/assets/projects/QuickStartGuide.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - image_path: /assets/images/projects/severity-levels.png
    alt: "Vulnerability Severity Levels"
    title: "Explanation-type Document"
    excerpt: "Conceptual article explaining vulnerability severity levels and how they help teams prioritize fixes."
    url: "/assets/projects/VulnerabilitySeverityLevels.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"

mcu:
  - title: "MAX32690 Datasheet"
    excerpt: "Datasheet for the MAX32690 Arm Cortex-M4 microcontroller with Bluetooth LE 5. [Product page](https://www.analog.com/en/products/max32690.html)"
    url: "https://www.analog.com/media/en/technical-documentation/data-sheets/max32690.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - title: "MAX32690 User Guide"
    excerpt: "User guide for the MAX32690 microcontroller. [Product page](https://www.analog.com/en/products/max32690.html)"
    url: "https://www.analog.com/media/en/technical-documentation/user-guides/ug7618.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - title: "MAX32675C User Guide"
    excerpt: "User guide for the MAX32675C ultra-low-power microcontroller. [Product page](https://www.analog.com/en/products/max32675c.html)"
    url: "https://www.analog.com/media/en/technical-documentation/user-guides/max32675c-user-guide.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
  - title: "MAX32657 User Guide"
    excerpt: "Documentation for the MAX32657 microcontroller. [Product page](https://www.analog.com/en/products/max32657.html)"
    url: "https://www.analog.com/media/en/technical-documentation/data-sheets/max32657.pdf"
    btn_label: "Read (PDF)"
    btn_class: "btn--primary"
---

<h2 class="section-title">Microcontroller datasheets and user guides</h2>

{% include feature_row id="mcu" %}

<h2 class="section-title">API and hardware documentation</h2>

{% include feature_row id="api" %}

<h2 class="section-title">Guides and explanations</h2>

{% include feature_row id="guides" %}
