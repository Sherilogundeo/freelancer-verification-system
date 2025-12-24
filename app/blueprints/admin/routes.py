from flask import abort, jsonify, render_template, request
from flask_login import login_required, current_user

from app import db
from app.blueprints.admin.models import SuperUser
from app.blueprints.auth.models import User

from . import admin_bp

@admin_bp.route('/admin')
@login_required
def dashboard():
    total_users = User.query.all()
    awaiting_users = User.query.filter(User.verified == False)
    verified_users = User.query.filter(User.verified == True)
    return render_template('admin.html', title='Admin Dashboard', admin_user=current_user, total_users=total_users, awaiting_users=awaiting_users, verified_users=verified_users)

@admin_bp.route("/verify-user", methods=["POST"])
def verify_user():
    user_id = request.json.get("id")
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False}), 404

    user.verified = True
    db.session.commit()

    return jsonify({"success": True})

@login_required
def admin_dashboard():
    if not isinstance(current_user._get_current_object(), SuperUser):
        return abort(403)
