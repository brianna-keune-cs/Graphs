"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of visited_rooms mapping labels to edges."""

    def __init__(self):
        self.visited_rooms = {}

    def add_room(self, room_id):
        """
        Add a vertex to the graph.
        """
        if room_id not in self.visited_rooms.keys():
            self.visited_rooms[room_id] = {}
            return
        raise AssertionError(
            f'room_id: {room_id} is already in graph.')
        
    def len_of_visited(self):
        return len(self.visited_rooms.keys())
    
    def get_visited_rooms(self):
        return self.visited_rooms.keys()

    def add_edge(self, room_id, direction, next_room_id):
        """
        Add a directed edge to the graph.
        """
        if room_id not in self.visited_rooms.keys():
            self.add_room(room_id)
        if direction not in ["n", 's', 'e', 'w']:
            return
        if direction in self.visited_rooms.values():
            raise AssertionError(
                f'vertex: {direction} already has an edge to {room_id}.')
            return
        self.visited_rooms[room_id].__setitem__(direction, next_room_id)

    def get_tracked_exits(self, room_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.visited_rooms[room_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        q.enqueue(starting_vertex)
        visited = set()

        while q.size() > 0:
            current_node = q.dequeue()
            if current_node not in visited:
                visited.add(current_node)
                print(current_node)
                neighbours = self.get_neighbors(current_node)
                for neighbour in neighbours:
                    q.enqueue(neighbour)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        s.push(starting_vertex)
        visited = set()

        while s.size() > 0:
            current_node = s.pop()
            if current_node not in visited:
                visited.add(current_node)
                print(current_node)
                neighbours = self.get_neighbors(current_node)
                for neighbour in neighbours:
                    s.push(neighbour)

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex not in self.visited_rooms:
            raise IndexError(
                f'the starting vertext: {starting_vertex} is not a vertex.')

        if starting_vertex not in visited:
            visited.add(starting_vertex)
            print(starting_vertex)
            neighbours = self.get_neighbors(starting_vertex)
            for neighbour in neighbours:
                self.dft_recursive(neighbour, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_vertex])
        visited = set()

        while q.size() > 0:
            path = q.dequeue()
            current_node = path[-1]
            if current_node is destination_vertex:
                return path
            if current_node not in visited:
                visited.add(current_node)
                for neighbour in self.get_neighbors(current_node):
                    path_copy = path.copy()
                    path_copy.append(neighbour)
                    q.enqueue(path_copy)

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])
        visited = set()

        while s.size() > 0:
            path = s.pop()
            current_node = path[-1]
            if current_node is destination_vertex:
                return path
            if current_node not in visited:
                visited.add(current_node)
                for neighbour in self.get_neighbors(current_node):
                    path_copy = path.copy()
                    path_copy.append(neighbour)
                    s.push(path_copy)

    def dfs_recursive(self, vertex, destination_vertex, visited=set(), path=list()):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if len(path) is 0:
            path.append(vertex)

        visited.add(vertex)

        if vertex is destination_vertex:
            return path

        for neighbour in self.get_neighbors(vertex):
            if neighbour not in visited:
                result = self.dfs_recursive(
                    neighbour, destination_vertex, visited, path + [neighbour])
                if result is not None:
                    return result


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_room(1)
    graph.add_room(2)
    graph.add_room(3)
    graph.add_room(4)
    graph.add_room(5)
    graph.add_room(6)
    graph.add_room(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.visited_rooms)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6), '\n')

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6), '\n')
    print(graph.dfs_recursive(1, 6))
