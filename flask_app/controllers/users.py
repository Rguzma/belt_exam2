from flask import render_template,redirect,session,request,flash

from flask_app import app
from flask_app.models.user import User                         #funcion en models
from flask_app.models.tree import Tree
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")                                           #FIRST STEP
def index():                                                #FIRST STEP 
    return render_template("index.html")
    



@app.route('/create',methods=['POST'])        #SIXTH STEP. INTERACTION WITH FORM
def create():
    print(0)
    if not User.validate_register(request.form):                             #PROCESO DE VALIDACION
        print(1)
        return redirect('/')

        
    data = {
        "first_name": request.form ['first_name'],
        "last_name": request.form ['last_name'],
        "email": request.form ['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])

    }
#   confirmation = bcrypt.check_password_hash(encryptedpassword)
    
    print(2)
    id = User.save(data)
    session['id_user'] =id
    return redirect('/dashboard')



@app.route('/login',methods=['POST'])
def login():
    print(0)
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        print(1)
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        print(2)
        return redirect('/')
    session['id_user'] = user.id_user
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'id_user' not in session:
        return redirect('/logout')
    data ={
        'id': session['id_user']
    }
    return render_template("dashboard.html", tree=Tree.get_all(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
