import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@bp.route('/manage-sessions', methods=(['POST','GET','PATCH','DELETE']))
def manage_sessions():
    request_method = request.method
    db = get_db()

    if request_method == 'POST':
        data = request.get_json()
        values = list(data.values())

        if len(values) < 3:
            return jsonify({'message':'Please include a reader id, sitter id, and status'})

        try:
            db.execute(
            """
                INSERT INTO session (reader_id,sitter_id,status)
                VALUES (?,?,?)
            """,
            values
            )
            db.commit()
        except db.IntegrityError:
            return jsonify({'message':'session is already registered'})
        except Exception as e:
            print(f"Database error: {e}") 
            return jsonify({'message': f'Error: {str(e)}'}), 500

        return jsonify({'message':'session created successfully.'})
    elif request_method == 'GET':
        try:
            sessions_query = db.execute(
            """
                select
                    r.reader_id as 'reader-id',
                    r.name as 'reader-name',
                    s.sitter_id as 'sitter-id',
                    s.name as 'sitter-name',
                    se.created_at as 'created-at',
                    r.offering as 'session-type',
                    se.status,
                    r.location,
                    se.session_id
                from session se
                left join reader r on se.reader_id = r.reader_id
                left join sitter s on se.sitter_id = s.sitter_id
            """
            ).fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        sessions = [dict(row) for row in sessions_query]
        return jsonify(sessions)
    elif request_method == 'PATCH':
        data = request.get_json()
        print(f'Data received at endpoint: {data}')
        session_id = data.pop('session-id','')
        columns = [f'"{col}" = ?' for col in data.keys()]
        set_clause = ", ".join(columns)
        values = list(data.values())
        values.append(session_id)

        sql = f'update session set {set_clause} where session_id = ?'

        if not session_id:
            return jsonify({'message':'Please provide a session id.'})
        
        try:
            db.execute(sql, values)
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        try:
            sessions_query = db.execute(
            """
                select
                    r.reader_id as 'reader-id',
                    r.name as 'reader-name',
                    s.sitter_id as 'sitter-id',
                    s.name as 'sitter-name',
                    se.created_at as 'created-at',
                    r.offering as 'session-type',
                    r.location,
                    se.status,
                    se.session_id
                from session se
                left join reader r on se.reader_id = r.reader_id
                left join sitter s on se.sitter_id = s.sitter_id
            """
            ).fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        sessions = [dict(row) for row in sessions_query]
        return jsonify({'session_data':sessions, 'message':'Session updated successfully'}), 200
    elif request_method == 'DELETE':
        data = request.get_json()
        session_id = data.get('session-id','')

        if not session_id:
            return jsonify({'message':'Please provide a session id.'})

        try:
            db.execute('delete from session where session_id = ?',(session_id,))
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        return jsonify({'message':'session deleted successfully.'})
        
    else:
        return jsonify({'message':'This endpoint only accepts POST, GET, PATCH, and DELETE requests'})