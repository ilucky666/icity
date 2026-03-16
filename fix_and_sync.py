import psycopg2

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

def fix_and_sync():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("1. 修改列类型以支持 MultiPolygon...")
        # 将 geom 列类型修改为通用的 GEOMETRY，以兼容 Polygon 和 MultiPolygon
        # 注意：需要先删除类型约束（如果存在），或者直接转换
        cur.execute("""
            ALTER TABLE wuhan_renewal_units 
            ALTER COLUMN geom TYPE GEOMETRY(Geometry, 4326) 
            USING ST_Force2D(geom); -- 确保是二维的
        """)
        print("   列类型修改完成。")

        print("2. 再次执行数据同步...")
        cur.execute("""
            UPDATE wuhan_renewal_units target
            SET geom = source.geom
            FROM wuhan_urban_renewal source
            WHERE target.id = source.id;
        """)
        updated_count = cur.rowcount
        print(f"   已尝试更新 {updated_count} 行地理数据。")

        print("3. 验证更新结果 (ID=1)...")
        cur.execute("SELECT id, ST_GeometryType(geom), ST_AsText(geom) FROM wuhan_renewal_units WHERE id = 1;")
        row = cur.fetchone()
        if row:
            print(f"   ID: {row[0]}")
            print(f"   Type: {row[1]}")
            print(f"   Geom Snippet: {row[2][:50]}...")
        
        conn.commit()
        print("操作成功提交！")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"操作失败: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    fix_and_sync()
