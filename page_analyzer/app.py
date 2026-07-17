import os
from flask import Flask, render_template  # Добавили импорт render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'placeholder-for-local-dev')

@app.route('/')
def index():
    # Отдаем отрендеренный HTML-шаблон
    return render_template('index.html')