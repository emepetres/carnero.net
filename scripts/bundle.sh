#!/bin/bash
set -e

# This script is used to build the project locally

python -m site_generator.bundle _site content
