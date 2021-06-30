from flask import Flask, render_template, url_for, redirect, request, session
from authlib.integrations.flask_client import OAuth
application = Flask(__name__)

oauth = OAuth(application)

application.config['SECRET_KEY'] = "super"
application.config['GOOGLE_CLIENT_ID'] = "1055422963219-vif63bofkmidos35lr8ijh94200a4m3b.apps.googleusercontent.com"
application.config['GOOGLE_CLIENT_SECRET'] = "2KhyjBnh63iVtvijRVBuspKh"

google = oauth.register(
    name = 'google',
    client_id = application.config["GOOGLE_CLIENT_ID"],
    client_secret = application.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)



# Default route
@application.route('/')
def index():
    session['islogged'] = False
    return render_template('index.html')


# Google login route
@application.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@application.route('/login/google/authorize')
def google_authorize():
    if not session['islogged']:
        try:
            google = oauth.create_client('google')
            token = google.authorize_access_token()
            resp = google.get('userinfo').json()
            session['islogged'] = True
            session['username'] = resp['name']
            print(f"\n{resp}\n")
            return redirect(url_for('home'))
        except:
            session['islogged'] = False
            return redirect(url_for('index'))
    else:
        return redirect(url_for('home'))


@application.route('/home')
def home():
    return render_template('First_page.html', name = session['username'])


@application.route('/staticfeed/', methods=['POST'])
def Staticfeed():
    if session['islogged']:
        if request.form['Static Feed']=="static":
            username = session['username']
            return render_template('static.html', name=username)
    else:
        return redirect(url_for('index'))


@application.route('/livefeed/', methods=['POST'])
def Livefeed():
    if session['islogged']:
        if request.form['Live Feed']=="live":
            return render_template('live.html', name=username)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
  application.run(debug=True)