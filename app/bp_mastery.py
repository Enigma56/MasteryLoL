from flask import Blueprint, render_template, request, g
from ..api.account_data import get_account_information

bp = Blueprint('mastery', __name__, url_prefix='/')


@bp.route('home')
def home():
    return render_template('home.html')


# TODO: Check for account existance before rendering this page
@bp.route('profile', methods=['GET', 'POST'])
def profile():
    # Execute puuid search here
    info = get_account_information(request.form['ign'].lower(), request.form['tag'])
    print(info)
    return render_template('profile.html', info=info)
