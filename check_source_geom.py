import psycopg2

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

def check_source_data():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 检查源表 wuhan_urban_renewal 的数据
        cur.execute("SELECT id, ST_AsText(geom) FROM wuhan_urban_renewal LIMIT 1;")
        row = cur.fetchone()
        
        if row:
            print(f"Source ID: {row[0]}")
            geom_wkt = row[1]
            print(f"Source Geom (First 100 chars): {geom_wkt[:100]}...")
            if len(geom_wkt) < 200:
                print("\n[分析] 源表数据也是简单的方形数据！")
            else:
                print("\n[分析] 源表数据看起来是真实的。")
        else:
            print("源表 wuhan_urban_renewal 中没有数据。")

    except Exception as e:
        print(f"数据库查询失败: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    check_source_data()
