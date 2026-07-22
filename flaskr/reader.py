import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('reader', __name__, url_prefix='/reader')

@bp.route('', methods=(['GET']))
def show_reader_dashboard():
    reader_id = request.args.get('reader-id','')
    if reader_id:
        db = get_db()
        sessions_query = db.execute(
        """
            select s.name, se.created_at, se.status
            from session se
            left join sitter s on se.sitter_id = s.sitter_id
            where se.reader_id = ?
        """,
        (reader_id,)
        ).fetchall()
        sessions = [dict(row) for row in sessions_query]
        reader_query = db.execute('select name from reader where reader_id = ?',(reader_id,)).fetchone()
        if reader_query is None:
            return jsonify({'message':'Unable to locate reader with provided id'})
        reader_name = reader_query['name']
        return jsonify({
            'sessions':sessions, 
            'reader-name':reader_name
            })
    else:
        return jsonify({'message':'Reader not logged in'})

@bp.route('/manage-readers', methods=(['POST','GET','PATCH','DELETE']))
def manage_readers():
    request_method = request.method
    db = get_db()

    if request_method == 'POST':
        data = request.get_json()
        values = list(data.values())

        if len(values) < 4:
            return jsonify({'message':'Please include a name, bio, offering, and location'})

        try:
            db.execute(
            """
                INSERT INTO reader (name, bio, offering, location)
                VALUES (?,?,?,?)
            """,
            values
            )
            db.commit()
        except db.IntegrityError:
            return jsonify({'message':'Reader is already registered'})
        except Exception as e:
            print(f"Database error: {e}") 
            return jsonify({'message': f'Error: {str(e)}'}), 500

        return jsonify({'message':'Reader created successfully.'})
    elif request_method == 'GET':
        try:
            readers_query = db.execute(
            """
                select *
                from reader
            """
            ).fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        readers = [dict(row) for row in readers_query]
        return jsonify(readers)
    elif request_method == 'PATCH':
        data = request.get_json()
        reader_id = data.pop('reader-id','')
        columns = [f'"{col}" = ?' for col in data.keys()]
        set_clause = ", ".join(columns)
        values = list(data.values())
        values.append(reader_id)

        sql = f'update reader set {set_clause} where reader_id = ?'

        if not reader_id:
            return jsonify({'message':'Please provide a reader id.'})
        
        try:
            db.execute(sql, values)
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        return jsonify({'message':'reader updated successfully.'})
    elif request_method == 'DELETE':
        data = request.get_json()
        reader_id = data.get('reader-id','')

        if not reader_id:
            return jsonify({'message':'Please provide a reader id.'})

        try:
            db.execute('delete from reader where reader_id = ?',(reader_id,))
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        return jsonify({'message':'reader deleted successfully.'})
        
    else:
        return jsonify({'message':'This endpoint only accepts POST, GET, PATCH, and DELETE requests'})

@bp.route('/available-readers', methods=['GET'])
def get_available_readers():
    db = get_db()
    sql = """
        select r.name
        from reader r
        left join (
            select distinct r.name
            from reader r
            left join session s on r.reader_id = s.reader_id
            where s.status = 'In Progress'
        ) a on r.name = a.name
        where a.name is null;
    """
    available_readers_query = db.execute(sql).fetchall()
    available_readers = [r['name'] for r in available_readers_query]
    return jsonify(available_readers)