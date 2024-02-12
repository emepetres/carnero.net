# carnero.net

My personal website

## How to write a new post

### 1. Write the post content in markdown

Add a new file in the `posts` directory with the following format:

```markdown
# tile

Text here is ignored. Use for properties, notes, etc.

## TL;DR (rirst h2 is considered the summary)

summary

## section 1

markdown content, more h2 sections, subsections, etc.
```

### 2. Add the post to the feed metadata

Add to the top of ´posts/posts.yml´ posts section the new post file and language. The pub_date is optional, it will be added automatically if not set.

This is the equivalent of publishing it.

### 3. Test it locally

Run the following command to build the site and test it locally:

```bash
[only the first time] mamba env create -f scripts/blog_generator/environment.yml
mamba activate blog_generator
scripts/build.sh
```

### 4. Commit and push

Commit to master & push. The site will be automatically built and deployed.

## How to update the site

Just commit to master & push. The site will be automatically built and deployed.

## TODO

- [ ] Add Github, Linkein & Twitter links
- [ ] Write interests
- [ ] Write things I believe in
- [ ] Add feed to landing
- [ ] Write first post
- [ ] Add favicon
- [ ] Publish design principles
- [ ] Add categories to feed, landing & posts
- [ ] Pagination