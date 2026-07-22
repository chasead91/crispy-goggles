import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/reader-login', methods=(['POST']))
def user_login():
    data = request.get_json()
    username = data.get('username','')
    db = get_db()
    user_query = db.execute('select id,name from reader where name = ?',(username,)).fetchone()
    user = user_query['name'] or ''
    if user:
        user_id = user_query['id']
        return jsonify({'message':'Login successful', 'user-id':user_id})
    else:
        return {'message':'User unknown'}