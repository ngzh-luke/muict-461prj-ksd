""" account manager """
from flask import Blueprint, render_template, url_for, flash, request, redirect, session
from flask_login import current_user, login_required
from flask_bcrypt import generate_password_hash
from levelUP import db
from levelUP.dna import _sendDNA

acc = Blueprint('acc', __name__)


def commit():
    db.session.commit()


@acc.route("/")
@login_required
def getAccManager():
    return render_template("account.html", user=current_user, acc=current_user)


@acc.route("/edit/", methods=["POST"])
@login_required
def edit():
    try:
        user = current_user
        alias = request.form.get('alias')
        fname = request.form.get('firstname')
        newPswd = request.form.get("inputPassword")
        conNewPswd = request.form.get("inputPassword2")
        if newPswd != None:
            if newPswd != conNewPswd:
                flash("Passwords are not matched!", category='warning')

            elif newPswd == conNewPswd:
                newPswd = generate_password_hash(newPswd)
                user.password = newPswd
                if alias != None:
                    user.alias = alias
                if fname != None:
                    user.fname = fname
                commit()
                flash("Your changes have been updated!", category='success')
                return redirect(url_for("app.home"))

        else:
            flash("Something is incorrect!", category='error')
            return redirect(url_for("acc.getAccManager"))

    except ValueError:
        if (user.fname == fname) and (user.alias == alias):
            flash(message="No changes applied!", category='info')
            return redirect(url_for("app.home"))
        if alias != None:
            user.alias = alias
        if fname != None:
            user.fname = fname
        commit()
        flash("Your changes have been updated!", category='success')
        return redirect(url_for("app.home"))
    except Exception as e:

        flash(f"No changes applied.Encounter error:{e.__repr__()}",
              category='danger')
        return redirect(url_for("app.home"))
    finally:
        return redirect(url_for("app.home"))
    return render_template("account.html", user=current_user)


@acc.route("/delete-account/", methods=["POST"])
@login_required
def delAcc():
    try:
        session.clear()
        user = current_user
        db.session.delete(user)
        commit()
        _sendDNA(user_id=user.userID, delete=True, pattern=None)
        flash("Your account is deleted!", category='success')
        return redirect(url_for("auth.getLogin"))

    except Exception as e:

        flash(f"No changes applied.Encounter error:{e}",
              category='danger')
        return redirect(url_for("app.home"))
