from flask import render_template, request, redirect, url_for, flash
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_dance.contrib.facebook import facebook
from app import app
from app.models import TodoList
from app import db
from app.models import UserAccounts

@app.route('/')
def main():
    return redirect(url_for('login_self'))

@app.route('/login/self', methods=['GET', 'POST'])
def login_self():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = UserAccounts.query.filter_by(email=email, password=password).first()
        
        if user and password:
            return redirect(url_for('todo_main', user_id=user.user_id))
        else:
            flash('Invalid email or password', category = 'error')
    return render_template('login.html')

@app.route('/login/google')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))
    account_info = google.get("https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses")
    if account_info.ok:
        account_info_json = account_info.json()

        email = account_info_json.get("emailAddresses", [{}])[0].get("value", "N/A")

        password = account_info_json.get("names", [{}])[0].get("displayName", "N/A")   #Gets full name from google as password

        user = UserAccounts.query.filter_by(email=email, password=password).first()
        if user and password:           #If user used google before to login, it will redirect to todo_main and display to the same data from that account
            return redirect(url_for('todo_main', user_id=user.user_id))
        else:                           #If first time using google to login, it will register email and username as password in database, then redirect to todo_main
            register = UserAccounts(email=email, password=password)
            db.session.add(register)
            db.session.commit()
            user = UserAccounts.query.filter_by(email=email, password=password).first()
            return redirect(url_for('todo_main', user_id=user.user_id))
    return f"Failed to fetch user info from Google: {account_info.text}"

@app.route('/login/facebook')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))
    account_info = facebook.get('/me?fields=id,name,email')
    if account_info.ok:
        account_info_json = account_info.json()

        email = account_info_json.get("email", "N/A")

        password = account_info_json.get("name", "N/A")   #Gets full name from facebook as password

        user = UserAccounts.query.filter_by(email=email, password=password).first()
        if user and password:           #If user used facebook before to login, it will redirect to todo_main and display to the same data from that account
            return redirect(url_for('todo_main', user_id=user.user_id))
        else:                           #If first time using facebook to login, it will register email and username as password in database, then redirect to todo_main
            register = UserAccounts(email=email, password=password)
            db.session.add(register)
            db.session.commit()
            user = UserAccounts.query.filter_by(email=email, password=password).first()
            return redirect(url_for('todo_main', user_id=user.user_id))
    return f"Failed to fetch user info from Facebook: {account_info.text}"

@app.route('/login/github')
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    account_info = github.get('/user')
    if account_info.ok:
        account_info_json = account_info.json()

        email_info = github.get('/user/emails')   #Gets email from github
        if email_info.ok:
            emails = email_info.json()
            # Get the primary email (the first one marked as 'primary' and 'verified')
            email = next((email['email'] for email in emails if email['primary'] and email['verified']), None)

        password = account_info_json.get('login')   #Gets username from github as password

        user = UserAccounts.query.filter_by(email=email, password=password).first()
        if user and password:           #If user used github before to login, it will redirect to todo_main and display to the same data from that account
            return redirect(url_for('todo_main', user_id=user.user_id))
        else:                           #If first time using github to login, it will register email and username as password in database, then redirect to todo_main
            register = UserAccounts(email=email, password=password)
            db.session.add(register)
            db.session.commit()
            user = UserAccounts.query.filter_by(email=email, password=password).first()
            return redirect(url_for('todo_main', user_id=user.user_id))
    return f"Failed to fetch user info from GitHub: {account_info.text}"

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
