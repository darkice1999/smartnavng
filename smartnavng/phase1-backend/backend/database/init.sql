-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Create tables
CREATE TABLE IF NOT EXISTS road_segments (
    id SERIAL PRIMARY KEY,
    segment_id VARCHAR(50) UNIQUE NOT NULL,
    city VARCHAR(50) NOT NULL,
    road_name VARCHAR(200),
    length_meters FLOAT NOT NULL,
    base_speed_kmh FLOAT DEFAULT 30.0,
    geometry GEOMETRY(LINESTRING, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    alert_id VARCHAR(50) UNIQUE NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    description VARCHAR(500),
    location GEOMETRY(POINT, 4326),
    affected_segments JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_road_segments_geometry ON road_segments USING GIST(geometry);
CREATE INDEX IF NOT EXISTS idx_road_segments_city ON road_segments(city);
CREATE INDEX IF NOT EXISTS idx_alerts_location ON alerts USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(is_active);