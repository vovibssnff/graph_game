import time
import socket
from heapq import heappush, heappop

Object = "robbers"
HOST = 'localhost'
PORT = 2222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('>>Robbers online!')
    INF = float('inf')

    n = 5
    adj = [[] for _ in range(n)]  # create an empty adjacency list for each vertex

    # add edges to the adjacency list
    adj[0].append((1, 2))  # an edge from vertex 0 to vertex 1 with weight 2
    adj[0].append((2, 4))  # an edge from vertex 0 to vertex 2 with weight 4
    adj[1].append((2, 1))  # an edge from vertex 1 to vertex 2 with weight 1
    adj[1].append((3, 7))  # an edge from vertex 1 to vertex 3 with weight 7
    adj[2].append((3, 3))  # an edge from vertex 2 to vertex 3 with weight 3
    adj[2].append((4, 5))  # an edge from vertex 2 to vertex 4 with weight 5
    adj[3].append((4, 2))  # an edge from vertex 3 to vertex 4 with weight 2


    def dijkstra(adj, s):
        # Initialize the distance and path arrays and visited array
        dist = [INF] * n
        path = [None] * n
        visited = [False] * n

        # Set the distance to the starting vertex to 0 and path to itself
        dist[s] = 0
        path[s] = s

        # Create a priority queue and push the starting vertex onto it
        pq = [(0, s)]  # priority queue of tuples (distance, vertex)

        while pq:
            # Get the vertex with the smallest distance from the priority queue
            d, v = heappop(pq)

            # If the vertex has already been visited, skip it
            if visited[v]:
                continue

            # Mark the vertex as visited
            visited[v] = True

            # Iterate over the edges coming out of the current vertex
            for u, w in adj[v]:
                # If the new distance to the neighboring vertex is shorter than the
                # old one, update the distance and path arrays and push the new distance
                # onto the priority queue
                if dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
                    path[u] = v
                    heappush(pq, (dist[u], u))

        return dist, path


    def move_object(adj, dist, path, start, end):
        current = end
        route = [end]

        # Follow the path in reverse order from end to start
        while current != start:
            current = path[current]
            route.append(current)
        route.reverse()

        # Iterate over the vertices in the route
        for i in range(len(route) - 1):
            # Get the current and next vertices in the route
            curr_vertex = route[i]
            next_vertex = route[i + 1]

            # Get the weight of the edge between the current and next vertices
            edge_weight = None
            for neighbor, weight in adj[curr_vertex]:
                if neighbor == next_vertex:
                    edge_weight = weight
                    break

            # If the edge weight is not found, the path is not valid
            if edge_weight is None:
                print("Error: Invalid path")
                return

            # Move the object along the edge, delaying at each vertex
            print(f"Moving from vertex {curr_vertex} to vertex {next_vertex}")
            for j in range(edge_weight):
                message = Object + str(curr_vertex) + str(next_vertex)
                s.sendall(message.encode('utf-8'))
                print(Object + f"  moving... {j + 1}/{edge_weight}")
                time.sleep(1)
            print(Object + f"   arrived at vertex {next_vertex}, waiting for {next_vertex} seconds")
            for j in range(next_vertex):
                message = Object + str(next_vertex)
                s.sendall(message.encode('utf-8'))
                time.sleep(1)

        # Print a message when the object reaches the final destination
        print(f"\n" + Object + " arrived at the final destination {end}!\n")


    # Find the shortest path from vertex 0 to vertex 4
    dist, path = dijkstra(adj, 0)
    move_object(adj, dist, path, 0, 4)
