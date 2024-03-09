---
img: https://carnero.net/img/blog/tips_cicd_development.png
---
# Tips for CI/CD development

## Summary

It is common to see, at some point in the git history, many commits that are just fixing the pipeline.
This is because pipelines are hard to test and, at the end of the day, the only way to really know if they are working is to push the code and see if it works. In this post I share some tips I find useful to make testing pipelines easier.

## Content

It's not uncommon to come across numerous commits in the Git history dedicated to fixing pipelines. This happens because testing pipelines can be challenging, and ultimately, the only way to truly verify their functionality is by pushing the code and observing its behavior.

Throughout the years, I've developed several strategies to simplify the testing of pipelines, and these are the "best practices" that I've found to be effective.

### Encapsulate functionality in scripts

A practical approach is to encapsulate most steps into scripts (bash, PowerShell, Python, etc.). This makes it easier to test the pipeline locally without relying on frameworks or complex tools. Not only does it enable you to test most functionality locally before pushing the code, but it also accelerates debugging with immediate feedback.

### Utilize a linter

Employ an Integrated Development Environment (IDE) like Visual Studio Code that incorporates a linter for the pipeline language in use. This helps catch syntax errors and common mistakes before pushing the code.

### Avoid tools for local testing

While it might be tempting to use tools emulating the pipeline environment locally, I believe this is a risky approach. The pipeline environment is intricate, making it challenging to replicate locally accurately. This can create a false sense of security, leading to the submission of non-functional code. Additionally, for complex pipelines, relying on local emulation may result in the addition of unnecessary code, adding maintenance overhead and potential sources of bugs.

### Work in a dedicated branch

When uncertain about the pipeline's functionality (which should be always), create a new branch for testing. This allows you to push the code and assess its performance without impacting the main branch. Once you're confident in its functionality, merge the branch into the main branch using a squash merge to maintain a clean history.

## A real example

I recently introduced a [Github Action](https://github.com/emepetres/html-minifier-action) designed to minify HTML files using [HTMLMinifier](https://github.com/kangax/html-minifier). In GitHub, a workflow (pipeline) must be defined in the default branch before utilization. Consequently, I initiated by pushing the pipeline scaffolding, featuring a hello-world-like content, to the main branch. Subsequently, I created the dev branch and commenced work on the pipeline, under Visual Studio Code.

![runs](/img/blog/tips_cicd_development.png)

I tested the pipeline locally using JavaScript scripts I authored. Once I verified its functionality, I pushed the code to the dev branch. After thorough testing, where I found some issues with the working directory, I performed a squash merge, integrating the dev branch into the main branch while maintaining a clean history.
