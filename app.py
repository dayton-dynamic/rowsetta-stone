from pathlib import Path
from collections import defaultdict
import sys
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


DEBUG = True
# FLATPAGES_AUTO_RELOAD = DEBUG
# FLATPAGES_EXTENSION = ['.html', '.md']
# FLATPAGES_ROOT = 'content'
# FREEZER_DESTINATION = "rowsetta"
# FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME*'] # keep the repository files.

app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

language_folders = Path("lang")


def get_solutions():
    solutions = defaultdict(dict)
    languages = set()
    for path in Path("solutions").iterdir():
        solutions[path.stem][path.suffix] = path.read_text()
        languages.add(path.suffix)
    languages = ['.result', ] + sorted(languages - {'.result'})
    return (solutions, languages)


def reordered_dict(orig, order):
    order = [k for k in order if k in orig] + [k for k in orig if k not in order]
    return {k: orig[k] for k in order}

@app.route("/")
def index():

    (solutions, languages) = get_solutions()
    solution_order = Path("solution_order.txt").read_text().split()
    solutions = reordered_dict(solutions, solution_order)
    return render_template(
        "index.html",
        solutions=dict(solutions),
        languages=languages,
        solution_order=solution_order,
    )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
