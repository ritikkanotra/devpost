from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import sqlite3
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
import os
from werkzeug.utils import secure_filename
from base64 import b64decode
import uuid
import magic
import shutil
from datetime import datetime


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "./static/assets/images/user_cache/"
Session(app)





if (os.path.exists(app.config["UPLOAD_FOLDER"])):
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

os.makedirs(app.config["UPLOAD_FOLDER"])

mydb = SQL("sqlite:///main.db")

def convert_image(image_data):
    f_name = uuid.uuid1().hex
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f_name))
    with open(file_path, 'wb') as f:
        f.write(image_data)
    
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)

    print(mime_type)

    if mime_type == 'image/jpeg':
        os.rename(file_path, file_path + '.jpg')
        # file_path += '.jpg'
        f_name = f_name + ".jpg"
    elif mime_type == 'image/png':
        os.rename(file_path, file_path + '.png')
        f_name = f_name + ".png"
    elif mime_type == 'image/gif':
        os.rename(file_path, file_path + '.gif')
        f_name = f_name + ".gif"
    elif mime_type == 'image/bmp':
        os.rename(file_path, file_path + '.bmp')
        f_name = f_name + ".bmp"
    elif mime_type == 'image/tiff':
        os.rename(file_path, file_path + '.tiff')
        f_name = f_name + ".tiff"

    print(file_path)
    
    return f_name



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        rows = mydb.execute("SELECT * FROM users WHERE email=:email", email = email)
        if len(rows) == 0:
            return render_template("apology.html", msg="You are not registered!", back="/login")
        
        print(check_password_hash(rows[0]["password_hash"], password))

        if check_password_hash(rows[0]["password_hash"], password) == False:
            return render_template("apology.html", msg="Incorrect password! Try again.", back="/login")

        session["user_id"] = rows[0]["id"]
        
        return redirect("/")


@app.route('/register', methods=['POST'])
def register():
    session.clear()

    if request.method == "POST":

        name = request.form.get('name')
        email = request.form.get('email')
        password_hash = generate_password_hash(request.form.get('password'))

        rows = mydb.execute("SELECT * FROM users WHERE email=:email;", email=email)
        
        if len(rows) != 0:
            return render_template("apology.html", msg="Email address already registered!", back="/register")

        mydb.execute("INSERT INTO users (name, email, password_hash) VALUES(?, ?, ?);", name, email, password_hash)
        return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route('/')
def explore():
    # print(session["user_id"])
    isLoggedIn = False
    user_name = None
    if session.get('user_id') is not None:
        isLoggedIn = True
        rows = mydb.execute("SELECT name FROM users WHERE id=:id;", id = session["user_id"])
        user_name = rows[0]["name"]

        
        print(datetime.now().strftime('%Y-%m-%d'))
    

    
    blog_rows = mydb.execute("SELECT * FROM blogs;")
    for row in blog_rows:
        
        
        row['coverimage'] = convert_image(row['coverimage'])
        # print(row['coverimage'])
        
        
        # row['coverimage'] = b64decode(row['coverimage'])
    return render_template("index.html", rows = blog_rows, isLoggedIn = isLoggedIn, user_name = user_name)


@app.route('/new_blog', methods=['GET', 'POST'])
@login_required
def new_blog():
    if request.method == 'POST':
        title = request.form.get('title')
        editor_data = request.form.get('editordata')
        cover_image = None
        print(request.files)
        if request.files:
            f = request.files['input_cover_image']

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            # f = request.files['input_cover_image']
            f.save(file_path)
            print(file_path)
            # This would save the file. Now to read simply use the normal way to read files in Python

            with open(file_path, 'rb') as f:
                cover_image = f.read()
                # print(file_content)
            
        rows = mydb.execute("SELECT name FROM users WHERE id=:id;", id = session["user_id"])
        user_name = rows[0]["name"]

        current_date = datetime.now().strftime('%Y-%m-%d')
            
        mydb.execute("INSERT INTO blogs(title, coverimage, content, author, date, likes, dislikes) VALUES(?, ?, ?, ?, ?, ?, ?);", title, cover_image, editor_data, session["user_id"], current_date, 0, 0)
        

        # print(cover_image)
        # print(request.form.get('editordata'))
        return redirect("/")
    else:
        return render_template("new_blog.html")


@app.route('/blogs/<blog_title>')
def show_blog(blog_title):

    print(blog_title)


    isLoggedIn = False
    current_user_name = None
    if session.get('user_id') is not None:
        isLoggedIn = True
        rows = mydb.execute("SELECT name FROM users WHERE id=:id;", id = session["user_id"])
        current_user_name = rows[0]["name"]

    rows = mydb.execute("SELECT * FROM blogs WHERE title=:title", title=blog_title)
    rows[0]['coverimage'] = convert_image(rows[0]['coverimage'])

    rows_author = mydb.execute("SELECT name FROM users WHERE id=:id;", id = rows[0]['author'])
    user_name = rows_author[0]["name"]

    print(rows[0]['date'])

    return render_template("blog_full.html", blog=rows[0], user_name = user_name, isLoggedIn = isLoggedIn, current_user_name = current_user_name)


@app.route('/update_like_dislike/<blog_title>/<liked>/<disliked>')
def update_like_dislike(blog_title, liked, disliked):
    print("update_like_dislike called")
    print("like: {}, dislike: {}".format(liked, disliked))
    if liked == '1':
        print('yes')
        mydb.execute("UPDATE blogs SET likes=likes+1 WHERE title=:title", title=blog_title)

    if disliked == '1':
        mydb.execute("UPDATE blogs SET dislikes=dislikes+1 WHERE title=:title", title=blog_title)

    return "1"

@app.route('/about')
def about():
    isLoggedIn = False
    current_user_name = None
    if session.get('user_id') is not None:
        isLoggedIn = True
        rows = mydb.execute("SELECT name FROM users WHERE id=:id;", id = session["user_id"])
        current_user_name = rows[0]["name"]
    


    return render_template("about.html", isLoggedIn = isLoggedIn, current_user_name = current_user_name)

if __name__ == '__main__':
    app.run()
