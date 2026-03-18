<img width="2559" height="1228" alt="屏幕截图 2026-03-17 051351" src="https://github.com/user-attachments/assets/549cadf9-2da5-4221-90c4-6af3256daad5" /># 城新智数 (City Innovation Smart Data)

> **基于舒适物理论的武汉市城市更新与创新空间 WebGIS 平台**  
> *WebGIS Platform for Urban Renewal & Innovation Space in Wuhan based on Urban Amenities Theory*

[![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-6DB33F?style=flat-square&logo=springboot)](https://spring.io/projects/spring-boot)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900?style=flat-square&logo=leaflet)](https://leafletjs.com/)

<img width="1000" height="492" alt="屏幕截图 2026-03-17 051128" src="https://github.com/user-attachments/assets/77753b08-f41a-449a-9a6e-5a258a92b66f" />
<img width="1000" height="492" alt="屏幕截图 2026-03-17 051308" src="https://github.com/user-attachments/assets/e612b983-f314-4850-a0b0-1b9c549b9cd6" />
<img width="1000" height="492" alt="屏幕截图 2026-03-17 051202" src="https://github.com/user-attachments/assets/d2373424-351b-4ce8-bb74-f6ddcc2471c9" />
<img width="1000" height="492" alt="屏幕截图 2026-03-17 051337" src="https://github.com/user-attachments/assets/231a205d-67b8-448e-94d8-b7d1de2a4e3b" />
<img width="1000" height="492" alt="屏幕截图 2026-03-17 051351" src="https://github.com/user-attachments/assets/d853da50-494f-4538-add1-e2a56d2e7bfd" />



## 📖 项目背景 (Background)

本项目脱胎于《城市更新与创新产业发展之间的关系》实证研究。研究聚焦武汉市，基于**“城市舒适物理论”** (Urban Amenities Theory)，提出了核心论点：

> **假说 H1：城市更新通过提升舒适物水平，进而促进创新空间的塑造与升级。**
> *(Urban renewal promotes the shaping of innovation spaces by improving the level of urban amenities.)*

为了将复杂的计量经济学模型（DID、中介效应）与空间分析结果转化为直观、可交互的可视化成果，我们开发了本 WebGIS 平台。平台旨在为城市规划者和研究人员提供数字化的参考，探索如何通过优化舒适物布局来激发区域创新活力。

## ✨ 核心功能 (Features)

本系统包含四大核心模块，全方位展示“空间-舒适物-创新”的耦合机制：

### 1. 🌏 宏观时空洞察 (Macro Spatial Insight)
- **多源图层叠加**：支持叠加武汉市高新技术企业核密度图、各类舒适物（咖啡馆、绿地、文化设施）热力图。
- **空间耦合分析**：通过动态透明度调节，直观观察创新空间与舒适物集聚区的地理重合特征。
- **实时统计看板**：侧边栏实时展示可视范围内的企业数量、舒适物密度等关键指标。

### 2. ⏳ 涌现过程演变 (Emergence Process Evolution)
- **时空演变可视化**：专注于展示单一更新单元在更新前后（如 2014 vs 2022）的微观变化。
- **动态 POI 渲染**：利用 Canvas 技术高效渲染成千上万个舒适物 POI 点，清晰呈现更新后舒适物数量的激增与类型丰富度的提升。
- **双期对比**：通过切换时间节点，直观验证“城市更新 → 舒适物提升”的路径。

### 3. 🏙️ 微观更新区档案 (Micro Renewal Archives)
- **全域项目图谱**：建立武汉市重点城市更新项目（如平和打包厂、汉阳造、昙华林等）的空间数据库。
- **数字详情卡片**：点击地图地块，自动弹出详细档案，包含项目基础信息、周边 500m 缓冲带舒适物构成、以及入驻企业的创新产出绩效（专利数趋势）。

### 4. 🧮 政策推演沙盘 (Policy Simulation) *(开发中)*
- **交互式模拟**：允许用户圈选规划地块，通过滑块调节拟新增的舒适物参数（如新增公园、文化设施）。
- **模型预测**：后端基于计量回归系数，实时测算该规划方案预期带来的创新企业增量，辅助科学决策。

## 🛠️ 技术架构 (Tech Stack)

### 前端 (Frontend)
- **核心框架**: Vue 3 + Vite
- **UI 组件库**: Element Plus
- **地图引擎**: Leaflet (配合 Canvas 渲染器优化性能)
- **数据可视化**: ECharts 5
- **HTTP 客户端**: Axios

### 后端 (Backend)
- **核心框架**: Java Spring Boot 3
- **ORM 框架**: MyBatis-Plus
- **数据库**: PostgreSQL + PostGIS (处理复杂空间几何与相交查询)
- **构建工具**: Maven

### 数据工程 (Data Engineering)
- **脚本语言**: Python 3
- **空间处理**: GeoPandas, Shapely, PyOgrio
- **ETL 流程**: 
    1. 清洗原始 SHP/GeoJSON 数据
    2. 坐标系标准化 (WGS84/GCJ02 转换)
    3. 空间连接 (Spatial Join) 计算 DID 面板数据
    4. 自动入库 (to_postgis)

## 🚀 快速开始 (Getting Started)

### 前置要求 (Prerequisites)
- Node.js >= 16
- JDK >= 17
- PostgreSQL >= 13 (需开启 PostGIS 扩展)
- Python >= 3.9 (仅用于数据处理脚本)

### 1. 数据库配置 (Database Setup)
确保 PostgreSQL 已安装并创建数据库 `wuhan_gis`。

```sql
CREATE DATABASE wuhan_gis;
\c wuhan_gis
CREATE EXTENSION postgis;
```

运行后端提供的初始化脚本 `src/main/resources/setup.sql` 建表并导入基础数据。

### 2. 后端启动 (Backend Setup)
```bash
cd icity-backend
# 检查配置文件 src/main/resources/application.yml 中的数据库连接
mvn spring-boot:run
```
服务默认运行在 `http://localhost:8080`。

### 3. 前端启动 (Frontend Setup)
```bash
cd icity-frontend
npm install
npm run dev
```
访问 `http://localhost:5173` 查看系统。

### 4. 数据处理 (Data Processing - Optional)
如果需要更新底层数据，可运行 Python 脚本：
```bash
# 配置 Python 环境并安装依赖 (geopandas, sqlalchemy, psycopg2)
python db_poi.py
```

## 📂 项目结构 (Project Structure)

```
icity/
├── icity-frontend/       # Vue 3 前端项目
│   ├── src/
│   │   ├── components/   # 地图、图表、详情卡片等组件
│   │   └── assets/       # 静态资源
├── icity-backend/        # Spring Boot 后端项目
│   ├── src/main/java/    # Controller, Service, Mapper, Entity
│   └── src/main/resources/ # 配置文件与 SQL 脚本
├── db_poi.py             # POI 数据清洗与入库脚本
├── db_polygon.py         # 更新单元多边形处理脚本
└── ...
```

## 👥 团队与致谢 (Team & Credits)

**城市更新与创新涌现研究课题组**  
*Urban Renewal & Innovation Emergence Research Group*

本项目受大学生创新创业训练计划支持。感谢所有为项目提供数据支持与指导的老师和同学。

---
© 2026 城新智数. All Rights Reserved.
