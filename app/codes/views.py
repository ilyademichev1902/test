from flask import render_template

from . import bp

@bp.route('/')
def grid():
    return render_template('grid.html.jinja')
