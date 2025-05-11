from flask import render_template, request, redirect, url_for, flash
from app import app
from app.models import TodoList
from app import db
from app.models import UserAccounts

@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserAccounts.query.filter_by(email=email, password=password).first()
        
        if user and password:
            return redirect(url_for('todo_main', user_id=user.user_id))
        else:
            flash('Invalid email or password', category = 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        register = UserAccounts(email=email, password=password)
        db.session.add(register)
        db.session.commit()

    return render_template('register.html')

@app.route('/todo_main/<int:user_id>', methods=['GET', 'POST'])
def todo_main(user_id):
    print(f"User ID: {user_id}")
    incomplete = TodoList.query.filter_by(complete=False, user_id=user_id).all()
    complete = TodoList.query.filter_by(complete=True, user_id=user_id).all()

    return render_template('todo_main.html', incomplete=incomplete, complete=complete, user_id=user_id)




@app.route('/add/<int:user_id>', methods=['POST'])
def add(user_id):
    todo = TodoList(text=request.form['todoitem'], complete=False, user_id=user_id)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('todo_main', user_id=user_id))


@app.route('/complete/<int:id>/<int:user_id>')
def complete(id, user_id):

    todo = TodoList.query.filter_by(todo_id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('todo_main', user_id=user_id))

@app.route('/delete/<int:id>/<int:user_id>')
def delete(id, user_id):

    todo = TodoList.query.filter_by(todo_id=int(id)).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('todo_main', user_id=user_id))
