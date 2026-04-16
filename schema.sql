-- schema.sql — 任務管理系統資料庫初始化腳本
-- 對應文件：docs/DB_DESIGN.md
-- 執行方式：
--   python -c "import sqlite3; conn=sqlite3.connect('instance/tasks.db'); conn.executescript(open('schema.sql').read()); conn.close()"

-- 建立 tasks 資料表
CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL CHECK(LENGTH(title) <= 200),
    is_done    INTEGER NOT NULL DEFAULT 0 CHECK(is_done IN (0, 1)),
    created_at TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%S', 'now', 'localtime'))
);
