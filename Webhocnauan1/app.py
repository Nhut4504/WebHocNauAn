import os
from flask import Blueprint, Flask, flash, render_template, request, jsonify, redirect, url_for, session
import openai
import google.generativeai as genai
from db import get_categories, getHocnauans, getHocnauan, getRecipeSteps, getRecipes, login, register_user
from flask_cors import CORS # type: ignore
from admin_routes import admin_bp  # Import blueprint từ admin_routes.py
from user_routes import user_bp # Import blueprint quản lý người dùng
from post_routes import post_api
from werkzeug.utils import secure_filename

import psycopg2

app = Flask(__name__, static_folder="static")
genai.configure(api_key="AIzaSyDbYbmj0TWNvW0lTcXIa4-jQOEF_2N0mu4")
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
app.secret_key = "00c9b72559b5bb8f20c049baabf45238"
openai.api_key = ""
CORS(app)  # Cho phép CORS để gọi API từ Postman hoặc frontend

def get_db_connection():
    try:
        conn = psycopg2.connect(database="Hocnauan1", user="postgres", password="123", host="localhost", port="5432")
        return conn
    except Exception as e:
        print("Lỗi kết nối DB:", e)  # In lỗi ra terminal
        return None
    
@app.route('/')
@app.route('/home')
def home_index():
    if 'user' not in session:
        return redirect(url_for('login_index'))
    
    search_query = request.args.get('search', '').strip()
    recipes = getRecipes(search_query)

    print("DEBUG - Recipes:", recipes)  # Kiểm tra dữ liệu

    return render_template('home/index.html', recipes=recipes)

@app.route('/login', methods=['GET', 'POST'])
def login_index():
    """Xử lý đăng nhập"""
    error = None
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        user = login(account, password)

        if user and isinstance(user, dict):
            session['user'] = user['account']
            session['user_id'] = user['id']
            session['role'] = user['role']

            if user['role'] == 'admin':
                return redirect(url_for('admin.add_monan', _external=True))
            else:
                return redirect(url_for('home_index'))
        
        error = "Sai tài khoản hoặc mật khẩu!"

    return render_template('home/login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        full_name = data.get('full_name')
        account = data.get('account')
        password = data.get('password')
        email = data.get('email')

        if register_user(full_name, account, password, email):
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Tài khoản hoặc email đã tồn tại!"})

    return render_template('home/register.html')

@app.route('/home/products')
def product_list():
    category_id = request.args.get('category')
    search_query = request.args.get('search', '').strip()

    try:
        category_id = int(category_id) if category_id else None
    except ValueError:
        category_id = None

    products = getHocnauans(search_query, category_id)
    categories = get_categories()

    return render_template('home/products.html', products=products, categories=categories, search_query=search_query)

@app.route('/home/post', methods=['GET', 'POST'])
def home_post():
    cn = get_db_connection()
    cur = cn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session.get('user_id')

        if not user_id:
            return "Bạn chưa đăng nhập", 401

        image = request.files.get('image')
        image_path = None

        if image and image.filename != '':
            filename = secure_filename(image.filename)
            upload_folder = 'static/uploads'
            os.makedirs(upload_folder, exist_ok=True)
            image.save(os.path.join(upload_folder, filename))
            image_path = f'uploads/{filename}'  # path tương đối

        cur.execute(
            "INSERT INTO posts (title, content, user_id, image_path) VALUES (%s, %s, %s, %s)",
            (title, content, user_id, image_path)
        )
        cn.commit()
        return redirect(url_for('home_post'))  # Tránh close quá sớm

    # Xử lý GET: lấy danh sách bài viết
    cur.execute("""
        SELECT posts.title, posts.content, posts.created_at, posts.image_path, users.account
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
    """)
    posts = []
    for row in cur.fetchall():
        posts.append({
            'title': row[0],
            'image_url': row[3],
            'content': row[1],
            'created_at': row[2],
            'account': row[4]
        })

    cur.close()
    cn.close()

    return render_template('home/post.html', posts=posts)


@app.route('/admin/post', methods=['GET', 'POST'])
def admin_add_post():
    cn = get_db_connection()
    cur = cn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = 1  # Mặc định admin

        cur.execute(
            "INSERT INTO posts (title, content, user_id, image_path) VALUES (%s, %s, %s)",
            (title, content, user_id)
        )
        cn.commit()
        cur.close()
        cn.close()
        return redirect(url_for('admin.list_posts'))

    return render_template('admin/add_post.html')

@app.route('/admin/post/delete/<int:post_id>', methods=['POST'])
def admin_delete_post(post_id):
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    cn.commit()
    cur.close()
    cn.close()
    return redirect(url_for('admin.list_posts'))  

@app.route('/home/products_details/<int:id>')
def product_details(id):
    data = getHocnauan(id)
    recipe_steps = getRecipeSteps(id)

    print("DEBUG - product:", data)
    print("DEBUG - recipe_steps:", recipe_steps)

    if data is None:
        return "Không tìm thấy sản phẩm", 404
    
    return render_template('home/products_details.html', product=data, recipe_steps=recipe_steps)

@app.route('/recipes/<int:id>')
def recipe_detail(id):
    conn = get_db_connection()
    if not conn:
        return "Lỗi kết nối cơ sở dữ liệu", 500

    cur = conn.cursor()
    cur.execute("SELECT id, name, ingredients, instructions, image_url, ingredient_tips, video_url FROM recipes WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        recipe = {
            'id': row[0],
            'name': row[1],
            'ingredients': row[2],
            'instructions': row[3],
            'image_url': row[4],
            'ingredient_tips': row[5],
            'video_url': row[6]
        }
        return render_template('home/recipe_detail.html', recipe=recipe)
    else:
        return "Không tìm thấy món ăn", 404

@app.template_filter('nl2br')
def nl2br_filter(s):
    return s.replace('\n', '<br>\n') if s else ''

@app.template_filter('youtube_embed')
def youtube_embed(url):
    if 'watch?v=' in url:
        return url.replace("watch?v=", "embed/")
    return url

@app.route('/home/contact')
def contact_page():
    return render_template('home/contact.html')

@app.route('/api/contact', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    print(f"Liên hệ từ {name} - {email} - {phone}: {message}")
    return redirect('/home/contact')

def chat_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# Trang giao diện chatbot
@app.route("/chatbot")
def chatbot_page():
    return render_template("home/chat.html")

# API xử lý chat
@app.route("/chat_api", methods=["POST"])
def chat_api():
    data = request.get_json()
    prompt = data.get("message", "")
    if not prompt:
        return jsonify({"response": "Bạn chưa nhập câu hỏi!"})
    
    response = model.generate_content(prompt)
    return jsonify({"response": response.text})

### API LẤY DANH SÁCH MÓN ĂN ###
@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Không thể kết nối DB"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM recipes")
        recipes = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"recipes": recipes})
    except Exception as e:
        print("Lỗi SQL:", e)
        return jsonify({"error": "Lỗi truy vấn DB"}), 500
    

