from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tree import Tree
from flask_app.models.user import User


@app.route('/add/tree')
def add():
    print(0)
    if 'id_user' not in session:
        print(1)
        return redirect('/logout')
    data_user = {
        "id_user":session['id_user']
    }
    print(2)
    return render_template("/add_tree.html", user=User.get_by_id(data_user))

@app.route('/create/tree',methods=['POST'])
def create_tree():
    if 'id_user' not in session:
        print(20)
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/add/tree')
    data_tree = {
        "specie":request.form["specie"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date_planted": request.form["date_planted"],
        "who_planted": session["id_user"]
    }
    print(25)
    Tree.save(data_tree)
    return redirect('/dashboard')


@app.route('/car/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    Car.delete(data)
    return redirect('/dashboard')


@app.route ('/mytrees/<int:who_planted>')
def edit(tree_data):
    if 'user_id' not in session:
        print(1)
        return redirect('/logout')
    tree_data = {
        "id":session['user_id']
    }
    return render_template('/edit_tree.html', tree=Tree.get_by_id(tree_data))


@app.route ('/update/car',methods=['POST'])
def update():
    Car.update(request.form)
    return redirect('/dashboard')



# @app.route ('/update/car',methods=['POST'])
# def update():
#     if 'user_id' not in session:
#         print(20)
#         return redirect('/logout')
#     if not Car.validate_car(request.form):
#         return redirect('/add/car')
#     data = {
#         "price":int(request.form["price"]),
#         "description": request.form["description"],
#         "model": request.form["model"],
#         "make": request.form["make"],
#         "year": int(request.form["year"]),
#         "id": int(request.form["id"])
#     }
#     print(25)
#     Car.update(data)
#     return redirect('/dashboard')

@app.route ('/tree/show/<int:id_tree>')
def show_tree(id_tree):
    if 'id_user' not in session:
        return redirect('/logout')
    tree_data ={
        'id': id_tree
    }

    return render_template("show_tree.html",tree=Tree.get_by_id(tree_data), visitors=User.full_name(tree_data))

# @app.route('/car/show/<int:id>')
# def show(id):
#     if 'user_id' not in session:
#         return redirect('/logout')
#     data = {
#         "id":id
#     }
#     return render_template("show_car.html",car=Car.get_car_and_seller(data))

