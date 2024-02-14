from datetime import datetime
from flask import Flask, Blueprint, redirect, render_template, request, session
from dotenv import load_dotenv
import requests
import os

from .models import find_user_by_token, save_user_token

load_dotenv()

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # TODO: If the user is logged in, redirect them to the app
    return render_template("index.html", FOURSQUARE_CLIENT_ID=os.getenv('FOURSQUARE_CLIENT_ID'), HOSTNAME=os.getenv('HOSTNAME'))

# The route that foursquare directs users back to after they've logged in
@bp.route('/auth')
def authenticate():
    FOURSQUARE_CLIENT_ID = os.getenv('FOURSQUARE_CLIENT_ID')
    FOURSQUARE_CLIENT_SECRET = os.getenv('FOURSQUARE_CLIENT_SECRET')

    code = request.args.get('code')
    print(code)  
    HOSTNAME = os.getenv('HOSTNAME')
    response = requests.get(f'https://foursquare.com/oauth2/access_token?client_id={FOURSQUARE_CLIENT_ID}&client_secret={FOURSQUARE_CLIENT_SECRET}&grant_type=authorization_code&redirect_uri={HOSTNAME}/auth/user&code={code}')
    token = response.json()['access_token']

    print('finding user by token')
    if not find_user_by_token(token):
        print('nope')
        print(find_user_by_token(token))
        save_user_token(token)

    session['token'] = token

    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    return redirect(f'/history/date/{today}')

@bp.route('/history/date/<date>')
def history(date):
    date_str = request.view_args['date']
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    after_timestamp = int(date_obj.timestamp())
    before_timestamp = after_timestamp + 86400
    token = session.get('token')
    checkins = requests.get(f'https://api.foursquare.com/v2/users/self/checkins?oauth_token={token}&v=20190101&beforeTimestamp={before_timestamp}&afterTimestamp={after_timestamp}')
    return render_template("daily-checkins.html", checkins=checkins.json())