import psycopg2

DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

def clean_orphan_rows():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM wuhan_renewal_units WHERE id NOT IN (SELECT id FROM wuhan_urban_renewal);")
        count = cur.fetchone()[0]
        
        if count > 0:
            print(f"发现 {count} 条残留数据，正在删除...")
            cur.execute("DELETE FROM wuhan_renewal_units WHERE id NOT IN (SELECT id FROM wuhan_urban_renewal);")
            print(f"已删除 {cur.rowcount} 条数据。")
            conn.commit()
        else:
            print("没有发现残留数据，表结构同步正常。")

    except Exception as e:
        print(f"操作失败: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    clean_orphan_rows()
