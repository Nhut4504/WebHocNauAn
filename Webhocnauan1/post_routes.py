from flask import Blueprint, request, jsonify
from db import get_db_connection  # hoặc đường dẫn import phù hợp với project của bạn

post_api = Blueprint('post_api', __name__)

@post_api.route('/api/posts', methods=['GET'])
def get_posts():
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    cn.close()

    posts = []
    for row in rows:
        posts.append({
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "created_at": row[3].isoformat() if hasattr(row[3], 'isoformat') else str(row[3])
        })
    return jsonify(posts)

@post_api.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Missing title or content"}), 400

    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("INSERT INTO posts (title, content, created_at) VALUES (%s, %s, NOW())", (title, content))
    cn.commit()
    cur.close()
    cn.close()

    return jsonify({"message": "Post created successfully"}), 201
    