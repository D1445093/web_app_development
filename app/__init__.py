"""
app/__init__.py — Flask App 工廠函式

負責初始化 Flask 應用程式、設定 secret key、
確保 instance 資料夾存在，並註冊所有 Blueprint。
"""

import os
import sqlite3
from flask import Flask


def create_app():
    """
    Flask App 工廠函式。

    Returns:
        Flask: 初始化完成的 Flask 應用程式實例
    """
    app = Flask(__name__, instance_relative_config=True)

    # ── 基本設定 ──────────────────────────────
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['DATABASE'] = os.path.join(app.instance_path, 'tasks.db')

    # ── 確保 instance 資料夾存在 ──────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── 初始化資料庫（若尚未建立）────────────
    _init_db(app)

    # ── 註冊 Blueprint ────────────────────────
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    return app


def _init_db(app: Flask):
    """
    若資料庫尚未初始化，讀取 schema.sql 建立資料表。
    """
    db_path = app.config['DATABASE']
    schema_path = os.path.join(os.path.dirname(app.root_path), 'schema.sql')

    if not os.path.exists(db_path) and os.path.exists(schema_path):
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
