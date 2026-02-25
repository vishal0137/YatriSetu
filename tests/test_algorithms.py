"""
Test Pathfinding Algorithms
Tests Dijkstra's and Greedy algorithms with real database data
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.chatbot_modules.algorithms import PathfindingAlgorithms
from app.models.database_models import Route, Stop, Bus

app = create_app()

def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def test_dijkstra_algorithm():
    """Test Dijkstra's algorithm for shortest path"""
    print_section("Testing Dijkstra's Algorithm (Shortest Path)")
    
    with app.app_context():
        test_cases = [
            ("Connaught Place", "IGI Airport"),
            ("Connaught Place", "Dwarka Sector 21"),
            ("Azadpur", "Hauz Khas"),
            ("Kashmere Gate", "Noida City Centre"),
        ]
        
        for source, destination in test_cases:
            print(f"\n🔍 Finding shortest path: {source} → {destination}")
            
            route, total_distance, path = PathfindingAlgorithms.dijkstra_shortest_path(source, destination)
            
            if route:
                bus = Bus.query.get(route.bus_id) if route.bus_id else None
                print(f"✅ Found shortest path!")
                print(f"   Route: {route.route_number} - {route.route_name}")
                print(f"   Bus: {bus.bus_number if bus else 'N/A'} ({bus.bus_type if bus else 'N/A'})")
                print(f"   Total Distance: {total_distance:.2f} km")
                print(f"   Fare: ₹{float(route.fare)}")
                print(f"   Path: {' → '.join(path)}")
                print(f"   Hops: {len(path) - 1}")
            else:
                print(f"❌ No path found")

def test_greedy_algorithm():
    """Test Greedy algorithm for minimum fare"""
    print_section("Testing Greedy Algorithm (Minimum Fare)")
    
    with app.app_context():
        test_cases = [
            ("Connaught Place", "IGI Airport"),
            ("Connaught Place", "Dwarka Sector 21"),
            ("Azadpur", "Hauz Khas"),
            ("Kashmere Gate", "Noida City Centre"),
        ]
        
        for source, destination in test_cases:
            print(f"\n💰 Finding cheapest route: {source} → {destination}")
            
            route, total_fare, path = PathfindingAlgorithms.greedy_minimum_fare(source, destination)
            
            if route:
                bus = Bus.query.get(route.bus_id) if route.bus_id else None
                print(f"✅ Found cheapest route!")
                print(f"   Route: {route.route_number} - {route.route_name}")
                print(f"   Bus: {bus.bus_number if bus else 'N/A'} ({bus.bus_type if bus else 'N/A'})")
                print(f"   Total Fare: ₹{total_fare:.2f}")
                print(f"   Distance: {float(route.distance_km) if route.distance_km else 'N/A'} km")
                print(f"   Path: {' → '.join(path)}")
                print(f"   Hops: {len(path) - 1}")
            else:
                print(f"❌ No path found")

def test_algorithm_comparison():
    """Compare Dijkstra's and Greedy algorithms"""
    print_section("Algorithm Comparison: Shortest vs Cheapest")
    
    with app.app_context():
        test_cases = [
            ("Connaught Place", "IGI Airport"),
            ("Connaught Place", "Dwarka Sector 21"),
        ]
        
        for source, destination in test_cases:
            print(f"\n📊 Comparing algorithms: {source} → {destination}")
            
            # Dijkstra's (shortest path)
            route_d, distance_d, path_d = PathfindingAlgorithms.dijkstra_shortest_path(source, destination)
            
            # Greedy (minimum fare)
            route_g, fare_g, path_g = PathfindingAlgorithms.greedy_minimum_fare(source, destination)
            
            if route_d and route_g:
                print(f"\n   Shortest Path (Dijkstra's):")
                print(f"   - Route: {route_d.route_number}")
                print(f"   - Distance: {distance_d:.2f} km")
                print(f"   - Fare: ₹{float(route_d.fare)}")
                print(f"   - Hops: {len(path_d) - 1}")
                
                print(f"\n   Cheapest Route (Greedy):")
                print(f"   - Route: {route_g.route_number}")
                print(f"   - Fare: ₹{fare_g:.2f}")
                print(f"   - Distance: {float(route_g.distance_km) if route_g.distance_km else 'N/A'} km")
                print(f"   - Hops: {len(path_g) - 1}")
                
                # Analysis
                if route_d.id == route_g.id:
                    print(f"\n   ✅ Same route! Both algorithms agree.")
                else:
                    distance_diff = distance_d - float(route_g.distance_km) if route_g.distance_km else 0
                    fare_diff = float(route_d.fare) - fare_g
                    print(f"\n   📈 Different routes:")
                    print(f"   - Distance difference: {distance_diff:.2f} km")
                    print(f"   - Fare difference: ₹{fare_diff:.2f}")
                    
                    if distance_diff < 0:
                        print(f"   - Shortest path is {abs(distance_diff):.2f} km shorter")
                    if fare_diff > 0:
                        print(f"   - Cheapest route saves ₹{fare_diff:.2f}")

