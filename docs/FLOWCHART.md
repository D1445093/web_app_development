# FLOWCHART — 任務管理系統流程圖

> 版本：v1.0　　建立日期：2026-04-12　　對應 PRD：v1.0

---

## 1. 使用者流程圖（User Flow）

描述使用者從開啟網頁到完成各項操作的完整路徑。

```mermaid
flowchart LR
    Start([🌐 使用者開啟網頁]) --> Home[首頁\n顯示任務清單]

    Home --> Q{要執行什麼操作？}

    Q -->|新增任務| InputForm[填寫任務名稱]
    InputForm --> Validate{名稱是否為空？}
    Validate -->|是| ErrorMsg[顯示錯誤提示] --> InputForm
    Validate -->|否| AddTask[提交表單\nPOST /tasks/add]
    AddTask --> Home

    Q -->|標記完成| ToggleTask[點擊勾選按鈕\nPOST /tasks/toggle/:id]
    ToggleTask --> Home

    Q -->|刪除任務| ConfirmDelete{確認刪除？}
    ConfirmDelete -->|取消| Home
    ConfirmDelete -->|確認| DeleteTask[點擊刪除按鈕\nPOST /tasks/delete/:id]
    DeleteTask --> Home

    Q -->|篩選任務| Filter[點擊篩選標籤\n全部 / 待完成 / 已完成]
    Filter --> FilteredList[顯示篩選後清單]
    FilteredList --> Q
```

---

## 2. 系統序列圖（Sequence Diagram）

描述各操作在系統內部的完整資料流動過程。

### 2.1 新增任務

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 填寫任務名稱並點擊「新增」
    Browser->>Flask: POST /tasks/add（帶入 title 參數）
    Flask->>Flask: 驗證 title 不為空白
    alt 名稱為空
        Flask-->>Browser: 回傳錯誤提示訊息
        Browser-->>User: 顯示「請輸入任務名稱」
    else 名稱有效
        Flask->>Model: create_task(title)
        Model->>DB: INSERT INTO tasks (title, is_done) VALUES (?, 0)
        DB-->>Model: 新增成功
        Model-->>Flask: 回傳新任務 ID
        Flask-->>Browser: redirect("/")
        Browser-->>User: 重新載入首頁，顯示新任務
    end
```

---

### 2.2 標記任務完成 / 取消完成

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務旁的勾選按鈕
    Browser->>Flask: POST /tasks/toggle/:id
    Flask->>Model: toggle_task(id)
    Model->>DB: SELECT is_done FROM tasks WHERE id = ?
    DB-->>Model: 回傳目前狀態（0 或 1）
    Model->>DB: UPDATE tasks SET is_done = NOT is_done WHERE id = ?
    DB-->>Model: 更新成功
    Model-->>Flask: 回傳完成
    Flask-->>Browser: redirect("/")
    Browser-->>User: 重新載入頁面，任務狀態切換
```

---

### 2.3 刪除任務

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕
    Browser->>Flask: POST /tasks/delete/:id
    Flask->>Model: delete_task(id)
    Model->>DB: DELETE FROM tasks WHERE id = ?
    DB-->>Model: 刪除成功
    Model-->>Flask: 回傳完成
    Flask-->>Browser: redirect("/")
    Browser-->>User: 重新載入頁面，任務已消失
```

---

### 2.4 顯示任務清單（含篩選）

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 開啟首頁 或 點擊篩選標籤
    Browser->>Flask: GET /?filter=all | pending | done
    Flask->>Model: get_tasks(filter)
    alt filter = "pending"
        Model->>DB: SELECT * FROM tasks WHERE is_done = 0
    else filter = "done"
        Model->>DB: SELECT * FROM tasks WHERE is_done = 1
    else filter = "all"
        Model->>DB: SELECT * FROM tasks
    end
    DB-->>Model: 回傳任務資料列
    Model-->>Flask: 回傳任務列表
    Flask->>Browser: render_template("index.html", tasks=tasks)
    Browser-->>User: 顯示任務清單頁面
```

---

## 3. 功能清單對照表

| 功能 | HTTP 方法 | URL 路徑 | 說明 |
|------|-----------|----------|------|
| 顯示首頁（全部任務） | `GET` | `/` | 預設顯示所有任務 |
| 顯示首頁（篩選） | `GET` | `/?filter=pending` 或 `/?filter=done` | 篩選待完成或已完成 |
| 新增任務 | `POST` | `/tasks/add` | 表單送出後新增並重導向 |
| 標記完成／取消完成 | `POST` | `/tasks/toggle/<int:id>` | 切換 is_done 狀態 |
| 刪除任務 | `POST` | `/tasks/delete/<int:id>` | 刪除指定任務並重導向 |

> ⚠️ **為何刪除和標記都用 POST 而非 DELETE / PATCH？**
> HTML 表單原生只支援 `GET` 與 `POST`，為保持簡單、不依賴 JavaScript fetch，統一使用 `POST` 處理資料變更操作。

---

*本文件由 Antigravity AI Agent 根據 Flowchart Skill 自動產生，請團隊審閱後確認。*
