import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('sitter', __name__, url_prefix='/sitter')

def create_sessions(sitter_id,reader_ids):
    db = get_db()
    new_sessions = []
    for reader_id in reader_ids:
        new_sessions.append((reader_id, sitter_id, 'Waiting'))
    try:
        db.executemany(
        """
            INSERT INTO session (reader_id, sitter_id, status)
            VALUES (?,?,?)
        """,
        (new_sessions)
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({'message':'User is already registered'})
    except Exception as e:
        print(f"Database error: {e}") 
        return jsonify({'message': f'Error: {str(e)}'}), 500

    return
    

@bp.route('/manage-sitters', methods=(['POST','GET','PATCH','DELETE']))
def manage_sitters():
    request_method = request.method
    db = get_db()

    if request_method == 'POST':
        data = request.get_json()
        sitter_name = data.get('name','')
        reader_list = data.get('reader-list',[])

        try:
            cursor = db.execute(
            """
                INSERT INTO sitter (name)
                VALUES (?)
            """,
            (sitter_name,)
            )
            db.commit()
        except db.IntegrityError:
            return jsonify({'message':'User is already registered'})
        except Exception as e:
            print(f"Database error: {e}") 
            return jsonify({'message': f'Error: {str(e)}'}), 500

        new_sitter_id = cursor.lastrowid
        create_sessions(new_sitter_id, reader_list)

        return jsonify({'message':'OK'})
    elif request_method == 'GET':
        try:
            sitters_query = db.execute(
            """
                select *
                from sitter
            """
            ).fetchall()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        sitters = [dict(row) for row in sitters_query]
        return jsonify(sitters)
    elif request_method == 'PATCH':
        data = request.get_json()
        sitter_id = data.pop('sitter-id','')
        columns = [f'"{col}" = ?' for col in data.keys()]
        set_clause = ", ".join(columns)
        values = list(data.values())
        values.append(sitter_id)

        sql = f'update sitter set {set_clause} where sitter_id = ?'

        if not sitter_id:
            return jsonify({'message':'Please provide a sitter id.'})
        
        try:
            db.execute(sql, values)
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        return jsonify({'message':'Sitter updated successfully.'})
    elif request_method == 'DELETE':
        data = request.get_json()
        sitter_id = data.get('sitter-id','')

        if not sitter_id:
            return jsonify({'message':'Please provide a sitter id.'})

        try:
            db.execute('delete from sitter where sitter_id = ?',(sitter_id,))
            db.commit()
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'message': f'Error: {str(e)}'}), 500
        
        return jsonify({'message':'Sitter deleted successfully.'})
        
    else:
        return jsonify({'message':'This endpoint only accepts POST, GET, PATCH, and DELETE requests'})