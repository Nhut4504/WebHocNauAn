from flask import Blueprint, render_template, request, redirect, url_for
import psycopg2
from db import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Lấy danh sách món ăn từ bảng recipes
def get_recipes():
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("SELECT id, name, ingredients, instructions, image_url, ingredient_tips, video_url FROM recipes")
    recipes_list = cur.fetchall()
    cur.close()
    cn.close()
    return recipes_list

# Hiển thị danh sách món ăn từ bảng recipes
import requests

@admin_bp.route('/monan')
def list_monan():
    api_url = "http://localhost:5000/api/recipes"  # Đường dẫn API lấy danh sách món ăn
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        recipes_list = data.get("recipes", [])  # Lấy danh sách công thức
    else:
        recipes_list = []  # Nếu lỗi, trả về danh sách rỗng
    
    return render_template('admin/monan_list.html', monan=recipes_list)

# Thêm món ăn vào bảng recipes
@admin_bp.route('/monan/add', methods=['GET', 'POST'])
def add_monan():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image = request.form['image']
        ingredient_tips = request.form['ingredient_tips']
        video_url = request.form['video_url']
        
        cn = get_db_connection()
        cur = cn.cursor()
        cur.execute("INSERT INTO recipes (name, ingredients, instructions, image_url, ingredient_tips, video_url) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, ingredients, instructions, image, ingredient_tips, video_url))
        cn.commit()
        cur.close()
        cn.close()
        return redirect(url_for('admin.list_monan'))
    
    return render_template('admin/add_monan.html')

# Sửa món ăn trong bảng recipes
@admin_bp.route('/monan/edit/<int:id>', methods=['GET', 'POST'])
def edit_monan(id):
    cn = get_db_connection()
    cur = cn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # đảm bảo trả dict
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        image = request.form['image']
        ingredient_tips = request.form['ingredient_tips']
        video_url = request.form['video_url']   
       
        cur.execute("""
            UPDATE recipes
            SET name=%s, ingredients=%s, instructions=%s, image_url=%s,
                ingredient_tips=%s, video_url=%s
            WHERE id=%s
        """, (name, ingredients, instructions, image, ingredient_tips, video_url, id))
        cn.commit()
        cur.close()
        cn.close()
        return redirect(url_for('admin.list_monan'))
    
    cur.execute("SELECT id, name, ingredients, instructions, image_url, ingredient_tips, video_url FROM recipes WHERE id=%s", (id,))
    monan = cur.fetchone()
    cur.close()
    cn.close()
    return render_template('admin/edit_monan.html', monan=monan)


# Xóa món ăn trong bảng recipes
@admin_bp.route('/monan/delete/<int:id>', methods=['POST'])
def delete_monan(id):
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("DELETE FROM recipes WHERE id=%s", (id,))
    cn.commit()
    cur.close()
    cn.close()
    return redirect(url_for('admin.list_monan'))

# Hiển thị danh sách bài viết
@admin_bp.route('/post/list')
def list_posts():
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC")
    posts = cur.fetchall()
    cur.close()
    cn.close()
    return render_template('admin/post.html', posts=posts)

# Thêm bài viết
@admin_bp.route('/post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        cn = get_db_connection()
        cur = cn.cursor()
        cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        cn.commit()
        cur.close()
        cn.close()

        return redirect(url_for('admin.list_posts'))

    return render_template('admin/add_post.html')


