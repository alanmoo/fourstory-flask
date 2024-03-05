from datetime import datetime, timedelta
from flask import Blueprint, redirect, render_template, request, session
from dotenv import load_dotenv
import requests
import os
import urllib.parse

from .models import find_user_by_token, save_user_token

load_dotenv()

bp = Blueprint('main', __name__)
HOSTNAME = os.getenv('HOSTNAME', 'http://127.0.0.1')
PORT = os.getenv('PORT', '80')
if PORT == '80':
    HOST = HOSTNAME
else:
    HOST = f'{HOSTNAME}:{PORT}'

@bp.route('/')
def index():
    # TODO: If the user is logged in, redirect them to the app
    vars = {
        'FOURSQUARE_CLIENT_ID': os.getenv('FOURSQUARE_CLIENT_ID'),
        'HOSTNAME': HOST,
    }
    return render_template("index.html", **vars)

# The route that foursquare directs users back to after they've logged in
@bp.route('/auth')
def authenticate():
    FOURSQUARE_CLIENT_ID = os.getenv('FOURSQUARE_CLIENT_ID')
    FOURSQUARE_CLIENT_SECRET = os.getenv('FOURSQUARE_CLIENT_SECRET')

    code = request.args.get('code')

    query = urllib.parse.urlencode({
        'client_id': FOURSQUARE_CLIENT_ID,
        'client_secret': FOURSQUARE_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': urllib.parse.urljoin(HOST, '/auth/code'),
        'code': code,
    })
    req_url = urllib.parse.urlunparse((
        'https',
        'foursquare.com',
        'oauth2/access_token',
        '',  # "path parameters" argument, largely unused on the internet as a whole
        query,
        '',  # fragment
    ))
    resp = requests.get(req_url)
    token = resp.json()['access_token']

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
    prev_day = date_obj - timedelta(days=1)
    prev_day_str = prev_day.strftime('%Y-%m-%d')
    next_day = date_obj + timedelta(days=1)
    next_day_str = next_day.strftime('%Y-%m-%d')

    templateVars = {
        'checkins': checkins.json(),
        'date': date_str,
        'prevDayStr': prev_day_str,
        'nextDayStr': next_day_str,
    }
    
    return render_template("daily-checkins.html", **templateVars)