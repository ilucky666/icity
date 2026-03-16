-- Ensure PostGIS extension is enabled (Commented out to avoid permission issues)
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- Re-create tables to ensure schema is correct
DROP TABLE IF EXISTS sys_renewal_project CASCADE;
DROP TABLE IF EXISTS sys_amenity CASCADE;
DROP TABLE IF EXISTS sys_enterprise CASCADE;

CREATE TABLE sys_renewal_project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    renewal_year INT,
    area DOUBLE PRECISION,
    geom GEOMETRY(Polygon, 4326)
);

CREATE TABLE sys_amenity (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    geom GEOMETRY(Point, 4326)
);

CREATE TABLE sys_enterprise (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    start_year INT,
    patent_count INT,
    geom GEOMETRY(Point, 4326)
);

-- 1. Wuhan Tiandi Xintiandi
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('武汉天地新天地', 2010, 60000, ST_Buffer(ST_GeomFromText('POINT(114.3060 30.6062)', 4326)::geography, 150)::geometry);

-- 2. Wuhan Trend Box X118
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('武汉潮流盒子X118', 2023, 33000, ST_Buffer(ST_GeomFromText('POINT(114.2863 30.5828)', 4326)::geography, 80)::geometry);

-- 3. Wuhan Xian''an Fang
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('武汉咸安坊', 2022, 20000, ST_Buffer(ST_GeomFromText('POINT(114.2951 30.5843)', 4326)::geography, 100)::geometry);

-- 4. Wuhan People''s Paradise
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('武汉民众乐园', 2023, 15000, ST_Buffer(ST_GeomFromText('POINT(114.2882 30.5815)', 4326)::geography, 90)::geometry);

-- 5. Tanhualin Historical and Cultural Block
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('昙华林历史文化街区', 2019, 40000, ST_Buffer(ST_GeomFromText('POINT(114.3105 30.5534)', 4326)::geography, 200)::geometry);

-- 6. Hanyangzao Cultural and Creative Industry Park
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('汉阳造文化创意产业园', 2013, 50000, ST_Buffer(ST_GeomFromText('POINT(114.2642 30.5568)', 4326)::geography, 250)::geometry);

-- 7. Wuhan Duoniu World / Pinghe Packaging Plant
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('武汉多牛世界 (平和打包厂)', 2019, 30000, ST_Buffer(ST_GeomFromText('POINT(114.2965 30.5872)', 4326)::geography, 120)::geometry);

-- 8. Deshengqiao Area
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('得胜桥片', 2024, 25000, ST_Buffer(ST_GeomFromText('POINT(114.3045 30.5565)', 4326)::geography, 150)::geometry);

-- 9. Sandeli Area
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('三德里片区', 2023, 18000, ST_Buffer(ST_GeomFromText('POINT(114.2982 30.5913)', 4326)::geography, 100)::geometry);

-- 10. Yangyuan Simeitang Railway Relics
INSERT INTO sys_renewal_project (name, renewal_year, area, geom)
VALUES ('杨园四美塘铁路遗址', 2023, 45000, ST_Buffer(ST_GeomFromText('POINT(114.3540 30.6125)', 4326)::geography, 200)::geometry);


-- Insert manual amenities (Sample)
INSERT INTO sys_amenity (name, type, geom) VALUES
('Starbucks Reserve', 'Cafe', ST_GeomFromText('POINT(114.3065 30.6065)', 4326)),
('Xintiandi Park', 'Park', ST_GeomFromText('POINT(114.3055 30.6060)', 4326)),
('X118 Cafe', 'Cafe', ST_GeomFromText('POINT(114.2865 30.5830)', 4326)),
('Xianan Museum', 'Museum', ST_GeomFromText('POINT(114.2955 30.5845)', 4326)),
('Paradise Theater', 'Culture', ST_GeomFromText('POINT(114.2885 30.5818)', 4326)),
('Tanhualin Gallery', 'Gallery', ST_GeomFromText('POINT(114.3110 30.5536)', 4326)),
('Hanyangzao Art Center', 'Gallery', ST_GeomFromText('POINT(114.2645 30.5570)', 4326)),
('Pinghe Library', 'Culture', ST_GeomFromText('POINT(114.2968 30.5875)', 4326)),
('Deshengqiao Teahouse', 'Restaurant', ST_GeomFromText('POINT(114.3048 30.5568)', 4326)),
('Sandeli Heritage', 'Museum', ST_GeomFromText('POINT(114.2985 30.5915)', 4326)),
('Railway Park', 'Park', ST_GeomFromText('POINT(114.3545 30.6130)', 4326));

-- Insert manual enterprises (Sample)
INSERT INTO sys_enterprise (name, start_year, patent_count, geom) VALUES
('Tiandi Tech', 2018, 12, ST_GeomFromText('POINT(114.3062 30.6063)', 4326)),
('X118 Design', 2023, 5, ST_GeomFromText('POINT(114.2864 30.5829)', 4326)),
('Xianan Media', 2022, 8, ST_GeomFromText('POINT(114.2952 30.5844)', 4326)),
('Paradise Interactive', 2023, 3, ST_GeomFromText('POINT(114.2883 30.5816)', 4326)),
('Tanhualin Creative', 2020, 15, ST_GeomFromText('POINT(114.3108 30.5535)', 4326)),
('Hanyangzao Studio', 2015, 25, ST_GeomFromText('POINT(114.2643 30.5569)', 4326)),
('Pinghe Innovation', 2019, 10, ST_GeomFromText('POINT(114.2966 30.5873)', 4326)),
('Deshengqiao Arch', 2024, 2, ST_GeomFromText('POINT(114.3046 30.5566)', 4326)),
('Sandeli Culture', 2023, 4, ST_GeomFromText('POINT(114.2983 30.5914)', 4326)),
('Simeitang Engineering', 2023, 7, ST_GeomFromText('POINT(114.3542 30.6128)', 4326));
