-- Insert sample road segments
INSERT INTO road_segments (segment_id, city, road_name, length_meters, base_speed_kmh, geometry) VALUES
('LAG001', 'Lagos', 'Ahmadu Bello Way', 1500, 40, ST_GeomFromText('LINESTRING(3.3792 6.5244, 3.3802 6.5254)', 4326)),
('LAG002', 'Lagos', 'Adetokunbo Ademola Street', 1200, 35, ST_GeomFromText('LINESTRING(3.3802 6.5254, 3.3812 6.5264)', 4326)),
('LAG003', 'Lagos', 'Kofo Abayomi Road', 1800, 45, ST_GeomFromText('LINESTRING(3.3812 6.5264, 3.3822 6.5274)', 4326)),
('ABJ001', 'Abuja', 'Yakubu Gowon Way', 2000, 50, ST_GeomFromText('LINESTRING(7.4951 9.0579, 7.4961 9.0589)', 4326)),
('PH001', 'Port Harcourt', 'Aba Road', 1600, 35, ST_GeomFromText('LINESTRING(7.0134 4.8156, 7.0144 4.8166)', 4326));

-- Insert sample alerts
INSERT INTO alerts (alert_id, alert_type, severity, description, location, affected_segments, is_active) VALUES
('ALT001', 'construction', 'medium', 'Road construction on Ahmadu Bello Way', ST_GeomFromText('POINT(3.3797 6.5249)', 4326), '["LAG001"]', true),
('ALT002', 'accident', 'high', 'Major accident blocking traffic', ST_GeomFromText('POINT(3.3807 6.5259)', 4326), '["LAG002"]', true);

-- Insert demo user (password: "demo123")
INSERT INTO users (username, email, password_hash) VALUES
('demo', 'demo@smartnavng.com', 'demo123');