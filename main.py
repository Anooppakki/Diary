from flask import Flask, request , render_template , redirect
import time , sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("root.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/signup', methods = ['GET','POST'])
def signup():
    return render_template("signup.html")


@app.route('/verify-signup' , methods = ['GET','POST'])
def verify():
    global password, username , email , password2
    password2 = str(request.form['password2'])
    password = str(request.form['password'])
    username = str(request.form['username'])
    conn = sqlite3.connect('stuff.db')
    c = conn.cursor()
    if password == password2:
        c.execute("SELECT * FROM user_details WHERE usernames=?", (username,))
        ppp = c.fetchall()
        if len(ppp)==0:
            c.execute("INSERT INTO user_details")

    else:
        redirect()

@app.route('/login_verification')


if __name__ == "__main__":
        app.run(debug=True)
