import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry

# ================= 1. 核心配置区 =================
# 数据库连接 (务必替换为你自己的配置)
DB_URL = 'postgresql://postgres:1@localhost:5432/wuhan_gis'
engine = create_engine(DB_URL)

# 数据源绝对路径
PATH_2014_DIR = r"F:\LIBRARY\Academic\Urbanrenew\icity\2014POI\2014"
FILES_2014 = {
    "餐饮服务": os.path.join(PATH_2014_DIR, "餐饮服务.shp"),
    "风景名胜": os.path.join(PATH_2014_DIR, "风景名胜.shp"),
    "公共设施": os.path.join(PATH_2014_DIR, "公共设施.shp"),
    "科教文化服务": os.path.join(PATH_2014_DIR, "科教文化服务.shp")
}
FILE_2022 = r"F:\LIBRARY\Academic\Urbanrenew\icity\武汉\wgs84\武汉市poi.shp"

# ================= 2. 空间处理管道函数 =================
def process_poi_layer(filepath, year, original_type_val, polygons_gdf, encoding='utf-8'):
    """
    通用空间图层处理管道：读取 -> 清洗 -> 坐标纠正 -> 空间相交裁剪 -> 格式化
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] 文件路径不存在: {filepath}")
        return gpd.GeoDataFrame()

    print(f"[{year}] 正在装载底层文件: {os.path.basename(filepath)} ...")
    
    try:
        # 防御性读取：若 UTF-8 失败则回退至 GB18030 (针对国内老旧SHP的杀手锏)
        gdf = gpd.read_file(filepath, encoding=encoding)
    except UnicodeDecodeError:
        print(f"[{year}] UTF-8 解码失败，正回退至 GB18030 重新读取...")
        gdf = gpd.read_file(filepath, encoding='GB18030')

    # 1. 过滤非法空间体 (NULL 或 EMPTY)
    gdf = gdf.dropna(subset=[gdf.geometry.name])
    gdf = gdf[~gdf.is_empty]

    # 2. 空间参考系统 (CRS) 防御性处理
    if gdf.crs is None:
        print(f"[{year}] 警告：缺失 PRJ 文件，假定原始坐标系为 WGS-84 (EPSG:4326)。")
        gdf.set_crs(epsg=4326, inplace=True)
    elif gdf.crs.to_epsg() != 4326:
        print(f"[{year}] 执行坐标系投影转换: {gdf.crs.to_epsg()} -> EPSG:4326...")
        gdf = gdf.to_crs(epsg=4326)

    # 3. 剥离无用内存字段，仅抽取名称列 (模糊匹配 name, 名称, NAME)
    name_col = next((col for col in gdf.columns if col.lower() in ['name', '名称', 'poiname']), None)
    
    # 动态确定原始分类（如果参数传入的是列名则取列值，若是硬编码字符串则直接赋值）
    if isinstance(original_type_val, str) and original_type_val in gdf.columns:
        raw_type = gdf[original_type_val]
    else:
        raw_type = original_type_val

    clean_df = pd.DataFrame({
        'poi_name': gdf[name_col] if name_col else "未命名要素",
        'original_type': raw_type,
        'unified_category': '舒适物',  # 业务硬性约束：统归一类
        'obs_year': year,
        'geom': gdf.geometry
    })
    clean_gdf = gpd.GeoDataFrame(clean_df, geometry='geom', crs="EPSG:4326")

    # 4. 核心运算：与城市更新多边形执行空间相交 (Spatial Join)
    # 采用 intersects 确保压在边界线上的街铺不被错误剔除
    print(f"[{year}] 执行 R-Tree 空间相交裁剪 (原始数据量: {len(clean_gdf)})...")
    joined_gdf = gpd.sjoin(clean_gdf, polygons_gdf, how='inner', predicate='intersects')
    
    # 5. 字段映射与冗余剔除
    joined_gdf.rename(columns={'id': 'unit_id', 'unit_name': 'unit_name'}, inplace=True)
    cols_to_keep = ['unit_id', 'unit_name', 'poi_name', 'original_type', 'unified_category', 'obs_year', 'geom']
    # 过滤可能存在的多重匹配或无用字段
    final_gdf = joined_gdf[[c for c in cols_to_keep if c in joined_gdf.columns]]
    
    print(f"[{year}] 裁剪完成 -> 实际落入更新区域内的有效 POI 数量: {len(final_gdf)}\n")
    return final_gdf

# ================= 3. 业务执行主控流 =================
def main():
    # 步骤 A: 从数据库抽出现有的城市更新多边形 (掩膜图层)
    print(">>> 正在从 PostGIS 获取城市更新多边形掩膜...")
    sql_poly = "SELECT id, unit_name, geom FROM wuhan_renewal_units;"
    try:
        mask_polygons = gpd.read_postgis(sql_poly, engine, geom_col='geom')
        mask_polygons = mask_polygons.to_crs(epsg=4326)
    except Exception as e:
        print(f"[FATAL] 无法从数据库读取多边形，请检查表结构与数据。错误详情: {e}")
        return

    if mask_polygons.empty:
        print("[FATAL] 城市更新多边形表为空，无执行裁剪的空间基准。程序终止。")
        return

    processed_datasets = []

    # 步骤 B: 批处理 2014 截面数据
    print("========== 开始处理 2014 截面 ==========")
    for label, path in FILES_2014.items():
        # 2014年分文件存储，将文件标签作为原始类别
        res_gdf = process_poi_layer(path, 2014, label, mask_polygons, encoding='GB18030')
        if not res_gdf.empty:
            processed_datasets.append(res_gdf)

    # 步骤 C: 处理 2022 截面数据
    print("========== 开始处理 2022 截面 ==========")
    # 2022年为单文件，假设分类字段名为 'type' 或 '大类'。需根据你实际SHP字段微调
    type_column_guess = 'type' 
    res_2022_gdf = process_poi_layer(FILE_2022, 2022, type_column_guess, mask_polygons, encoding='utf-8')
    if not res_2022_gdf.empty:
        processed_datasets.append(res_2022_gdf)

    # 步骤 D: 全局合并与持久化事务
    print("========== 启动数据库持久化事务 ==========")
    if not processed_datasets:
        print("最终没有任何有效数据落入更新网格，入库中止。")
        return

    master_panel_gdf = pd.concat(processed_datasets, ignore_index=True)
    
    print(f"合并完毕。即将向 PostGIS 写入 {len(master_panel_gdf)} 条清洗后的截面数据。")
    
    try:
        master_panel_gdf.to_postgis(
            name='wuhan_renewal_pois_unified',
            con=engine,
            if_exists='append',
            index=False,
            dtype={'geom': Geometry('POINT', srid=4326)}
        )
        print(">>> [SUCCESS] 空间相交截取并入库成功。双期 DID 面板数据已就绪。")
    except Exception as e:
        print(f">>> [FATAL] 入库过程中发生崩溃。错误链: {e}")

if __name__ == '__main__':
    main()