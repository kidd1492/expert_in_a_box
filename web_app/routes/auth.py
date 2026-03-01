# webapp/auth.py
from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # handle login
        return redirect(url_for('main.index'))
    return render_template('login.html')
