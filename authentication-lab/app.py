from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyASx2vWHHg418m4HX4eKbxOrIqC75zACo8",
  "authDomain": "meet---2022.firebaseapp.com",
  "projectId": "meet---2022",
  "storageBucket": "meet---2022.appspot.com",
  "messagingSenderId": "115400578724",
  "appId": "1:115400578724:web:a8565930f311175a6db831",
  "measurementId": "G-G009ZDNMKG",
  "databaseURL": "https://meet---2022-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
           return render_template("signup.html")
    else:
        return render_template("signin.html")


    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            name = request.form['full_name']
            username = request.form['username']
            bio = request.form['bio']
            user = {"full name" : name , "username" : username , "biography" : bio}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))

        except:
            error = "Error"
            return render_template("signup.html")

    else:
        return render_template("signup.html")



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():

    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        #try: 
        tweet = {"title" : title , "text" : text , "uid" : login_session['user']['localId']}
        db.child("Tweets").push(tweet)
        return redirect(url_for('all_tweets'))

        #except:
        #    return render_template("add_tweet.html")

    else: 
        return render_template("add_tweet.html")

    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    all_the_tweets = db.child("Tweets").get().val().values()
    return render_template("all_tweets.html", all_the_tweets = all_the_tweets )


if __name__ == '__main__':
    app.run(debug=True)