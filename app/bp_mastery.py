from flask import Blueprint, render_template, request, g
from ..api.account_data import get_account_information

bp = Blueprint('mastery', __name__, url_prefix='/')


@bp.route('home')
def home():
    return render_template('home.html')


@bp.route('profile', methods=['GET', 'POST'])
def profile():
    # Execute puuid search here
    info = get_account_information(request.form['ign'], request.form['tag'])
    print(info)
    print(g.db)
    return render_template('profile.html', info=info)
