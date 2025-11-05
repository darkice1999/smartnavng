from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from models import db, RoadSegment, Alert, User
from utils import build_road_graph, find_optimal_route
from ai_inference import predict_travel_time
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # For demo purposes - in production, use proper password hashing
    user = User.query.filter_by(username=username).first()
    if user and user.password_hash == password:  # In real app, use proper hashing
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/routes/get_route', methods=['POST'])
@jwt_required()
def get_route():
    try:
        data = request.get_json()
        start_lat = float(data['start_lat'])
        start_lng = float(data['start_lng'])
        end_lat = float(data['end_lat'])
        end_lng = float(data['end_lng'])
        city = data.get('city', 'Lagos')
        
        # Build graph and find route
        graph = build_road_graph(city)
        route_segments = find_optimal_route(graph, (start_lat, start_lng), (end_lat, end_lng))
        
        if not route_segments:
            return jsonify({'error': 'No route found'}), 404
        
        # Prepare route GeoJSON
        route_geojson = {
            'type': 'FeatureCollection',
            'features': [segment.to_geojson() for segment in route_segments]
        }
        
        # Calculate total metrics
        total_distance = sum(seg.length_meters for seg in route_segments)
        total_time = sum(predict_travel_time(seg) for seg in route_segments)
        
        return jsonify({
            'route': route_geojson,
            'summary': {
                'total_distance_km': round(total_distance / 1000, 2),
                'estimated_time_min': round(total_time / 60, 2),
                'segment_count': len(route_segments)
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_alerts():
    city = request.args.get('city', 'Lagos')
    active_alerts = Alert.query.filter_by(is_active=True).all()
    
    alerts_geojson = {
        'type': 'FeatureCollection',
        'features': [alert.to_geojson() for alert in active_alerts]
    }
    
    return jsonify(alerts_geojson)

@api_bp.route('/roads', methods=['GET'])
@jwt_required()
def get_roads():
    city = request.args.get('city', 'Lagos')
    roads = RoadSegment.query.filter_by(city=city).all()
    
    roads_geojson = {
        'type': 'FeatureCollection',
        'features': [road.to_geojson() for road in roads]
    }
    
    return jsonify(roads_geojson)