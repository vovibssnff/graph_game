import time
import socket
from collections import deque

Object = "police"
HOST = 'localhost'
PORT = 2222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('>>Cops online!')


    n = 5
    adj = [[] for _ in range(n)]

    # add edges to the adjacency list
    adj[0].append((1, 2))
    adj[0].append((2, 4))
    adj[1].append((2, 1))
    adj[1].append((3, 7))
    adj[2].append((3, 3))
    adj[2].append((4, 5))
    adj[3].append((4, 2))


    def bfs(adj, start):
        # Initialize visited array
        visited = [False] * n

        # Initialize queue and enqueue the start vertex
        queue = deque([start])
        visited[start] = True

        while queue:
            # Dequeue a vertex from the queue
            vertex = queue.popleft()

            # Iterate over adjacent vertices
            for neighbor, weight in adj[vertex]:
                # If neighbor is unvisited, mark it visited and add to the queue
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
                    #data = s.recv(1024)
                    #print('Received from the server:', data.decode('utf-8'))
                    # Move the object along the edge, delaying at each vertex
                    print(f"Moving from vertex {vertex} to vertex {neighbor}")
                    for j in range(weight):
                        print(Object + f"  moving... {j + 1}/{weight}")
                        message = Object + str(vertex) + str(neighbor)
                        s.sendall(message.encode('utf-8'))
                        time.sleep(1)
                    print(Object + f"  arrived at vertex {neighbor}, waiting for {neighbor} seconds")
                    for j in range(neighbor):
                        message = Object + str(neighbor)
                        s.sendall(message.encode('utf-8'))
                        time.sleep(1)
        # Print a message when the object reaches the final destination
        print("\n" + Object + " arrived to the last vertex!")

    # Call BFS starting from vertex 0
    bfs(adj, 2)
