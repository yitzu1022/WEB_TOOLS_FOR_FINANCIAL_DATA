import psycopg2

# 設定 PostgreSQL 連線資訊
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mydb"
DB_USER = "test"
DB_PASSWORD = "mypassword"

try:
    # 連接 PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("成功連接到 PostgreSQL!")

    # 建立 Cursor 物件
    cur = conn.cursor()

    # 測試查詢資料庫版本
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL 版本: {version[0]}")

    # 關閉 cursor 和 connection
    cur.close()
    conn.close()

except Exception as e:
    print(f"連接失敗: {e}")
