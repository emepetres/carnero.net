---
pub_date: '2024-03-29T12:05:29.884874+00:00'
---
# Tips for CI/CD development

Text here is ignored. Use for properties, internal notes, etc.

## Intro

It's not uncommon to come across numerous commits in the Git history dedicated to fixing pipelines. This happens because testing pipelines can be challenging, and ultimately, the only way to truly verify their functionality is by pushing the code and observing its behavior.

## Content

Throughout the years, I've tested several strategies to simplify the testing of pipelines, and these are the "best practices" that I've found to be effective.

_This work was originally published as a [blog post](/blog/tips_cicd_development.html)._
{: .note}

### 1. Work in a dedicated branch

When uncertain about the pipeline's functionality (which should be always), create a new branch for testing. This allows you to push the code and assess its performance without impacting the main branch. Once you're confident in its functionality, merge the branch into the main branch using a **squash merge** to maintain a clean history.

### 2. Encapsulate functionality in scripts

A practical approach is to encapsulate most steps into scripts (bash, PowerShell, Python, etc.). This makes it easier to test the pipeline locally without relying on frameworks or complex tools. Not only does it enable you to test most functionality locally before pushing the code, but it also accelerates debugging with immediate feedback.

### 3. Utilize a linter

Employ an Integrated Development Environment (IDE) like Visual Studio Code that incorporates a linter for the pipeline language in use. This helps catch syntax errors and common mistakes before pushing the code.

### 4. Avoid tools for local testing

While it might be tempting to use tools emulating the pipeline environment locally, I believe this is a risky approach. The pipeline environment is intricate, making it challenging to replicate locally accurately. This can create a false sense of security, leading to the submission of non-functional code. Additionally, for complex pipelines, relying on local emulation may result in the addition of unnecessary code, adding maintenance overhead and potential sources of bugs.
