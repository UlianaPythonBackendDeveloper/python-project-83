import os
from datetime import datetime
from urllib.parse import urlparse
import psycopg
from psycopg.rows import dict_row
import validators
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages
)
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    # Использование dict_row позволяет получать результаты как словари
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    return conn


def normalize_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}".lower()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    input_url = request.form.get('url')
    
    # Валидация URL
    if not input_url or not validators.url(input_url) or len(input_url) > 255:
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=input_url), 422

    normalized = normalize_url(input_url)

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Проверяем, существует ли уже такой URL
            cur.execute("SELECT id FROM urls WHERE name = %s;", (normalized,))
            existing_url = cur.fetchone()

            if existing_url:
                flash('Страница уже существует', 'info')
                return redirect(url_for('get_url', id=existing_url['id']))

            # Если URL новый, сохраняем его
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id;",
                (normalized, datetime.now())
            )
            new_id = cur.fetchone()['id']
            conn.commit()
            
            flash('Страница успешно добавлена', 'success')
            return redirect(url_for('get_url', id=new_id))


@app.route('/urls/<int:id>')
def get_url(id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s;", (id,))
            url_data = cur.fetchone()

    if not url_data:
        return "Страница не найдена", 404

    return render_template('url_show.html', url=url_data)


@app.route('/urls')
def get_urls():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Сортируем так, чтобы новые записи были первыми (DESC)
            cur.execute("SELECT * FROM urls ORDER BY id DESC;")
            urls_list = cur.fetchall()

    return render_template('urls_list.html', urls=urls_list)