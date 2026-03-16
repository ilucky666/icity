import psycopg2

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

def check_data():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 查询第一条记录的 geometry 文本格式，看看是不是复杂的形状
        cur.execute("SELECT id, unit_name, ST_AsText(geom) FROM wuhan_renewal_units LIMIT 1;")
        row = cur.fetchone()
        
        if row:
            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            geom_wkt = row[2]
            print(f"Geom (First 100 chars): {geom_wkt[:100]}...")
            
            # 简单的判断逻辑：Mock数据通常点很少，真实数据点很多
            if len(geom_wkt) < 200: 
                print("\n[分析] 几何数据看起来很简单，可能是 Mock 的方形数据。")
            else:
                print("\n[分析] 几何数据长度较长，可能是真实的复杂多边形。")
        else:
            print("表中没有数据。")

    except Exception as e:
        print(f"数据库查询失败: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    check_data()
