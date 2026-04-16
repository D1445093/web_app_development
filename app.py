"""
app.py — 應用程式入口

啟動 Flask 開發伺服器。
執行方式：python app.py
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
