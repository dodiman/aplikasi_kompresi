import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash

# from aplikasi_kompresi.db import get_db

bp = Blueprint('aplikasiku', __name__, url_prefix='/')

@bp.route('/', methods=("GET", "POST"))
def halaman_utama():
    if request.method == 'POST':
        pass

    return render_template('halaman_utama.html')

@bp.route('/about', methods=["GET"])
def about():

    return render_template('about.html')

@bp.route('/info', methods=["GET"])
def info():

    return render_template('info.html')