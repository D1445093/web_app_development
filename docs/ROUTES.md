# ROUTES — 任務管理系統路由設計

> 版本：v1.0　　建立日期：2026-04-16　　對應 PRD：v1.0 / DB_DESIGN：v1.0

---

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 顯示任務清單 | `GET` | `/` | `templates/index.html` | 首頁，顯示所有任務，可帶 `?filter=` 參數篩選 |
| 顯示篩選清單 | `GET` | `/?filter=pending` 或 `/?filter=done` | `templates/index.html` | 同一模板，依 query string 篩選待完成或已完成 |
| 新增任務 | `POST` | `/tasks/add` | — | 接收表單 `title`，寫入 DB，重導向到 `/` |
| 切換完成狀態 | `POST` | `/tasks/toggle/<int:id>` | — | 切換指定任務的 `is_done`，重導向到 `/` |
| 刪除任務 | `POST` | `/tasks/delete/<int:id>` | — | 刪除指定任務，重導向到 `/` |

> ⚠️ 依 ARCHITECTURE.md 決策 2：所有資料變更操作統一使用 `POST`（HTML 表單不支援 DELETE/PATCH）。

---

## 2. 每個路由詳細說明

### 2.1 `GET /` — 顯示任務清單（含篩選）

| 項目 | 內容 |
|------|------|
| **Blueprint** | `task_bp` |
| **函式名稱** | `index()` |
| **URL 參數** | `filter`（query string，選填）：`all`（預設）、`pending`、`done` |
| **表單欄位** | 無 |
| **Model 呼叫** | `get_all_tasks(filter)`、`get_task_counts()` |
| **輸出** | `render_template("index.html", tasks=tasks, counts=counts, filter=filter)` |
| **錯誤處理** | `filter` 值無效時預設為 `all` |

---

### 2.2 `POST /tasks/add` — 新增任務

| 項目 | 內容 |
|------|------|
| **Blueprint** | `task_bp` |
| **函式名稱** | `add_task()` |
| **URL 參數** | 無 |
| **表單欄位** | `title`（必填，`request.form['title']`） |
| **Model 呼叫** | `create_task(title)` |
| **輸出（成功）** | `redirect(url_for('task.index'))` |
| **輸出（失敗）** | 重導向回首頁並帶 `error` flash 訊息（title 為空或超長） |
| **錯誤處理** | `title.strip()` 為空 → flash 錯誤提示；`ValueError` → flash 錯誤提示 |

---

### 2.3 `POST /tasks/toggle/<int:id>` — 切換完成狀態

| 項目 | 內容 |
|------|------|
| **Blueprint** | `task_bp` |
| **函式名稱** | `toggle_task(task_id)` |
| **URL 參數** | `task_id`（int，路徑參數） |
| **表單欄位** | 無 |
| **Model 呼叫** | `toggle_task(task_id)` |
| **輸出（成功）** | `redirect(url_for('task.index'))` |
| **輸出（失敗）** | `abort(404)`（任務不存在） |
| **錯誤處理** | Model 回傳 `False` 時 → `abort(404)` |

---

### 2.4 `POST /tasks/delete/<int:id>` — 刪除任務

| 項目 | 內容 |
|------|------|
| **Blueprint** | `task_bp` |
| **函式名稱** | `delete_task(task_id)` |
| **URL 參數** | `task_id`（int，路徑參數） |
| **表單欄位** | 無 |
| **Model 呼叫** | `delete_task(task_id)` |
| **輸出（成功）** | `redirect(url_for('task.index'))` |
| **輸出（失敗）** | `abort(404)`（任務不存在） |
| **錯誤處理** | Model 回傳 `False` 時 → `abort(404)` |

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 說明 |
|----------|--------|------|
| `app/templates/base.html` | — | 基底模板：`<head>`、CSS/JS 引入、共用 nav |
| `app/templates/index.html` | `base.html` | 首頁：任務新增表單 + 篩選標籤 + 任務清單 |

**`index.html` 需要的 Jinja2 變數：**

| 變數 | 型別 | 說明 |
|------|------|------|
| `tasks` | `list[dict]` | 任務列表（依 filter 篩選後） |
| `counts` | `dict` | `{'total': int, 'pending': int, 'done': int}` |
| `filter` | `str` | 目前篩選狀態（`all` / `pending` / `done`） |
| `error` | `str` (flash) | 驗證失敗時的錯誤訊息（透過 Flask flash） |

---

## 4. Blueprint 與 URL prefix 設計

```python
# app/routes/task_routes.py
task_bp = Blueprint('task', __name__)

# 首頁路由掛在根路徑
app.register_blueprint(task_bp)        # prefix 為空，index 對應 "/"
```

| Blueprint 名稱 | prefix | endpoint 前綴 |
|----------------|--------|---------------|
| `task_bp` | `""` (無) | `task.` |

---

## 5. 路由骨架程式碼位置

| 檔案 | 說明 |
|------|------|
| `app/routes/__init__.py` | 套件初始化 |
| `app/routes/task_routes.py` | 所有任務相關路由（Blueprint） |
| `app/__init__.py` | Flask app 工廠、Blueprint 註冊 |
| `app.py` | 應用程式入口 |

---

*本文件由 Antigravity AI Agent 根據 API Design Skill 自動產生，請團隊審閱後確認。*
