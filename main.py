from flask import Flask, request , render_template , redirect
import time , sqlite3
global auth
auth = 0
app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    global auth
    if auth == 1:
        return redirect('/posts',code=302)
    else:
        return render_template("root.html")

@app.route('/login', methods = ['GET','POST'])
def login():
    return render_template("login.html")

@app.route('/signup', methods = ['GET','POST'])
def signup():
    return render_template("signup.html")


@app.route('/verify-signup' , methods = ['GET','POST'])
def verify():
    global password, username , email , password2, auth
    password2 = str(request.form['password2'])
    password = str(request.form['password'])
    username = str(request.form['username'])
    conn = sqlite3.connect('stuff.db')
    c = conn.cursor()
    if password == password2:
        c.execute("SELECT * FROM user_details WHERE username=?", (username,))
        stuff = c.fetchall() #NOTE TO SELF : HAVE TO ADD A LOT OF VERIFICATION TO MAKE SURE PASSWORD LENGTH , CHARECTERS ETC ARE LEGIT, NO SQLITE INJECTIONS
        if len(stuff)==0:
            c.execute("insert into user_details ( serial_number , username,password) values (null , ?,?)",
                      (username, password))
            conn.commit()
            auth = 1
            return redirect('/',code=302)
        else:
            return "USERNAME TAKEN. GO BACK AND CHOOSE OTHER ONE SON"
            #comebacklater
    else:
        return "PASSWORDS DON'T MATCH. GO BACK AND TRY AGAIN"

@app.route('/login_verification',methods = ['GET','POST'])
def login_verification():
    global auth,username,password
    username = str(request.form['login-username'])
    password = str(request.form['login-password'])
    conn = sqlite3.connect('stuff.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_details WHERE username=?",(username,))
    stuff = c.fetchall()
    if len(stuff)==0:
        return "INVALID CREDENTIALS. GO BACK AND TRY AGAIN"
    else:
        for details in stuff:
            db_username = details[1]
            db_password = details[2]
            if db_password == password and db_username == username:
                auth = 1

                return redirect('/',code=302)
            else:
                return "INVALID CREDENTIALS. GO BACK AND TRY AGAIN"
'''

@app.route('/error')

@app.route('/settings')

@app.route('/<username>/') #COMING SOON!!!!!!!!!!!!!!!!!!!!!!!!

@app.route('/posts')


@app.route('/<username>/public')
'''
if __name__ == "__main__":
        app.run(debug=True)