recipes = []  # Danh sách công thức

@app.route("/api/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dữ liệu không hợp lệ"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO recipes (name, ingredients, instructions, image_url, ingredient_tips, video_url) VALUES (%s, %s, %s, %s, %s, %s)",
        (data["name"], data["ingredients"], data["instructions"], data["image"], data["ingredient_tips"], data["video"])
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Thêm công thức thành công!"}), 201

        
### API LẤY CHI TIẾT MÓN ĂN ###
@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
    recipe = cur.fetchone()
    cur.close()
    conn.close()
    if recipe:
        return jsonify({"recipe": recipe})
    return jsonify({"error": "Recipe not found"}), 404

### API CẬP NHẬT MÓN ĂN ###
@app.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE recipes SET name = %s, ingredients = %s, instructions = %s, ingredient_tips = %s, video_url = %s WHERE id = %s", 
                (data['name'], data['ingredients'], data['instructions'], data['ingredient_tips'], data['video_url'], recipe_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Recipe updated"})

### API XÓA MÓN ĂN ###
@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Recipe deleted"})

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'user' not in session:
        return jsonify({"error": "Chưa đăng nhập!"}), 401
    
    account = session['user']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT full_name, account, email, role FROM users WHERE account = %s", (account,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({
            "user": {
                "full_name": user[0],
                "account": user[1],
                "email": user[2],
                "role": user[3]
            }
        })
    return jsonify({"error": "Không tìm thấy người dùng"}), 404

@app.route('/api/user', methods=['PUT'])
def update_user():
    if 'user' not in session:
        return jsonify({"error": "Chưa đăng nhập!"}), 401

    data = request.json
    full_name = data.get('full_name')
    email = data.get('email')

    if not full_name or not email:
        return jsonify({"error": "Thông tin không hợp lệ!"}), 400
    
    account = session['user']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET full_name = %s, email = %s WHERE account = %s", 
                (full_name, email, account))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Thông tin tài khoản đã được cập nhật!"})

@app.route('/api/user', methods=['DELETE'])
def delete_user():
    if 'user' not in session:
        return jsonify({"error": "Chưa đăng nhập!"}), 401

    account = session['user']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE account = %s", (account,))
    conn.commit()
    cur.close()
    conn.close()

    session.pop('user', None)  # Đăng xuất người dùng ngay lập tức

    return jsonify({"message": "Tài khoản đã được xóa!"})

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Không thể kết nối DB"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, full_name, account, email, role FROM users")
        users = cur.fetchall()
        cur.close()
        conn.close()

        # Chuyển đổi danh sách người dùng thành định dạng JSON
        users_list = []
        for user in users:
            users_list.append({
                "id": user[0],
                "full_name": user[1],
                "account": user[2],
                "email": user[3],
                "role": user[4]
            })

        return jsonify({"users": users_list})

    except Exception as e:
        print("Lỗi truy vấn DB:", e)
        return jsonify({"error": "Lỗi truy vấn DB"}), 500
    

from post_routes import post_api

# ĐĂNG KÝ BLUEPRINT SAU KHI ĐÃ ĐỊNH NGHĨA ROUTE
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(post_api)

if __name__ == '__main__':
    app.run(debug=True)
