"""
Pathfinding Algorithms Module
Implements Dijkstra's and Greedy algorithms for route optimization
"""

import heapq
from app.models import Route, Stop

class PathfindingAlgorithms:
    """Implements pathfinding algorithms for route optimization"""
    
    @staticmethod
    def dijkstra_shortest_path(source, destination):
        """
        Dijkstra's algorithm to find shortest path by distance
        Returns: (shortest_route, total_distance, path)
        """
        try:
            # Build graph from routes
            graph = {}  # {location: [(neighbor, distance, route_obj), ...]}
            all_routes = Route.query.filter_by(is_active=True).all()
            
            for route in all_routes:
                start = route.start_location
                end = route.end_location
                distance = float(route.distance_km) if route.distance_km else 999999
                
                if start not in graph:
                    graph[start] = []
                graph[start].append((end, distance, route))
                
                # Add stops as intermediate nodes
                stops = Stop.query.filter_by(route_id=route.id).order_by(Stop.stop_order).all()
                prev_stop = start
                for stop in stops:
                    stop_name = stop.stop_name
                    stop_distance = distance / (len(stops) + 1) if stops else distance
                    
                    if prev_stop not in graph:
                        graph[prev_stop] = []
                    graph[prev_stop].append((stop_name, stop_distance, route))
                    prev_stop = stop_name
                
                # Connect last stop to end
                if stops and prev_stop != end:
                    if prev_stop not in graph:
                        graph[prev_stop] = []
                    graph[prev_stop].append((end, distance / (len(stops) + 1), route))
            
            # Dijkstra's algorithm
            distances = {node: float('inf') for node in graph}
            distances[source] = 0
            previous = {node: None for node in graph}
            route_used = {node: None for node in graph}
            pq = [(0, source)]
            visited = set()
            
            while pq:
                current_dist, current = heapq.heappop(pq)
                
                if current in visited:
                    continue
                visited.add(current)
                
                if current == destination:
                    break
                
                if current not in graph:
                    continue
                
                for neighbor, weight, route in graph[current]:
                    distance = current_dist + weight
                    
                    if distance < distances.get(neighbor, float('inf')):
                        distances[neighbor] = distance
                        previous[neighbor] = current
                        route_used[neighbor] = route
                        heapq.heappush(pq, (distance, neighbor))
            
            # Reconstruct path
            if distances.get(destination, float('inf')) == float('inf'):
                return None, None, None
            
            path = []
            current = destination
            while current is not None:
                path.append(current)
                current = previous.get(current)
            path.reverse()
            
            shortest_route = route_used.get(destination)
            
            if len(path) == 2 and shortest_route:
                total_distance = float(shortest_route.distance_km) if shortest_route.distance_km else distances[destination]
            else:
                total_distance = distances[destination]
            
            return shortest_route, total_distance, path
            
        except Exception as e:
            print(f"Dijkstra error: {e}")
            return None, None, None
    
    @staticmethod
    def greedy_minimum_fare(source, destination):
        """
        Greedy algorithm to find minimum fare route
        Returns: (cheapest_route, total_fare, path)
        """
        try:
            # Build graph from routes with fare as weight
            graph = {}  # {location: [(neighbor, fare, route_obj), ...]}
            all_routes = Route.query.filter_by(is_active=True).all()
            
            for route in all_routes:
                start = route.start_location
                end = route.end_location
                fare = float(route.fare)
                
                if start not in graph:
                    graph[start] = []
                graph[start].append((end, fare, route))
                
                # Add stops
                stops = Stop.query.filter_by(route_id=route.id).order_by(Stop.stop_order).all()
                prev_stop = start
                for stop in stops:
                    stop_name = stop.stop_name
                    stop_fare = fare / (len(stops) + 1) if stops else fare
                    
                    if prev_stop not in graph:
                        graph[prev_stop] = []
                    graph[prev_stop].append((stop_name, stop_fare, route))
                    prev_stop = stop_name
                
                if stops and prev_stop != end:
                    if prev_stop not in graph:
                        graph[prev_stop] = []
                    graph[prev_stop].append((end, fare / (len(stops) + 1), route))
            
            # Greedy approach: always choose minimum fare edge
            fares = {node: float('inf') for node in graph}
            fares[source] = 0
            previous = {node: None for node in graph}
            route_used = {node: None for node in graph}
            pq = [(0, source)]
            visited = set()
            
            while pq:
                current_fare, current = heapq.heappop(pq)
                
                if current in visited:
                    continue
                visited.add(current)
                
                if current == destination:
                    break
                
                if current not in graph:
                    continue
                
                # Greedy: sort by fare and pick cheapest
                neighbors = sorted(graph[current], key=lambda x: x[1])
                
                for neighbor, fare, route in neighbors:
                    total_fare = current_fare + fare
                    
                    if total_fare < fares.get(neighbor, float('inf')):
                        fares[neighbor] = total_fare
                        previous[neighbor] = current
                        route_used[neighbor] = route
                        heapq.heappush(pq, (total_fare, neighbor))
            
            # Reconstruct path
            if fares.get(destination, float('inf')) == float('inf'):
                return None, None, None
            
            path = []
            current = destination
            while current is not None:
                path.append(current)
                current = previous.get(current)
            path.reverse()
            
            cheapest_route = route_used.get(destination)
            
            if len(path) == 2 and cheapest_route:
                total_fare = float(cheapest_route.fare)
            else:
                total_fare = fares[destination]
            
            return cheapest_route, total_fare, path
            
        except Exception as e:
            print(f"Greedy error: {e}")
            return None, None, None
