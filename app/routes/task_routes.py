"""
app/routes/task_routes.py — 任務管理路由骨架

所有任務相關的 Flask 路由，使用 Blueprint 組織。
Blueprint 名稱：'task'，無 URL prefix（首頁掛在根路徑）。

對應文件：docs/ROUTES.md
"""

from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from app.models.task import (
    create_task,
    get_all_tasks,
    get_task_counts,
    toggle_task,
    delete_task,
)

# 建立 Blueprint
task_bp = Blueprint('task', __name__)


# ──────────────────────────────────────────────
# GET / — 顯示任務清單（含篩選）
# ──────────────────────────────────────────────

@task_bp.route('/')
def index():
    """
    首頁：顯示任務清單。

    Query Parameters:
        filter (str): 篩選條件，可為 'all'（預設）、'pending'、'done'

    Context Variables:
        tasks  (list[dict]): 篩選後的任務列表
        counts (dict):       {'total': int, 'pending': int, 'done': int}
        filter (str):        目前篩選狀態

    Returns:
        render_template('index.html', ...)
    """
    pass


# ──────────────────────────────────────────────
# POST /tasks/add — 新增任務
# ──────────────────────────────────────────────

@task_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    接收表單送出的任務名稱，寫入資料庫後重導向回首頁。

    Form Fields:
        title (str): 任務名稱（必填，1–200 字元）

    On Success:
        redirect(url_for('task.index'))

    On Failure (title 為空或超長):
        flash 錯誤訊息，redirect 回首頁

    Returns:
        redirect(...)
    """
    pass


# ──────────────────────────────────────────────
# POST /tasks/toggle/<int:task_id> — 切換完成狀態
# ──────────────────────────────────────────────

@task_bp.route('/tasks/toggle/<int:task_id>', methods=['POST'])
def toggle_task_route(task_id):
    """
    切換指定任務的 is_done 狀態（0→1 或 1→0）。

    URL Parameters:
        task_id (int): 任務 ID（路徑參數）

    On Success:
        redirect(url_for('task.index'))

    On Failure (任務不存在):
        abort(404)

    Returns:
        redirect(...)
    """
    pass


# ──────────────────────────────────────────────
# POST /tasks/delete/<int:task_id> — 刪除任務
# ──────────────────────────────────────────────

@task_bp.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task_route(task_id):
    """
    永久刪除指定任務。

    URL Parameters:
        task_id (int): 任務 ID（路徑參數）

    On Success:
        redirect(url_for('task.index'))

    On Failure (任務不存在):
        abort(404)

    Returns:
        redirect(...)
    """
    pass
