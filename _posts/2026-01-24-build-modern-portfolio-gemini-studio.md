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
title: Build a Modern Portfolio with Gemini Studio & React
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
description: Master building a dynamic portfolio website using Gemini Studio and React
  TypeScript. Follow our detailed guide to set up, integrate, and deploy your professional
  online presence.
video_id: ''
playlist_id: ''
github_repo: ''
---

Stop building static portfolios. This guide shows you how to leverage Google's Gemini Pro to create a dynamic, AI-powered showcase. We'll integrate the Gemini API with a React TypeScript frontend to generate your bio, skills,
and projects on the fly using Google AI Studio for rapid prompt engineering.

## What You'll Get

* A step-by-step guide to integrate Google's Gemini API into a React app.
* Actionable code snippets for setting up a React project from scratch.
* A high-level architecture diagram to visualize the data flow.
* A proven strategy for prompting Gemini to generate structured JSON data.
* A clear breakdown of the pros and cons of this AI-driven approach.

## Prerequisites and Setup

Before starting, ensure you have accounts for:

* [Google AI Studio](https://aistudio.google.com/): Gemini API access.
* [GitHub](https://github.com/): Version control.
* [Vercel](https://vercel.com/): Deployment.
* [Web3Forms](https://web3forms.com/): Contact forms.
* [Custom Domain](https://vercel.com/docs/projects/domains): Optional but recommended (Paid).

## Extract Yout Profile From LinkedIn/Resume

* If you don't have your resume with you, go to your LinkedIn profile, click on Resources, then click on "Save to PDF".

## Gemini Studio Setup

To get started, we need to carefully prompt Gemini 3 Pro to act as our "Senior Frontend Architect". Open [Google AI Studio](https://aistudio.google.com/), create a new chat prompt, and paste the following System Instructions.

### System Prompt

Paste the following block into the **System Instructions** field in Google AI Studio. This prompt defines the role, tech stack, and strict coding rules.

```md

# Role
Act as a Senior Frontend Architect specializing in high-performance, mobile-first React applications. Your goal is to generate production-grade, maintainable, and strictly typed code.

# Tech Stack Standards
- Core: React (Functional Components) + TypeScript (Strict Mode).
- Styling: Tailwind CSS (Utility-first, mobile-first breakpoints).
- Icons: Lucide-React (or HeroIcons).
- Animations: Framer Motion (for polished, rich interactions).
- State/Forms: React Hook Form (efficient) or standard state for simple forms.

# Architectural Rules (Non-Negotiable)
1.  Mobile-First Discipline: Write CSS for mobile screens first (default), then add sm:, md:, lg: overrides.
2.  Micro-Componentization: Break UI into "Nano-Components" (e.g., <Button />, <Card />, <SectionHeading />) to ensure reusability and readability. Max file length ~100-150 lines.
3.  Separation of Concerns:
    -   Data: ALL text content, portfolio items, and configuration literals must be extracted into a separate data.ts or config.ts file. Do not hardcode content in JSX.
    -   Logic: Custom hooks for complex logic.
4.  DRY & Type Safety: No repetitive code. Use TypeScript interfaces for all props and data models. Avoid any.
5.  External Libs: Do not reinvent the wheel. If a standard library (like framer-motion or lucide-react) solves a problem elegantly, use it.
6.  Accessibility: Ensure semantic HTML (<main>, <section>, <nav>) and proper ARIA labels.

# Output Style
- Provide code files clearly.
- Do not explain basic React concepts; focus on the implementation details.
```

### User Prompt

Once the system prompt is set, use this structured prompt to generate the initial project files. **Remember to fill in the "USER CONFIGURATION" section with your specific details.**

```md
# Project: Dynamic Modern Portfolio Generator

## 1. USER CONFIGURATION (EDIT THIS SECTION ONLY)
- Web3Forms Token: <WEB3_TOKEN>
- Resume/LinkedIn Profile: Attached
- Target Audience: [e.g., Recruiters, Clients, Developers]

## 2. Design Directive: "The Unique Seed"
CRITICAL: Before generating any code, you must randomly select a distinct modern design aesthetic to ensure this portfolio looks unique compared to previous generations. Pick ONE of the following styles (or invent a hybrid):
1.  Neo-Brutalism: High contrast, bold borders, vibrant simplified colors, large typography.
2.  Glassmorphism: Deep gradients, frosted glass effects, floating cards, subtle borders.
3.  Swiss Minimal: Huge negative space, grid-based, massive sans-serif fonts, monochromatic with 1 accent color.
4.  Cyber-Gradient: Dark mode base, rich moving gradients (mesh), glowing accents, tech-focused.
5.  Ensure to use the attached resume/LinkedIn profile to generate the portfolio.
6.  Make the scroll up and scroll down animations smooth and rich.
7.  Make the website mobile-first and responsive.
8.  Ensure to add Vercel json file so that it becomes deployable on Vercel.
9.  Add a custom favicon for the website.

*Apply this chosen style consistently across fonts, spacing, and animations.*

## 3. Requirements
Create a single-page, smooth-scroll React portfolio based on the Configuration above and your chosen Design Directive.

### Core Sections
1.  Hero: High impact, distinct value proposition, rich usage of the chosen font.
2.  Tech Stack: Visual representation (grid/carousel) of skills.
3.  Projects: Card-based layout displaying "Data Source" items. Cards must be interactive (hover effects).
4.  Timeline/Experience: Vertical layout for professional history.
5.  Contact: Functional form using the Web3Forms Token.
    -   Form Logic: POST request to https://api.web3forms.com/submit.
    -   Fields: Name, Email, Message, hidden robots honeypot, hidden access_key input.

### Functional Constraints
-   Config-Driven: All text (Headlines, Bio, Projects) must be imported from a content/index.ts file. Create this file first based on the "Data Source" provided.
-   Responsive: The layout must look perfect on iPhone SE, iPad, and 4K Desktop.
-   Performance: Use lazy loading for images if applicable.

## 4. Execution Step
Start by declaring the Selected Design Style and the Color Palette (Hex Codes) you will use. Then, generate the file structure, starting with the data/config file.
```

## Store Code on GitHub

Once you have your code generated in Gemini Studio, you can directly push it to GitHub.

1. **Link GitHub Account:** Click on the GitHub Icon in the top right corner and select "Export to GitHub". You will be asked to authorize your GitHub account.
2. **Create New Project:** Select "Create a new repository". Name your project (e.g., `my-ai-portfolio`).
3. **Push Changes:** Confirm the files to be committed and click "Push". Your code is now safely stored in a new GitHub repository.

## Deploy on Vercel

1. **Import:** Log in to [Vercel](https://vercel.com/) with GitHub and import your new repository.
2. **Deploy:** Click **Deploy**. Vercel handles the build configuration automatically.
3. **Live:** Your site is now live and will update automatically on every push.

## Maintaining Your Portfolio

The best part about this workflow is how easy it is to maintain. Need to add a new job or project?

1. Go back to your Gemini Studio project.
2. Enter a prompt like, "Add a new role to my Professional Experience: Senior Gizmo Engineer at Acme Corp from 2023-Present."
3. Review the changes in the preview.
4. Commit the update to GitHub.

Vercel will automatically redeploy your site with the new information. Your portfolio stays current with just a few sentences.

## Conclusion

By combining the generative power of Gemini Studio with the robustness of React and TypeScript, you've built more than just a portfolio, you've created a scalable, professional platform that evolves with your career.

Ready to take your development skills to the next level? Check out my live courses available at [aicademy.ac/courses](https://www.aicademy.ac/courses).

Also, you can get up to a **100% discount** on our programs by taking the free scholarship test. Apply now at [aicademy.ac/scholarship](https://www.aicademy.ac/aisp).
