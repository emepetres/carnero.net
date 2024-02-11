#!/bin/bash
set -e

# This script must be run after building the site with the build.sh script

rm -rf _site
mkdir -p _site/writings
cp *.html _site
cp *.css _site
cp *.xml _site
cp -r writings/*.html _site/writings/
cp -r img _site/img
cp -r blog _site/blog
cp LICENSE _site
