import bcrypt
from psycopg2 import connect, extras

# Cấu hình kết nối database
DB_CONFIG = {
    "database": "Hocnauan1",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": 5432
}

def get_db_connection():
    """Kết nối đến PostgreSQL"""
    return connect(**DB_CONFIG)

def getHocnauans(search_query=None, category_id=None):
    """Lấy danh sách sản phẩm, hỗ trợ tìm kiếm và lọc theo danh mục"""
    cn = get_db_connection()
    cur = cn.cursor()

    sql = "SELECT * FROM product WHERE 1=1"
    params = []

    if search_query:
        sql += " AND LOWER(productname) LIKE %s"
        params.append(f"%{search_query.lower()}%")

    if category_id:
        sql += " AND categoryid = %s"
        params.append(category_id)

    sql += " ORDER BY productid ASC"
    
    cur.execute(sql, tuple(params))
    arr = cur.fetchall()
    cur.close()
    cn.close()
    
    return [{'productid': v[0], 'categoryid': v[1], 'productname': v[2], 'imageurl': v[3], 'note': v[4], 'rating': v[5]} for v in arr]

def getHocnauan(id):
    """Lấy chi tiết món ăn theo ID"""
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("SELECT productid, productname, imageurl, note, rating, ingredient_tips, instructions FROM product WHERE productid = %s", (id,))
    v = cur.fetchone()
    cur.close()
    cn.close()
    if v:
        return {
            'productid': v[0], 
            'productname': v[1], 
            'imageurl': v[2], 
            'note': v[3], 
            'rating': v[4], 
            'ingredient_tips': v[5], 
            'instructions': v[6]
        }
    return None

def getRecipeSteps(product_id):
    """Lấy danh sách các bước nấu ăn"""
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute("SELECT step_number, instruction, image_url, video_url FROM recipe_steps WHERE product_id = %s ORDER BY step_number", (str(product_id),))
    steps = cur.fetchall()
    cur.close()
    cn.close()

    return [{'step': s[0], 'instruction': s[1], 'image_url': s[2], 'video_url': s[3]} for s in steps]

def getRecipes(search_query=None):
    """Lấy danh sách công thức món ăn, hỗ trợ tìm kiếm theo tên"""
    cn = get_db_connection()
    cur = cn.cursor()

    sql = "SELECT id, name, ingredients, instructions, image_url, ingredient_tips, video_url FROM recipes WHERE 1=1"
    params = []

    if search_query:
        sql += " AND LOWER(name) LIKE %s"
        params.append(f"%{search_query.lower()}%")

    sql += " ORDER BY id ASC"

    cur.execute(sql, tuple(params))
    arr = cur.fetchall()
    cur.close()
    cn.close()

    return [{'id': r[0], 'name': r[1], 'ingredients': r[2], 'instructions': r[3], 'image_url': r[4], 'ingredient_tip': r[5], 'video_url': r[6]} for r in arr]



def hash_password(password):
    """Hash mật khẩu trước khi lưu"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(stored_password, provided_password):
    """So sánh mật khẩu nhập vào với mật khẩu đã hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def login(account, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, account, email, role FROM users WHERE account = %s AND password = %s", (account, password))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return {
            "id": user[0],
            "full_name": user[1],
            "account": user[2],
            "email": user[3],
            "role": user[4]
        }
    return None

def register_user(full_name, account, password, email):
    """Đăng ký người dùng mới, lưu mật khẩu thô"""
    cn = get_db_connection()
    cur = cn.cursor()
    try:
        # Kiểm tra tài khoản hoặc email đã tồn tại chưa
        cur.execute("SELECT 1 FROM users WHERE account = %s OR email = %s", (account, email))
        if cur.fetchone():
            return False  # Tài khoản hoặc email đã tồn tại

        # Tiến hành đăng ký nếu chưa trùng
        cur.execute(
            "INSERT INTO users (full_name, account, password, email, role) VALUES (%s, %s, %s, %s, %s)", 
            (full_name, account, password, email, 'user')
        )
        cn.commit()
        return True
    except Exception as e:
        print("Lỗi đăng ký:", e)
        return False
    finally:
        cur.close()
        cn.close()

def get_categories():
    """Lấy danh sách danh mục từ database"""
    cn = get_db_connection()
    cur = cn.cursor()
    cur.execute('SELECT categoryid, categoryname FROM category ORDER BY categoryid ASC')
    arr = cur.fetchall()
    cur.close()
    cn.close()
    return [{'categoryid': v[0], 'categoryname': v[1]} for v in arr]

