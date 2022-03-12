#!/usr/bin/env python3

### IMPORTS ###
import logging

from flask import Blueprint, render_template_string

### GLOBALS ###
root_blueprint = Blueprint('root', __name__)

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <title>HA-STS Server</title>
</head>
<body style="min-height: 100%;">
  <h1>Basic HA-STS Server Core</h1>
  <p>Here's the URLs for the parts of the site:</p>
  <ul>
  {% for item in links %}
    <li><a href="{{item}}">{{item}}</a></li>
  {% endfor %}
  </ul>
</body>
</html>
"""

SITEMAP_LINKS = []

### FUNCTIONS ###
@root_blueprint.route('/', methods = ['GET'])
def index():
    return render_template_string(HTML_PAGE, links = SITEMAP_LINKS)

### CLASSES ###
# FIXME: Make this into a proper class based implementation later
class RootBlueprint:
    pass
