import psycopg2
import math

# 数据库连接配置
DB_CONFIG = {
    'dbname': 'wuhan_gis',
    'user': 'postgres',
    'password': '1',
    'host': 'localhost',
    'port': '5432'
}

# 从图像中提取的结构化数据集
RENEWAL_DATA = [
    # 强功能单元
    {"name": "汉口数智谷(岱山)", "category": "强功能单元", "desc": "聚焦数字经济与智慧城市产业，打造汉口北部产业核心。", "industry": "数字经济"},
    {"name": "汉口滨江商务区片(七期)", "category": "强功能单元", "desc": "沿江商务带延伸，主打总部经济与金融服务。", "industry": "总部经济"},
    {"name": "杨园设计产业片", "category": "强功能单元", "desc": "依托铁路与工程设计院所，构建世界级工程设计之都核心区。", "industry": "工程设计"},
    {"name": "汉正街中央服务区片(江汉区)", "category": "强功能单元", "desc": "传统商贸转型升级，打造现代商贸与跨境电商枢纽。", "industry": "现代商贸"},
    {"name": "汉正街中央服务区片(硚口区)", "category": "强功能单元", "desc": "商贸物流供应链升级，承接汉正街产业外溢。", "industry": "现代供应链"},
    {"name": "白沙洲科创片", "category": "强功能单元", "desc": "激活武昌南大门，布局智能制造与科技创新转化。", "industry": "科技转化"},
    {"name": "街道口大学之城片", "category": "强功能单元", "desc": "依托武大华科等高校智力资源，发展环高校知识经济带。", "industry": "知识经济"},
    {"name": "南湖创智街区片", "category": "强功能单元", "desc": "南湖片区产城融合示范点，聚焦信息技术服务。", "industry": "信息技术"},
    
    # 补短板单元
    {"name": "华安里环境提升片", "category": "补短板单元", "desc": "城中村及老旧小区环境综合整治，补齐公共服务设施短板。", "industry": "民生保障"},
    {"name": "武汉天地商圈时尚片", "category": "补短板单元", "desc": "优化商圈周边交通微循环与公共空间品质。", "industry": "高端消费"},
    {"name": "澳门金角公园片(周边坊)", "category": "补短板单元", "desc": "街角空间梳理与绿化提升，打造城市口袋公园网络。", "industry": "生态游憩"},
    {"name": "三阳设计之都片", "category": "补短板单元", "desc": "历史街区基础设施改造，为设计产业入驻提供高品质底座。", "industry": "创意设计"},
    {"name": "西北湖金融时尚片", "category": "补短板单元", "desc": "环湖慢行系统打通及老旧商业楼宇外立面焕新。", "industry": "现代金融"},
    {"name": "万松精致生活片", "category": "补短板单元", "desc": "提升居住区内部第三空间，打造15分钟高品质生活圈。", "industry": "生活服务"},
    {"name": "武车国际社区片", "category": "补短板单元", "desc": "工业遗址周边的国际化社区配套完善工程。", "industry": "国际交往"},
    {"name": "崇仁健康生活片", "category": "补短板单元", "desc": "依托医疗资源，完善大健康产业链及周边适老化改造。", "industry": "大健康"},
    {"name": "汉西古四商贸片", "category": "补短板单元", "desc": "传统建材市场腾退与环境治理，植入新商业业态。", "industry": "商贸服务"},
    {"name": "王家湾北全龄友好片", "category": "补短板单元", "desc": "全周期社区建设，补齐儿童及适老化公共设施。", "industry": "社区服务"},
    {"name": "青山绿润片", "category": "补短板单元", "desc": "青山老工业区生态修复与重金属污染土壤治理。", "industry": "生态治理"},

    # 显特色单元
    {"name": "武汉CBD未来社区片", "category": "显特色单元", "desc": "CBD商务区配套的未来社区数字化与低碳化场景应用。", "industry": "低碳生活"},
    {"name": "汉阳古城融合片", "category": "显特色单元", "desc": "归元寺至汉阳树片区的文脉梳理与历史场景复原。", "industry": "文化旅游"},
    {"name": "环墨水湖湖韵片", "category": "显特色单元", "desc": "挖掘湖泊文化，打造汉阳生态与文化融合的滨水空间。", "industry": "生态旅游"},
    {"name": "鹦鹉邻里生活片", "category": "显特色单元", "desc": "知音文化传承，打造具有高识别度的特色邻里中心。", "industry": "文化社交"},
    {"name": "武昌古城得胜桥古轴片", "category": "显特色单元", "desc": "武昌古城千年轴线复兴，黄鹤楼视觉廊道保护与文创开发。", "industry": "文化创意"},
    {"name": "华中音乐谷片", "category": "显特色单元", "desc": "依托音乐学院资源，打造涵盖音乐制作、演出的垂直产业链。", "industry": "音乐产业"},
    {"name": "华中金融城片", "category": "显特色单元", "desc": "中北路金融主轴的城市形象塑造与夜经济亮化。", "industry": "科技金融"},
    {"name": "青山古镇片", "category": "显特色单元", "desc": "青山红房子工业遗产保护性开发，重塑钢铁文化记忆。", "industry": "工业遗产"},
    {"name": "东湖健康养生片", "category": "显特色单元", "desc": "依托东湖绿心，发展高端康养、疗养与高端生态旅游。", "industry": "高端康养"},
    {"name": "南湖桥梁文创休闲片", "category": "显特色单元", "desc": "桥梁工程文化与文创产业的跨界融合试验区。", "industry": "文创休闲"},
    {"name": "微电通信创产城片", "category": "显特色单元", "desc": "光电子信息产业核心区，产城深度融合的高能级创新空间。", "industry": "光电信息"},
    {"name": "吹笛生态休闲片", "category": "显特色单元", "desc": "马鞍山森林公园周边生态管控与轻度户外休闲开发。", "industry": "户外休闲"}
]

