import psycopg2

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

def sync_data():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 1. 检查新表是否存在
        cur.execute("SELECT to_regclass('public.wuhan_urban_renewal');")
        if cur.fetchone()[0] is None:
            print("错误：新表 'wuhan_urban_renewal' 不存在！请确认表名是否正确。")
            return

        # 2. 检查 ID 重叠情况 (可选，为了安全)
        cur.execute("SELECT COUNT(*) FROM wuhan_renewal_units WHERE id IN (SELECT id FROM wuhan_urban_renewal);")
        overlap_count = cur.fetchone()[0]
        print(f"检测到 {overlap_count} 个 ID 匹配的项目。")

        if overlap_count == 0:
            print("警告：没有发现匹配的 ID！操作已取消，以免误删所有数据。请确认两个表的 id 字段确实对应。")
            return

        # 3. 删除旧表中多余的行 (即 ID 不在新表中的行)
        print("正在删除旧表中多余的行...")
        cur.execute("""
            DELETE FROM wuhan_renewal_units
            WHERE id NOT IN (SELECT id FROM wuhan_urban_renewal);
        """)
        deleted_count = cur.rowcount
        print(f"已删除 {deleted_count} 行不在新表中的数据。")

        # 4. 更新地理数据
        # 假设新表的几何字段名为 geom。如果不是，可能会报错。
        # 这里尝试动态获取几何字段名会更稳健，但先试 geom。
        print("正在从新表同步地理数据...")
        try:
            cur.execute("""
                UPDATE wuhan_renewal_units target
                SET geom = source.geom
                FROM wuhan_urban_renewal source
                WHERE target.id = source.id;
            """)
            updated_count = cur.rowcount
            print(f"已更新 {updated_count} 行地理数据。")
        except psycopg2.Error as e:
            print(f"更新地理数据失败，可能是列名不匹配: {e}")
            conn.rollback()
            return

        conn.commit()
        print("数据同步成功完成！")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"数据库操作发生异常: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    sync_data()
