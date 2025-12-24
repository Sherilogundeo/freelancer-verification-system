from flask import jsonify, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from app import db
from app.blueprints.admin.models import SuperUser
from app.blueprints.auth.models import User
from app.utils.helpers import reset_password, send_reset_email, send_verification_email, verify_token
from . import auth_bp


# ----------------------------------------
# Register (Normal User)
# ----------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        form = request.form

        if User.get_by_username(form.get("username")):
            return render_template("register.html", error="Username already exists.")

        if User.get_by_email(form.get("email")):
            return render_template("register.html", error="Email already in use.")

        user = User(
            name=form.get("name"),
            username=form.get("username"),
            email=form.get("email"),
        )
        user.set_password(form.get("password"))
        user.save()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")
    

# ----------------------------------------
# Login (Normal User)
# ----------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.get_by_username(username)

        if user and user.check_password(password):
            login_user(user, remember=True)
            session["user_id"] = user.user_id
            next_page = request.args.get("next")

            flash("Logged in successfully!", "success")
            return redirect(next_page) if next_page else redirect(url_for("dashboard.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html")


# ----------------------------------------
# Create Admin (autocreate one if missing)
# ----------------------------------------
def ensure_admin():
    admin_email = "sherileidah@gmail.com"
    admin = SuperUser.get_by_email(admin_email)

    if not admin:
        admin = SuperUser(email=admin_email)
        admin.set_password("5240")
        admin.save()


# ----------------------------------------
# Admin Login
# ----------------------------------------
@auth_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    ensure_admin()

    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = SuperUser.get_by_email(email)

        if admin and admin.check_password(password):
            login_user(admin, remember=True)
            session["user_id"] = admin.super_id

            next_page = request.args.get("next")
            flash("Admin login success!", "success")
            return redirect(next_page) if next_page else redirect(url_for("admin.dashboard"))

        flash("Invalid login", "danger")

    return render_template("admin-login.html")


# ----------------------------------------
# Logout
# ----------------------------------------
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/admin-logout")
def admin_logout():
    session.pop("user_id", None)
    logout_user()
    flash("Admin logged out", "info")
    return redirect(url_for("auth.admin_login"))


@auth_bp.route("reset-password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        form = request.form
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        text = 'Email sent with instructions to resset password'
        flash(text, 'success')
    return render_template('reset-request.html', title='Reset Password')


@auth_bp.route("reset-password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('auth.reset_request'))
    if request.method == 'POST':
        form = request.form
        success, err = reset_password(form, user)
        if success:
            flash(f'Your password has been updated. You are now able to log in with your new password', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'Error resetting password: {err}', 'error')

    return render_template('reset-token.html', title='Reset Password')


@auth_bp.route("verify-email", methods=['GET', 'POST'])
def verify_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    if request.method == 'POST':
        form = request.form
        email = form.email.data
        user = User.query.filter_by(email=email)
        send_verification_email(user.user_id, email)
        flash(f'Email verification link send to {email}. Verify your email before login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('verify-request.html', title='Verify Email')


@auth_bp.route('verify-email/<token>')
def verify_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    title = 'Email Verified!'
    text = 'Your email has been verified. Redirecting to login...'
    icon = 'success'
    user = verify_token(token)
    if user:
        user.verified = True
        db.session.commit()
        flash(f'Your email has been verified. You are now able to log in', 'success')
    if not user:
        title = 'Email Verification Failed!'
        text = 'Token is invalid or expired'
        icon = 'warning'
        flash('Token is invalid or expired', 'warning')

    return render_template('verify-email.html', title='Verify Email', _title=title, text=text, icon=icon)

@auth_bp.route('get_user_details', methods=['GET'])
@login_required
def get_user():
    return jsonify(
        {
            "message": "User details", 
            "user_details": {
                "user_id": current_user.user_id,
                "username":current_user.username, 
                "email":current_user.email,
                "phone":current_user.phone,
                "profile": current_user.profile
            }
        }
    )