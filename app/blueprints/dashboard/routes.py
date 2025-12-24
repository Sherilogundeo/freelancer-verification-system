import os
from flask import current_app, flash, jsonify, render_template, request
from flask_login import login_required, current_user

from app import db
from app.blueprints.dashboard.models import Project
from app.utils.helpers import save_picture, update_account

from . import dashboard_bp

@dashboard_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        form = request.form
        form_id = form.get("form_id")

        if form_id == "profile_edit_form":
            success, error = update_account(form)
            if success:
                flash("Profile updated")
            else:
                flash(f"Profile update failed: {error}")

        # elif form_id == "add_project_form":
        #     new_project = Project(
        #         title = form.get('title'),
        #         description = form.get('description'),
        #         user_id = current_user.user_id
        #     )
        #     new_project.save()
        #     flash("Project added successfully")
    projects = Project.query.filter_by(user_id = current_user.user_id)

    return render_template('dashboard.html', current_user=current_user, projects=projects)

@dashboard_bp.route("/upload_profile", methods=['POST'])
def upload_image():
    file = request.files.get('file')
    old_picture_filename = current_user.profile
    if file:
        picture_file = save_picture(file, old_picture_filename)
        current_user.profile = picture_file
        db.session.commit()
        return jsonify({'success': True, 'message': 'File uploaded successfully'})
    else:
        if old_picture_filename != 'default-avatar.png':
            old_picture_path = os.path.join(current_app.root_path, 'static/images/profile', old_picture_filename)
            if os.path.exists(old_picture_path):
                os.remove(old_picture_path)
        current_user.profile = 'default-avatar.png'
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile picture unlinked successfully'})

@dashboard_bp.route("/add-project", methods=["POST"])
def add_project():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title or not description:
        return jsonify({"message": "All fields required"}), 400

    new_project = Project(
        title = title,
        description = description,
        user_id = current_user.user_id
    )
    new_project.save()

    return jsonify(
        {
            "message": "Project details", 
            "project_details": {
                "title": title,
                "description": description
            }
        }
    )