def generate_mock_polygon(base_lng, base_lat, index, size=0.01):
    """
    基于索引生成矩阵式分布的多边形占位符 (Mock Geometry)
    size 0.01度 约等于 1km
    """
    cols = 6
    offset_x = (index % cols) * (size * 1.5)
    offset_y = (index // cols) * (size * 1.5)
    
    lng = base_lng + offset_x
    lat = base_lat - offset_y
    
    # 构造 WKT 多边形 (逆时针闭合)
    wkt = f"POLYGON(({lng} {lat}, {lng+size} {lat}, {lng+size} {lat-size}, {lng} {lat-size}, {lng} {lat}))"
    return wkt

def main():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # 确保表存在
        cur.execute("""
            CREATE TABLE IF NOT EXISTS wuhan_renewal_units (
                id SERIAL PRIMARY KEY,
                unit_name VARCHAR(255),
                category VARCHAR(100),
                description TEXT,
                main_industry VARCHAR(100),
                investment_est DOUBLE PRECISION,
                geom GEOMETRY(Polygon, 4326)
            );
        """)

        insert_sql = """
            INSERT INTO wuhan_renewal_units 
            (unit_name, category, description, main_industry, investment_est, geom)
            VALUES (%s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
        """
        
        # 武汉中心基准点
        base_lng, base_lat = 114.25, 30.65 
        
        for idx, data in enumerate(RENEWAL_DATA):
            # 模拟生成 10-50 亿的随机投资额度
            invest = round(10 + (idx * 1.5) % 40, 2)
            wkt_geom = generate_mock_polygon(base_lng, base_lat, idx)
            
            cur.execute(insert_sql, (
                data['name'], 
                data['category'], 
                data['desc'], 
                data['industry'],
                invest,
                wkt_geom
            ))
            
        conn.commit()
        print(f"成功将 {len(RENEWAL_DATA)} 条城市更新单元与空间占位符入库！")
        
    except Exception as e:
        print(f"数据库操作失败: {e}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()