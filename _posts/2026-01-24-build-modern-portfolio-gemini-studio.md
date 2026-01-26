---
layout: post
authors:
- kamal
pin: false
mermaid: true
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: "Build a Modern Portfolio with Gemini Studio & React (In Minutes)"
permalink: build-modern-portfolio-gemini-studio-react
media_subpath: /assets/img
date: 2026-01-24 13:54:24 +0000
categories:
- Development
tags:
- portfolio-website
- gemini-studio
- react
- frontend-development
- ai-tools
image: build-modern-portfolio-gemini-studio-react.png
description: Master building a dynamic portfolio website using Gemini Studio and React TypeScript. Follow our detailed guide to set up, integrate, and deploy your professional online presence.
video_id: ''
playlist_id: ''
github_repo: ''
---

Stop building static portfolios from scratch. In this guide, we'll use **Google's Gemini Studio** to act as a Senior Frontend Architect and generate a production-ready, highly-polished React portfolio for you—completely free.

We will go from **PDF Resume -> Live Website** in 4 simple steps.

## 1️⃣ Preparation

Before we start, make sure you have these ready:

1. **Your Resume**: Download your [LinkedIn](https://linkedin.com) profile as a PDF (found under the 'Resources' button on your profile) or use your standard resume PDF.
2. **Google Account**: For [Google AI Studio](https://aistudio.google.com/).
3. **GitHub Account**: To store your code on [GitHub](https://github.com/).
4. **Vercel Account**: To host your website for free on [Vercel](https://vercel.com/).

---

## 2️⃣ The Brain (Gemini Setup)

We need to teach Gemini to be an expert developer.

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Create a **New Chat Prompt**.
3. On the left, locate the **System Instructions** box. This is where we define the "Rules".

**Copy and paste this into System Instructions:**

```md
# Role
Act as a Senior Frontend Architect. Your goal is to generate production-grade, maintainable, and strictly typed React code.

# Tech Stack
- Core: React (Functional Components) + TypeScript.
- Styling: Tailwind CSS (Mobile-first).
- Icons: Lucide-React.
- Animations: Framer Motion, or more (Smooth, premium feel, scroll-triggered too).

# Rules
1.  **Mobile-First & All-Device Ready**: Prioritize mobile screens first, but ensure perfect rendering on tablets and 4K desktops.
2.  **Architecture & Maintenance**: Separate content (`data.ts`) from UI components. Code must be clean, strictly typed (Interfaces), and include a maintenance `README.md`.
3.  **Premium UX**: Use a consistent design system (Glassmorphism/Neo-Brutalism) with Framer Motion for smooth page transitions and navigation.
4.  **Production Ready**: Code must be optimized for performance and include `vercel.json` for deployment.
5.  **Output**: Provide full, well-commented file contents.
```

---

## 3️⃣ The Content (User Prompt)

Now, we give Gemini your specific data.

1. In the main chat window, click the **(+)** button to attach your **Resume PDF**.
2. **Copy and paste this prompt below** (fill in your email for the contact form):

```md
# Project: Modern Portfolio Generator

## 1. User Data
- Resume: [Attached]
- Target Audience: Recruiters & Clients
- Contact Email Web3Forms Token: [Get free token from web3forms.com] (Optional, or just use email)

## 2. Requirements
Create a single-page React portfolio with these sections:
1.  **Hero**: Impactful introduction.
2.  **Stack**: Grid of skills/technologies.
3.  **Projects**: Interactive cards with hover effects.
4.  **Experience**: Vertical timeline.
5.  **Contact**: Simple yet animatedform.

## 3. Design Directive
Pick a unique modern style (e.g., Glassmorphism or deep gradients). Make it look premium.
Ensure all text content is extracted into a generated `content/index.ts` file so I can edit it easily later.

**Action**: Generate the file structure and code now.
```

*Hit **Run**. Gemini will analyze your resume- [x] Refine blog post rules to be more concise

- [x] Add links to preparation step
bsite.*

---

## 4️⃣ Export & Go Live

Once Gemini generates the code, you will see a preview or file list.

1. **Export to GitHub**: inside AI Studio, look for the **Export** or **Share** icon (often top right) and select **Export to GitHub**.
    - Authorize GitHub if asked.
    - Create a new repository (e.g., `my-ai-portfolio`).
2. **Deploy on Vercel**:
    - Go to [Vercel.com](https://vercel.com) and log in.
    - Click **Add New... > Project**.
    - Import your new `my-ai-portfolio` repository.
    - Click **Deploy**.

**That's it!** Vercel will build your site and give you a live URL (e.g., `my-portfolio.vercel.app`).

---

## Maintenance & Updates

Because we asked Gemini to separate the data, updating your site is easy:

1. Open your project in GitHub (or clone it locally).
2. Find the `content/index.ts` (or `data.ts`) file.
3. Edit your text, add new projects, or change links.
4. Commit changes. Vercel will **automatically redeploy** your site.

---

### Ready to level up?

You now have a modern portfolio, but building the skills to back it up is what matters.

- **Master AI Development**: Check out my live courses at [aicademy.ac/courses](https://www.aicademy.ac/courses).
- **Get a Scholarship**: Apply for up to **100% off** at [aicademy.ac/scholarship](https://www.aicademy.ac/scholarship).

Happy coding!
