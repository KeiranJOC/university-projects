import numpy as np

class Edge:
    def __init__(self, u, v, weight, reversed=False):
        self.u = u
        self.v = v
        self.weight = weight
        self.reversed = reversed

    def reverse(self):
        return Edge(self.v, self.u, self.weight, reversed=True)
    
    def matches_undirected(self, other):
        return (self.u == other.u and self.v == other.v) or (self.u == other.v and self.v == other.u)
    
    def matches(self, other):
        return self.u == other.u and self.v == other.v
    
    def __lt__(self, other):
        return self.weight < other.weight
    
    def __str__(self):
        return f"{self.u} --{self.weight}-> {self.v}"


class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.edges = [[] for v in vertices]
    
    def vertex_count(self):
        return len(self.vertices)
    
    def edge_count(self):
        return sum(map(len, self.edges))
    
    def add_edge_directed_by_index(self, u_index, v_index, weight):
        edge = Edge(u_index, v_index, weight)
        self.edges[edge.u].append(edge)
    
    def add_edge_undirected_by_index(self, u_index, v_index, weight):
        edge = Edge(u_index, v_index, weight)
        self.edges[edge.u].append(edge)
        self.edges[edge.v].append(edge.reverse())
    
    def add_edge_undirected_by_vertex(self, u, v, weight):
        u_index = self.vertices.index(u)
        v_index = self.vertices.index(v)
        edge = Edge(u_index, v_index, weight)
        self.edges[edge.u].append(edge)
        self.edges[edge.v].append(edge.reverse())
    
    def get_edges_by_vertex(self, vertex):
        index = self.vertices.index(vertex)
        return self.edges[index]
    
    def get_edges_by_index(self, index):
        return self.edges[index]
    
    def get_edge_by_indices(self, u_index, v_index):
        return [edge for edge in self.edges[u_index] if edge.v == v_index][0]

    def get_neighbours(self, u_index):
        return [edge.v for edge in self.edges[u_index]]
    
    def get_common_neighbours(self, u_index, v_index):
        u_neighbours = [edge.v for edge in self.edges[u_index]]
        v_neighbours = [edge.v for edge in self.edges[v_index]]
        return np.intersect1d(u_neighbours, v_neighbours)
    
    def get_edges_by_common_neighbour(self, u_index, v_index, r_index):
        edge_u_r = self.get_edge_by_indices(u_index, r_index)
        edge_v_r = self.get_edge_by_indices(v_index, r_index)
        return [edge_u_r, edge_v_r]
    
    def get_vertex_at(self, index):
        return self.vertices[index]
    
    def get_index_of(self, vertex):
        return self.vertices.index(vertex)
    
    def total_weight(self):
        return sum([edge.weight for edges in self.edges for edge in edges if not edge.reversed])
    
    def contains_undirected(self, other_edge):
        for edges in self.edges:
            for edge in edges:
                if edge.matches_undirected(other_edge):
                    return True
        return False
    
    def contains(self, other_edge):
        for edges in self.edges:
            for edge in edges:
                if edge.matches(other_edge):
                    return True
        return False
    
    def print(self):
        print(f"number of vertices: {self.vertex_count()}")
        print(f"number of edges: {self.edge_count()}")
        print(f"total weight: {self.total_weight()}")
        for edges in self.edges:
            for edge in edges:
                print(edge)


def export_gml(graph, file_name, weights=True):
    with open(f"graphs/{file_name}.gml", "w") as f:
        print('Creator "yFiles"', file=f)
        print('Version "2.17"', file=f)
        print('graph', file=f)
        print('[', file=f)
    
        for vertex in graph.vertices:
            print(' node', file=f)
            print(' [', file=f)
            print(f' id {graph.get_index_of(vertex)}', file=f)
            print(f' label "{vertex}"', file=f)
            print(' ]', file=f)
        
        for edges in graph.edges:
            for edge in edges:
                if edge.reversed:
                    continue
                print(' edge', file=f)
                print(' [', file=f)
                print(f' source {edge.u}', file=f)
                print(f' target {edge.v}', file=f)
                if weights:
                        print(f' label {edge.weight}', file=f)
                print(' ]', file=f)
        
        print(']', file=f)


def relative_neighbourhood_graph(graph):
    rng = Graph(graph.vertices)
    visited = [False] * graph.vertex_count()
    
    for u in graph.vertices:
        u_index = graph.get_index_of(u)
        
        for edge in graph.get_edges_by_index(u_index):
            v_index = edge.v
            if visited[edge.v]:
                continue
            common_neighbours = graph.get_common_neighbours(u_index, v_index)
            closer_candidate = False
            
            for r_index in common_neighbours:
                candidate_edges = graph.get_edges_by_common_neighbour(u_index, v_index, r_index)
                if candidate_edges[0] < edge and candidate_edges[1] < edge:
                    closer_candidate = True
                    break
        
            if not closer_candidate:
                rng.add_edge_undirected_by_index(edge.u, edge.v, edge.weight)
        
        visited[edge.u] = True

    return rng