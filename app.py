import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ['.html', '.md']
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PROJECTS_DIR = 'projects'
FREEZER_DESTINATION = "rowsetta"
FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME*'] # keep the repository files.

app = Flask(__name__)
app.config.from_object (__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

#Homepage
@app.route('/')
def index():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    projects = [project for project in flatpages if project.path.startswith(PROJECTS_DIR)]
    return render_template('index.html', posts=posts, projects=projects)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
