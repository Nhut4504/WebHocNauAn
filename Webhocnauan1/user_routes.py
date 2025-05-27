from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('user_bp', __name__)

# HTML ADMIN PANEL
@user_bp.route('/admin/users')
def manage_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, account, email, role FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin/manage_users.html', users=users)

@user_bp.route('/admin/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        full_name = request.form['full_name']
        account = request.form['account']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (full_name, account, password, email, role) VALUES (%s, %s, %s, %s, %s)",
                    (full_name, account, password_hash, email, role))
        conn.commit()
        cur.close()
        conn.close()

        flash('Người dùng đã được tạo!', 'success')
        return redirect(url_for('user_bp.manage_users'))
    
    return render_template('admin/create_users.html')

@user_bp.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        full_name = request.form['full_name']
        account = request.form['account']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password:
            if password != confirm_password:
                flash('Mật khẩu không khớp!', 'danger')
                return redirect(request.url)
            password_hash = generate_password_hash(password)
            cur.execute(
                "UPDATE users SET full_name = %s, account = %s, email = %s, role = %s, password = %s WHERE id = %s",
                (full_name, account, email, role, password_hash, user_id))
        else:
            cur.execute(
                "UPDATE users SET full_name = %s, account = %s, email = %s, role = %s WHERE id = %s",
                (full_name, account, email, role, user_id))

        conn.commit()
        cur.close()
        conn.close()

        flash('Thông tin người dùng đã được cập nhật!', 'success')
        return redirect(url_for('user_bp.manage_users'))

    cur.execute("SELECT id, full_name, account, email, role FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        flash('Không tìm thấy người dùng!', 'danger')
        return redirect(url_for('user_bp.manage_users'))

    user = {
        'id': row[0],
        'full_name': row[1],
        'account': row[2],
        'email': row[3],
        'role': row[4]
    }

    return render_template('admin/edit_users.html', user=user)

@user_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Người dùng đã bị xóa!', 'success')
    return redirect(url_for('user_bp.manage_users'))

# === REST API cho Postman ===

# Lấy danh sách người dùng
@user_bp.route('/api/users', methods=['GET'])
def api_get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, account, email, role FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {'id': u[0], 'full_name': u[1], 'account': u[2], 'email': u[3], 'role': u[4]}
        for u in users
    ])

# Tạo người dùng mới
@user_bp.route('/api/users', methods=['POST'])
def api_create_user():
    data = request.get_json()
    full_name = data.get('full_name')
    account = data.get('account')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not all([full_name, account, password, email, role]):
        return jsonify({'error': 'Thiếu dữ liệu'}), 400

    password_hash = password

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (full_name, account, password, email, role) VALUES (%s, %s, %s, %s, %s)",
                (full_name, account, password_hash, email, role))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Tạo người dùng thành công'}), 201

# Cập nhật người dùng
@user_bp.route('/api/user/<int:user_id>', methods=['PUT'])
def api_update_user(user_id):
    data = request.get_json()

    full_name = data.get('full_name')
    account = data.get('account')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    conn = get_db_connection()
    cur = conn.cursor()

    if password:
        cur.execute(
            "UPDATE users SET full_name = %s, account = %s, email = %s, role = %s, password = %s WHERE id = %s",
            (full_name, account, email, role, password, user_id)
        )
    else:
        cur.execute(
            "UPDATE users SET full_name = %s, account = %s, email = %s, role = %s WHERE id = %s",
            (full_name, account, email, role, user_id)
        )

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Cập nhật thành công!"}

# Xóa người dùng
@user_bp.route('/api/user/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Người dùng đã bị xóa!"}

