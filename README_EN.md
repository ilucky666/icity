# Urban Renewal & Innovation Emergence (City Innovation Smart Data)

> **WebGIS Platform for Urban Renewal & Innovation Space in Wuhan based on Urban Amenities Theory**  
> *Exploring the relationship between urban renewal and innovation emergence.*

[![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.x-6DB33F?style=flat-square&logo=springboot)](https://spring.io/projects/spring-boot)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9-199900?style=flat-square&logo=leaflet)](https://leafletjs.com/)

## 📖 Background

This project is derived from the empirical study on "The Relationship between Urban Renewal and the Development of Innovation Industries". Focusing on Wuhan City and based on **"Urban Amenities Theory"**, it proposes the core argument:

> **Hypothesis H1: Urban renewal promotes the shaping and upgrading of innovation spaces by improving the level of urban amenities.**

To transform complex econometric models (DID, mediation effects) and spatial analysis results into intuitive, interactive visualization outputs, we developed this WebGIS platform. The platform aims to provide digital references for urban planners and researchers to explore how to stimulate regional innovation vitality by optimizing amenity layout.

## ✨ Key Features

The system includes four core modules, comprehensively demonstrating the coupling mechanism of "Space-Amenity-Innovation":

### 1. 🌏 Macro Spatial Insight
- **Multi-source Layer Overlay**: Supports overlaying kernel density maps of high-tech enterprises in Wuhan and heatmaps of various amenities (cafes, green spaces, cultural facilities).
- **Spatial Coupling Analysis**: Through dynamic transparency adjustment, intuitively observe the geographical overlap characteristics of innovation spaces and amenity agglomeration areas.
- **Real-time Statistics Dashboard**: The sidebar displays key indicators such as the number of enterprises and amenity density within the visible range in real-time.

### 2. ⏳ Emergence Process Evolution
- **Spatio-temporal Evolution Visualization**: Focuses on showing micro-changes in a single renewal unit before and after renewal (e.g., 2014 vs. 2022).
- **Dynamic POI Rendering**: Utilizes Canvas technology to efficiently render thousands of amenity POI points, clearly presenting the surge in amenity quantity and the increase in type richness after renewal.
- **Dual-period Comparison**: By switching time nodes, intuitively verify the path of "Urban Renewal → Amenity Improvement".

### 3. 🏙️ Micro Renewal Archives
- **Full-domain Project Atlas**: Establishes a spatial database of key urban renewal projects in Wuhan (e.g., Pinghe Packaging Plant, Hanyangzao, Tanhualin, etc.).
- **Digital Detail Cards**: Click on a map plot to automatically pop up detailed archives, including basic project information, amenity composition within a 500m buffer zone, and innovation output performance (patent trend) of settled enterprises.

### 4. 🧮 Policy Simulation Sandbox *(In Development)*
- **Interactive Simulation**: Allows users to select planned plots and adjust parameters for proposed amenities (e.g., new parks, cultural facilities) using sliders.
- **Model Prediction**: Based on econometric regression coefficients, the backend calculates the expected increase in innovation enterprises in real-time to assist scientific decision-making.

## 🛠️ Tech Stack

### Frontend
- **Core Framework**: Vue 3 + Vite
- **UI Component Library**: Element Plus
- **Map Engine**: Leaflet (optimized with Canvas renderer)
- **Data Visualization**: ECharts 5
- **HTTP Client**: Axios

### Backend
- **Core Framework**: Java Spring Boot 3
- **ORM Framework**: MyBatis-Plus
- **Database**: PostgreSQL + PostGIS (handling complex spatial geometry and intersection queries)
- **Build Tool**: Maven

### Data Engineering
- **Scripting Language**: Python 3
- **Spatial Processing**: GeoPandas, Shapely, PyOgrio
- **ETL Process**: 
    1. Clean raw SHP/GeoJSON data
    2. Coordinate system standardization (WGS84/GCJ02 conversion)
    3. Spatial Join calculation for DID panel data
    4. Automatic ingestion (to_postgis)

## 🚀 Getting Started

### Prerequisites
- Node.js >= 16
- JDK >= 17
- PostgreSQL >= 13 (PostGIS extension required)
- Python >= 3.9 (Only for data processing scripts)

### 1. Database Setup
Ensure PostgreSQL is installed and create the database `wuhan_gis`.

```sql
CREATE DATABASE wuhan_gis;
\c wuhan_gis
CREATE EXTENSION postgis;
```

Run the initialization script `src/main/resources/setup.sql` provided by the backend to create tables and import basic data.

### 2. Backend Setup
```bash
cd icity-backend
# Check database connection in src/main/resources/application.yml
mvn spring-boot:run
```
The service runs by default at `http://localhost:8080`.

### 3. Frontend Setup
```bash
cd icity-frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to view the system.

### 4. Data Processing (Optional)
If you need to update underlying data, run the Python script:
```bash
# Configure Python environment and install dependencies (geopandas, sqlalchemy, psycopg2)
python db_poi.py
```

## 📂 Project Structure

```
icity/
├── icity-frontend/       # Vue 3 Frontend Project
│   ├── src/
│   │   ├── components/   # Map, Charts, Detail Cards, etc.
│   │   └── assets/       # Static Assets
├── icity-backend/        # Spring Boot Backend Project
│   ├── src/main/java/    # Controller, Service, Mapper, Entity
│   └── src/main/resources/ # Configuration & SQL Scripts
├── db_poi.py             # POI Data Cleaning & Ingestion Script
├── db_polygon.py         # Renewal Unit Polygon Processing Script
└── ...
```

## 👥 Team & Credits

**Urban Renewal & Innovation Emergence Research Group**

This project is supported by the College Student Innovation and Entrepreneurship Training Program. Thanks to all teachers and students who provided data support and guidance for the project.

---
© 2026 City Innovation Smart Data. All Rights Reserved.
