""" authentication to system """
from flask import render_template, Blueprint, request, redirect, url_for, session, flash, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import check_password_hash, generate_password_hash
from levelUP.models import User
from levelUP import db
from levelUP.dna import _sendDNA
from levelUP.helpers.IDInstances import userInstance
from levelUP.helpers.logger import log

iden = Blueprint('auth', __name__)


@iden.route('/logout/')  # 127.0.0.1:5500/logout
@login_required
# log user out
def logout():
    session.clear()
    logout_user()
    flash('Please login again!',
          category='logout')
    session['current'] = '/logout'
    return redirect(url_for('auth.login'))


@iden.get('/login/')
def getLogin():
    # login page
    try:
        # if user already logged in
        if User.get_id(current_user):
            return redirect(url_for("app.home"))
    except:
        pass

    return render_template('login.html', user=current_user)


@iden.post("/login/")
def login():
    # login operation
    if request.method == 'POST':

        name = request.form.get('inputUsername')
        password = request.form.get('inputPassword')
        user = User.query.filter_by(uname=name).first()
        if user:
            # comparing two given parameters
            if check_password_hash(user.password, password):

                log(title='user', msg={
                    'userID': user.userID, 'username': user.uname, 'pattern': session['dna']})

                dna = _sendDNA(user_id=user.userID, pattern=session['dna'])
                log(title='dna', msg=dna)
                if dna['message_code'] == 10:
                    flash(
                        message="We need to collect some typing data from you. You may be asked to fill out this form multiple times.", category='info')
                    return redirect(url_for('tools.typing_patterns'))
                elif dna['message_code'] == 2:
                    flash(
                        message=f"{dna['message']} Please try all over again", category='info')
                    return redirect(url_for('auth.getLogin'))
                elif dna['message_code'] == 1 and dna['high_confidence'] == 1:
                    login_user(user, remember=False)
                else:
                    flash(
                        message=f"DNA high confidence: {dna['high_confidence']}, please try again", category='info')
                    return redirect(url_for('auth.getLogin'))

                flash('Welcome, "' + name + '"!', category='login')

                # return make_response(jsonify({'message': 'Login succesful', 'dnaID': user.dnaID, 'userID': user.userID, 'username': user.uname, 'pattern': session['dna']}), 200)
                return redirect(url_for("app.home"))

            else:
                flash("Password or the username is incorrect!", category='error')
                return redirect(url_for("auth.getLogin"))
        else:
            flash(
                "Password or the username is incorrect!", category='error')
            return redirect(url_for("auth.getLogin"))
    else:
        redirect(url_for('auth.getLogin'))


@iden.get('/signup/')
def getSignup():
    # signup page
    try:
        # if user already logged in
        if User.get_id(current_user):
            return redirect(url_for("app.home"))
    except:
        pass
    return render_template('signup.html', user=current_user)


@iden.post('/signup/')
def signup():
    # signup operation
    if current_user.is_authenticated:
        flash("Please logout to continue!", category='info')
        return redirect(url_for("app.home"))
    if request.method == "POST":
        newAcc = None
        name = request.form.get('inputUsername')
        password = request.form.get('inputPassword')
        password2 = request.form.get('inputPassword2')
        alias = request.form.get('alias')
        firstname = request.form.get('firstname')
        user = User.query.filter_by(uname=name).first()
        if user != None:
            # if user is exists
            flash("This username is already taken!", category='warning')
            return redirect(url_for("auth.getSignup"))
        if password2 != password:
            # if passwords are not matched
            flash("Passwords are not matched!", category='warning')
            return redirect(url_for("auth.getSignup"))
        else:
            try:
                # create new account
                newAccID = userInstance.generateID()
                newAcc = User(userID=newAccID, uname=name, password=generate_password_hash(
                    password).decode('utf-8'), alias=name if alias == None else alias, fname=None if firstname == None else firstname)
                db.session.add(newAcc)
                db.session.commit()
                _sendDNA(user_id=newAccID, pattern=session['dna'])

                flash("Your account has been created!", category='success')
                return redirect(url_for("auth.getLogin"))
            except Exception as e:
                flash(
                    f"Encounter error(s), couldn't create account, please try again<br>ERR: {e}", category='danger')
                return redirect(url_for("auth.getSignup"))

    return render_template("signup.html", user=current_user)
