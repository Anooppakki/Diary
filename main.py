from flask import Flask, request , render_template , redirect
import time , sqlite3
global auth,username_approved , password_approved
auth = False
approved_username_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                           'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '-', '_', '.']
approved_password_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                           'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                           '(', ')', '_', '+', '=', '-', '\',''', ';', '/', '.', ',', '|', '}', '{', '"', ':', '?', '>',
                           '<']


def check_username(username):
    n = len(str(username))
    un_approved = []
    if len(str(username)) <= 20:
        for k in range(n):
            letter = username[k]
            if (letter in approved_username_chars) is True:
                pass
            else:
                un_approved.append(letter)
        if len(un_approved) == 0:
            global username_approved
            username_approved = True


def check_password(password):
    n = len(str(password))
    un_approved = []
    if len(str(password)) <= 64:
        for k in range(n):
            letter = password[k]
            if (letter in approved_password_chars) is True:
                pass
            else:
                un_approved.append(letter)
        if len(un_approved) == 0:
            global password_approved
            password_approved = True


app = Flask(__name__)


@app.route('/',methods = ['GET','POST'])
def index():
    global auth
    if auth = True:
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
    username1 = str(request.form['username'])
    conn = sqlite3.connect('stuff.db')
    c = conn.cursor()
    username = str(username1.lower())
    check_username(username)
    if username_approved = True:
        check_password(password)
        if password_approved = True:

            if password == password2:
                c.execute("SELECT * FROM user_details WHERE username=?", (username,))
                stuff = c.fetchall() #NOTE TO SELF : HAVE TO ADD A LOT OF VERIFICATION TO MAKE SURE PASSWORD LENGTH , CHARECTERS ETC ARE LEGIT, NO SQLITE INJECTIONS
                if len(stuff)==0:
                    c.execute("insert into user_details ( serial_number , username,password) values (null , ?,?)",
                              (username, password))
                    conn.commit()
                    auth = True
                    return redirect('/',code=302)
                else:
                    return "USERNAME TAKEN. GO BACK AND CHOOSE OTHER ONE SON"
                    #comebacklater
            else:
                return "PASSWORDS DON'T MATCH. GO BACK AND TRY AGAIN"
        else:
            return "MAKE SURE PASSWORD IS UNDER 64 CHARS AND DOESN'T CONTAIN UNACCEPTABLE CHARS. ONLY A-Z , a-z , 0-9 and ~`!@#$%^&*()_+=-|}{\":?><\\';/.,'"
    else:
        return "MAKE SURE USERNAME IS UNDER 20 LETTERS AND CONTAINS 0-9 a-z AND _-. only"

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
                auth = True
	
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
