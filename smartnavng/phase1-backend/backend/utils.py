import networkx as nx
from models import RoadSegment, Alert
from ai_inference import predict_travel_time, calculate_road_penalty
import math

def haversine_distance(coord1, coord2):
    """Calculate Haversine distance between two coordinates in meters"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def build_road_graph(city: str) -> nx.Graph:
    """Build a graph from road segments in the database"""
    G = nx.Graph()
    road_segments = RoadSegment.query.filter_by(city=city).all()
    alerts = Alert.query.filter_by(is_active=True).all()
    
    for segment in road_segments:
        # Extract start and end points from geometry (simplified)
        # In real implementation, parse actual LINESTRING coordinates
        coords = [(6.5244, 3.3792), (6.5254, 3.3802)]  # Demo coordinates
        
        start_node = coords[0]
        end_node = coords[-1]
        
        # Calculate edge weight: distance + predicted time + penalties
        distance = segment.length_meters
        predicted_time = predict_travel_time(segment)
        penalty = calculate_road_penalty(segment, alerts)
        
        # Combined weight (prioritizing time with penalties)
        weight = predicted_time * penalty
        
        G.add_edge(start_node, end_node, 
                  weight=weight,
                  segment=segment,
                  distance=distance,
                  predicted_time=predicted_time)
    
    return G

def find_optimal_route(graph: nx.Graph, start: tuple, end: tuple) -> list:
    """Find optimal route using A* algorithm"""
    try:
        # Find closest nodes in graph to start/end points
        start_node = min(graph.nodes(), key=lambda node: haversine_distance(start, node))
        end_node = min(graph.nodes(), key=lambda node: haversine_distance(end, node))
        
        # Use A* algorithm with Haversine heuristic
        def heuristic(u, v):
            return haversine_distance(u, v) / 10.0  # Convert to time heuristic
        
        path = nx.astar_path(graph, start_node, end_node, heuristic=heuristic, weight='weight')
        
        # Extract road segments from path
        route_segments = []
        for i in range(len(path) - 1):
            edge_data = graph.get_edge_data(path[i], path[i + 1])
            if edge_data and 'segment' in edge_data:
                route_segments.append(edge_data['segment'])
        
        return route_segments
        
    except (nx.NetworkXNoPath, ValueError):
        return []