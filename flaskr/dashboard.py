import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('', methods=(['GET']))
def dashboard():
   db = get_db()
   lobby_data_query = db.execute(
    """
        select
            si.name AS 'Sitter',
            r.name AS 'Reader',
            r.offering AS 'Session Type',
            s.status AS 'Session Status'
        from session s
        left join reader r on s.reader_id = r.reader_id
        left JOIN sitter si on s.sitter_id = si.sitter_id
        where s.status != 'Done';
    """
    ).fetchall()
   lobby_data = [dict(row) for row in lobby_data_query]
   return jsonify(lobby_data)