from flask import Blueprint, render_template

bp = Blueprint('mastery', __name__, url_prefix='/')


@bp.route('home')
def home():
    return render_template('home.html')