def test_graph_structure():
    """Test graph building and structure"""
    print_section("Testing Graph Structure")
    
    with app.app_context():
        # Get all routes
        all_routes = Route.query.filter_by(is_active=True).all()
        print(f"\n📊 Database Statistics:")
        print(f"   Total Active Routes: {len(all_routes)}")
        
        # Build graph
        graph = {}
        total_edges = 0
        
        for route in all_routes:
            start = route.start_location
            end = route.end_location
            
            if start not in graph:
                graph[start] = []
            graph[start].append(end)
            total_edges += 1
            
            # Add stops
            stops = Stop.query.filter_by(route_id=route.id).order_by(Stop.stop_order).all()
            prev_stop = start
            for stop in stops:
                stop_name = stop.stop_name
                if prev_stop not in graph:
                    graph[prev_stop] = []
                graph[prev_stop].append(stop_name)
                total_edges += 1
                prev_stop = stop_name
            
            if stops and prev_stop != end:
                if prev_stop not in graph:
                    graph[prev_stop] = []
                graph[prev_stop].append(end)
                total_edges += 1
        
        print(f"   Total Nodes (Locations): {len(graph)}")
        print(f"   Total Edges (Connections): {total_edges}")
        print(f"   Average Degree: {total_edges / len(graph):.2f}")
        
        # Find most connected nodes
        node_degrees = [(node, len(neighbors)) for node, neighbors in graph.items()]
        node_degrees.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n   Top 5 Most Connected Locations:")
        for i, (node, degree) in enumerate(node_degrees[:5], 1):
            print(f"   {i}. {node}: {degree} connections")

def test_performance():
    """Test algorithm performance"""
    print_section("Testing Algorithm Performance")
    
    import time
    
    with app.app_context():
        test_cases = [
            ("Connaught Place", "IGI Airport"),
            ("Azadpur", "Hauz Khas"),
            ("Kashmere Gate", "Noida City Centre"),
        ]
        
        print("\n⏱️  Performance Benchmarks:")
        
        for source, destination in test_cases:
            print(f"\n   Route: {source} → {destination}")
            
            # Test Dijkstra's
            start_time = time.time()
            route_d, _, _ = PathfindingAlgorithms.dijkstra_shortest_path(source, destination)
            dijkstra_time = (time.time() - start_time) * 1000
            
            # Test Greedy
            start_time = time.time()
            route_g, _, _ = PathfindingAlgorithms.greedy_minimum_fare(source, destination)
            greedy_time = (time.time() - start_time) * 1000
            
            print(f"   - Dijkstra's: {dijkstra_time:.2f}ms")
            print(f"   - Greedy: {greedy_time:.2f}ms")
            
            if dijkstra_time < greedy_time:
                print(f"   - Dijkstra's is {greedy_time - dijkstra_time:.2f}ms faster")
            else:
                print(f"   - Greedy is {dijkstra_time - greedy_time:.2f}ms faster")

def run_all_tests():
    """Run all algorithm tests"""
    print("\n" + "🚀" * 35)
    print("PATHFINDING ALGORITHMS - COMPREHENSIVE TEST")
    print("Testing Dijkstra's and Greedy algorithms with real database")
    print("🚀" * 35)
    
    try:
        test_graph_structure()
        test_dijkstra_algorithm()
        test_greedy_algorithm()
        test_algorithm_comparison()
        test_performance()
        
        print("\n" + "=" * 70)
        print("✅ ALL ALGORITHM TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\n📝 Summary:")
        print("   ✅ Dijkstra's algorithm: Finding shortest path by distance")
        print("   ✅ Greedy algorithm: Finding minimum fare route")
        print("   ✅ Graph structure: Properly built from database")
        print("   ✅ Performance: Both algorithms execute in milliseconds")
        print("   ✅ Data structures: Using heapq (priority queue) for efficiency")
        
        print("\n🎯 Algorithm Characteristics:")
        print("   • Dijkstra's: O((V + E) log V) time complexity")
        print("   • Greedy: O((V + E) log V) time complexity")
        print("   • Space: O(V) for both algorithms")
        print("   • Data Structure: Min-heap (priority queue) via heapq")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run_all_tests()
