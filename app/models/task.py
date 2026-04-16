"""
app/models/task.py — Task 資料模型

負責所有與 tasks 資料表相關的 CRUD 操作。
使用 Python 標準庫 sqlite3（依 ARCHITECTURE.md 決策 3）。
資料庫檔案路徑：instance/tasks.db
"""

import sqlite3
import os

# 資料庫檔案路徑（相對於專案根目錄）
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'tasks.db')


def _get_connection():
    """
    建立並回傳 SQLite 資料庫連線。
    設定 row_factory 使查詢結果可用欄位名稱存取（dict-like）。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 可用 row['column_name'] 存取
    return conn


# ──────────────────────────────────────────────
# CREATE — 新增任務
# ──────────────────────────────────────────────

def create_task(title: str) -> int:
    """
    新增一筆任務到資料庫。

    Args:
        title (str): 任務名稱（不可為空，長度上限 200 字元）

    Returns:
        int: 新增任務的 id

    Raises:
        ValueError: 若 title 為空字串或超過 200 字元
    """
    title = title.strip()
    if not title:
        raise ValueError("任務名稱不可為空白")
    if len(title) > 200:
        raise ValueError("任務名稱不可超過 200 個字元")

    conn = _get_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


# ──────────────────────────────────────────────
# READ — 查詢任務
# ──────────────────────────────────────────────

def get_all_tasks(filter: str = 'all') -> list[dict]:
    """
    取得任務清單，可依狀態篩選。

    Args:
        filter (str): 篩選條件，可為 'all'（預設）、'pending'、'done'

    Returns:
        list[dict]: 任務字典列表，每筆包含 id, title, is_done, created_at
    """
    conn = _get_connection()
    try:
        if filter == 'pending':
            rows = conn.execute(
                "SELECT * FROM tasks WHERE is_done = 0 ORDER BY created_at DESC"
            ).fetchall()
        elif filter == 'done':
            rows = conn.execute(
                "SELECT * FROM tasks WHERE is_done = 1 ORDER BY created_at DESC"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC"
            ).fetchall()
        # 將 sqlite3.Row 轉為一般 dict 以方便 Jinja2 使用
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_task_by_id(task_id: int) -> dict | None:
    """
    依 ID 取得單一任務。

    Args:
        task_id (int): 任務 ID

    Returns:
        dict | None: 任務資料字典，若不存在則回傳 None
    """
    conn = _get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_task_counts() -> dict:
    """
    取得任務統計數量（總數、待完成、已完成）。

    Returns:
        dict: {'total': int, 'pending': int, 'done': int}
    """
    conn = _get_connection()
    try:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = conn.execute("SELECT COUNT(*) FROM tasks WHERE is_done = 1").fetchone()[0]
        return {
            'total': total,
            'done': done,
            'pending': total - done,
        }
    finally:
        conn.close()


# ──────────────────────────────────────────────
# UPDATE — 更新任務
# ──────────────────────────────────────────────

def toggle_task(task_id: int) -> bool:
    """
    切換指定任務的完成狀態（0 → 1 或 1 → 0）。

    Args:
        task_id (int): 任務 ID

    Returns:
        bool: 操作是否成功（任務存在為 True，否則 False）
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "UPDATE tasks SET is_done = CASE WHEN is_done = 0 THEN 1 ELSE 0 END WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def update_task(task_id: int, title: str) -> bool:
    """
    更新指定任務的名稱。

    Args:
        task_id (int): 任務 ID
        title (str): 新的任務名稱

    Returns:
        bool: 操作是否成功

    Raises:
        ValueError: 若 title 為空或超過 200 字元
    """
    title = title.strip()
    if not title:
        raise ValueError("任務名稱不可為空白")
    if len(title) > 200:
        raise ValueError("任務名稱不可超過 200 個字元")

    conn = _get_connection()
    try:
        cursor = conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (title, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


# ──────────────────────────────────────────────
# DELETE — 刪除任務
# ──────────────────────────────────────────────

def delete_task(task_id: int) -> bool:
    """
    刪除指定的任務。

    Args:
        task_id (int): 任務 ID

    Returns:
        bool: 操作是否成功（任務存在並刪除為 True，否則 False）
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_all_done_tasks() -> int:
    """
    一鍵清除所有已完成的任務。

    Returns:
        int: 被刪除的任務筆數
    """
    conn = _get_connection()
    try:
        cursor = conn.execute("DELETE FROM tasks WHERE is_done = 1")
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
