from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__)

# 데이터베이스 초기화
def init_db():
    if not os.path.exists('fridge.db'):
        conn = sqlite3.connect('fridge.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# 데이터베이스 연결 함수
def get_db():
    conn = sqlite3.connect('fridge.db')
    conn.row_factory = sqlite3.Row
    return conn

# 앱 시작 시 데이터베이스 초기화
init_db()

@app.route('/')
def index():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    
    # 현재 날짜를 가져옵니다
    current_date = datetime.now().date()
    
    # 아이템들에 유통기한 상태 정보를 추가합니다
    items_with_status = []
    for item in items:
        item_dict = dict(item)
        expiry_date = datetime.strptime(item['expiry_date'], '%Y-%m-%d').date()
        item_dict['is_expired'] = expiry_date < current_date
        item_dict['days_left'] = (expiry_date - current_date).days
        items_with_status.append(item_dict)
    
    conn.close()
    return render_template('index.html', items=items_with_status)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO items (name, category, location, purchase_date, expiry_date, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            request.form['name'],
            request.form['category'],
            request.form['location'],
            request.form['purchase_date'],
            request.form['expiry_date'],
            int(request.form['quantity'])
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    selected_location = request.args.get('location', '')
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('add_item.html', 
                         today=today, 
                         datetime=datetime, 
                         timedelta=timedelta,
                         selected_location=selected_location)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update_quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    new_quantity = int(request.form['quantity'])
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/recipes')
def recipes():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT name FROM items')
    items = c.fetchall()
    
    # 재료 목록 추출
    ingredients = [item['name'] for item in items]
    
    # 여기서는 예시로 정적 레시피를 반환하지만,
    # 실제로는 외부 API를 사용하여 레시피를 검색할 수 있습니다
    sample_recipes = [
        {
            'title': f'재료로 만들 수 있는 레시피',
            'ingredients': ingredients,
            'search_url': f'https://www.10000recipe.com/recipe/list.html?q={"+".join(ingredients)}'
        }
    ]
    
    conn.close()
    return render_template('recipes.html', recipes=sample_recipes, ingredients=ingredients)

if __name__ == '__main__':
    app.run(debug=True) 