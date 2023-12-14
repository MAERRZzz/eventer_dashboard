from flask import Blueprint, render_template

errors_bp = Blueprint('errors', __name__, template_folder='templates')


@errors_bp.app_errorhandler(404)
def handle_404(err):
    return render_template('errors/page-404.html'), 404


@errors_bp.app_errorhandler(403)
def handle_500(err):
    return render_template('errors/page-403.html'), 403


@errors_bp.app_errorhandler(500)
def handle_500(err):
    return render_template('errors/page-500.html'), 500
