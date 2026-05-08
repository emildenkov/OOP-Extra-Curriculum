import numpy as np
from collections import deque


class Graph:

    def __init__(self, mat, node_labels=None, mat_type=True, graph_type=None):
        """
        Args:
            mat: 2D list or numpy array representing the matrix
            node_labels: list of node names (e.g. ['A','B','C']). If None, uses 0,1,2...
            mat_type: True = adjacency matrix, False = incidence matrix
            graph_type: True = weighted, False = unweighted, None = unknown/tree
        """
        self.mat = np.array(mat)
        self.mat_type = mat_type
        self.graph_type = graph_type

        if node_labels is not None:
            self.node_labels = list(node_labels)
        else:
            n = self.mat.shape[0]
            self.node_labels = list(range(n))

        self._label_to_idx = {label: i for i, label in enumerate(self.node_labels)}

    # ==================================================================
    # Properties
    # ==================================================================

    @property
    def num_nodes(self):
        return self.mat.shape[0]

    @property
    def num_edges(self):
        if self.mat_type:
            return int(np.count_nonzero(self.mat))
        else:
            return self.mat.shape[1]

    @property
    def is_directed(self):
        """A graph is undirected if its adjacency matrix is symmetric."""
        if not self.mat_type:
            return True
        return not np.array_equal(self.mat, self.mat.T)

    # ==================================================================
    # Pretty print
    # ==================================================================

    def pretty_print(self, title=""):
        if title:
            print(f"\n{'=' * 60}")
            print(f"  {title}")
            print(f"{'=' * 60}")

        mat_label = "Adjacency" if self.mat_type else "Incidence"
        weight_label = {True: "weighted", False: "unweighted", None: "unknown/tree"}[self.graph_type]
        directed_label = "directed" if self.is_directed else "undirected"

        print(f"  Type: {mat_label} matrix | {weight_label} | {directed_label}")
        print(f"  Nodes: {self.num_nodes} | Edges: {self.num_edges}")
        print()

        if self.mat_type:
            max_label_len = max(len(str(l)) for l in self.node_labels)
            cell_width = max(max_label_len + 1, 4)

            header = " " * (max_label_len + 2) + "".join(
                f"{str(l):>{cell_width}}" for l in self.node_labels
            )
            print(header)
            print(" " * (max_label_len + 2) + "-" * (cell_width * self.num_nodes))

            for i, label in enumerate(self.node_labels):
                row_str = f"{str(label):>{max_label_len}} |"
                for j in range(self.num_nodes):
                    val = self.mat[i][j]
                    val_str = str(int(val)) if val == int(val) else f"{val:.0f}"
                    row_str += f"{val_str:>{cell_width}}"
                print(row_str)
        else:
            edge_labels = [f"e{i}" for i in range(self.mat.shape[1])]
            max_label_len = max(len(str(l)) for l in self.node_labels)
            cell_width = max(4, max_label_len + 1)

            header = " " * (max_label_len + 2) + "".join(
                f"{el:>{cell_width}}" for el in edge_labels
            )
            print(header)
            print(" " * (max_label_len + 2) + "-" * (cell_width * len(edge_labels)))

            for i, label in enumerate(self.node_labels):
                row_str = f"{str(label):>{max_label_len}} |"
                for j in range(self.mat.shape[1]):
                    val = int(self.mat[i][j])
                    row_str += f"{val:>{cell_width}}"
                print(row_str)

        print()

    # ==================================================================
    # Conversion: adjacency <-> incidence
    # ==================================================================

    def to_incidence(self):
        """Converts adjacency matrix to incidence matrix.
        For directed graphs: source = -1, target = 1.
        For undirected graphs: both endpoints = 1.
        Returns a new Graph with mat_type=False."""
        if not self.mat_type:
            print("Already an incidence matrix.")
            return self

        edges = []
        n = self.num_nodes
        directed = self.is_directed

        for i in range(n):
            start_j = 0 if directed else i
            for j in range(start_j, n):
                if self.mat[i][j] != 0:
                    col = np.zeros(n, dtype=int)
                    if directed:
                        col[i] = -1
                        col[j] = 1
                    else:
                        col[i] = 1
                        col[j] = 1
                    edges.append(col)

        if not edges:
            inc_mat = np.zeros((n, 0), dtype=int)
        else:
            inc_mat = np.column_stack(edges)

        new_graph = Graph(inc_mat, self.node_labels, mat_type=False, graph_type=self.graph_type)
        return new_graph

    def to_adjacency(self):
        """Converts incidence matrix back to adjacency matrix.
        Returns a new Graph with mat_type=True."""
        if self.mat_type:
            print("Already an adjacency matrix.")
            return self

        n = self.mat.shape[0]
        num_edges = self.mat.shape[1]
        adj = np.zeros((n, n), dtype=int)

        for e in range(num_edges):
            col = self.mat[:, e]

            sources = np.where(col == -1)[0]
            targets = np.where(col == 1)[0]

            if len(sources) > 0 and len(targets) > 0:
                for s in sources:
                    for t in targets:
                        adj[s][t] = 1
            elif len(targets) >= 2:
                nodes_in_edge = list(targets)
                for a in range(len(nodes_in_edge)):
                    for b in range(a + 1, len(nodes_in_edge)):
                        adj[nodes_in_edge[a]][nodes_in_edge[b]] = 1
                        adj[nodes_in_edge[b]][nodes_in_edge[a]] = 1

        new_graph = Graph(adj, self.node_labels, mat_type=True, graph_type=self.graph_type)
        return new_graph

    def convert(self):
        """Converts the matrix based on current mat_type.
        If adjacency -> returns incidence. If incidence -> returns adjacency."""
        if self.mat_type:
            return self.to_incidence()
        else:
            return self.to_adjacency()

    # ==================================================================
    # Standard graph algorithms
    # ==================================================================

    def _get_adj(self):
        """Returns adjacency matrix (converts if needed)."""
        if self.mat_type:
            return self.mat
        else:
            return self.to_adjacency().mat

    def neighbors(self, node):
        """Returns list of neighbor labels for a given node."""
        adj = self._get_adj()
        idx = self._label_to_idx[node]
        result = []
        for j in range(self.num_nodes):
            if adj[idx][j] != 0:
                result.append(self.node_labels[j])
        return result

    def bfs(self, start):
        """Breadth-First Search from a starting node. Returns visit order."""
        adj = self._get_adj()
        start_idx = self._label_to_idx[start]
        visited = set()
        order = []
        queue = deque([start_idx])
        visited.add(start_idx)

        while queue:
            current = queue.popleft()
            order.append(self.node_labels[current])

            for j in range(self.num_nodes):
                if adj[current][j] != 0 and j not in visited:
                    visited.add(j)
                    queue.append(j)

        return order

    def dfs(self, start):
        """Depth-First Search from a starting node. Returns visit order."""
        adj = self._get_adj()
        start_idx = self._label_to_idx[start]
        visited = set()
        order = []

        def _dfs(node):
            visited.add(node)
            order.append(self.node_labels[node])
            for j in range(self.num_nodes):
                if adj[node][j] != 0 and j not in visited:
                    _dfs(j)

        _dfs(start_idx)
        return order

    def has_cycle(self):
        """Detects if the directed graph has a cycle using DFS coloring.
        WHITE=0 (unvisited), GRAY=1 (in progress), BLACK=2 (done)."""
        adj = self._get_adj()
        n = self.num_nodes
        color = [0] * n

        def _dfs(node):
            color[node] = 1
            for j in range(n):
                if adj[node][j] != 0:
                    if color[j] == 1:
                        return True
                    if color[j] == 0 and _dfs(j):
                        return True
            color[node] = 2
            return False

        for i in range(n):
            if color[i] == 0:
                if _dfs(i):
                    return True
        return False

    def shortest_path(self, start, end):
        """BFS-based shortest path (unweighted) or Dijkstra (weighted).
        Returns (distance, path_as_labels)."""
        adj = self._get_adj()
        start_idx = self._label_to_idx[start]
        end_idx = self._label_to_idx[end]

        if self.graph_type:
            return self._dijkstra(start_idx, end_idx, adj)
        else:
            return self._bfs_shortest(start_idx, end_idx, adj)

    def _bfs_shortest(self, start, end, adj):
        """BFS shortest path for unweighted graphs."""
        n = self.num_nodes
        dist = [-1] * n
        parent = [-1] * n
        dist[start] = 0
        queue = deque([start])

        while queue:
            u = queue.popleft()
            if u == end:
                break
            for v in range(n):
                if adj[u][v] != 0 and dist[v] == -1:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)

        if dist[end] == -1:
            return float('inf'), []

        path = []
        current = end
        while current != -1:
            path.append(self.node_labels[current])
            current = parent[current]
        path.reverse()

        return dist[end], path

    def _dijkstra(self, start, end, adj):
        """Dijkstra's algorithm for weighted graphs."""
        import heapq
        n = self.num_nodes
        dist = [float('inf')] * n
        parent = [-1] * n
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                break
            for v in range(n):
                if adj[u][v] != 0:
                    new_dist = dist[u] + adj[u][v]
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        parent[v] = u
                        heapq.heappush(pq, (new_dist, v))

        if dist[end] == float('inf'):
            return float('inf'), []

        path = []
        current = end
        while current != -1:
            path.append(self.node_labels[current])
            current = parent[current]
        path.reverse()

        return dist[end], path

    def in_degree(self):
        """Returns dict of in-degree for each node."""
        adj = self._get_adj()
        return {self.node_labels[j]: int(np.sum(adj[:, j] != 0))
                for j in range(self.num_nodes)}

    def out_degree(self):
        """Returns dict of out-degree for each node."""
        adj = self._get_adj()
        return {self.node_labels[i]: int(np.sum(adj[i, :] != 0))
                for i in range(self.num_nodes)}

    def find_roots(self):
        """Finds nodes with in-degree 0 (potential roots for trees)."""
        in_deg = self.in_degree()
        return [node for node, deg in in_deg.items() if deg == 0]

    def find_leaves(self):
        """Finds nodes with out-degree 0 (leaves in a tree)."""
        out_deg = self.out_degree()
        return [node for node, deg in out_deg.items() if deg == 0]

    def is_tree(self):
        """Checks if the graph is a tree:
        - Connected, N-1 edges, no cycles."""
        n = self.num_nodes
        e = self.num_edges
        if e != n - 1:
            return False
        return not self.has_cycle()

    def topological_sort(self):
        """Topological sort using Kahn's algorithm. Returns sorted labels or None if cycle."""
        adj = self._get_adj()
        n = self.num_nodes
        in_deg = [0] * n
        for j in range(n):
            for i in range(n):
                if adj[i][j] != 0:
                    in_deg[j] += 1

        queue = deque([i for i in range(n) if in_deg[i] == 0])
        result = []

        while queue:
            u = queue.popleft()
            result.append(self.node_labels[u])
            for v in range(n):
                if adj[u][v] != 0:
                    in_deg[v] -= 1
                    if in_deg[v] == 0:
                        queue.append(v)

        if len(result) != n:
            return None
        return result

    def connected_components(self):
        """Finds connected components (treats graph as undirected)."""
        adj = self._get_adj()
        n = self.num_nodes
        visited = set()
        components = []

        def _bfs(start):
            comp = []
            q = deque([start])
            visited.add(start)
            while q:
                u = q.popleft()
                comp.append(self.node_labels[u])
                for v in range(n):
                    if (adj[u][v] != 0 or adj[v][u] != 0) and v not in visited:
                        visited.add(v)
                        q.append(v)
            return comp

        for i in range(n):
            if i not in visited:
                components.append(_bfs(i))

        return components

    # ==================================================================
    # Summary
    # ==================================================================

    def summary(self):
        """Prints a full analysis of the graph."""
        self.pretty_print()

        roots = self.find_roots()
        leaves = self.find_leaves()
        tree = self.is_tree()
        cycle = self.has_cycle()
        components = self.connected_components()

        print(f"  Roots (in-degree 0): {roots}")
        print(f"  Leaves (out-degree 0): {leaves}")
        print(f"  Is tree: {tree}")
        print(f"  Has cycle: {cycle}")
        print(f"  Connected components: {len(components)}")
        for i, comp in enumerate(components):
            print(f"    Component {i}: {comp}")

        if roots and not cycle:
            start = roots[0]
            print(f"\n  BFS from {start}: {self.bfs(start)}")
            print(f"  DFS from {start}: {self.dfs(start)}")

        topo = self.topological_sort()
        if topo:
            print(f"  Topological sort: {topo}")

        print(f"\n  In-degree: {self.in_degree()}")
        print(f"  Out-degree: {self.out_degree()}")


# ======================================================================
# Graph definitions from archive images
# ======================================================================

def build_all_graphs():
    """Builds all graphs from the images and returns them as a dict."""
    graphs = {}

    # ------------------------------------------------------------------
    # 1.JPG — Directed tree (A-K)
    # A→B, A→C, B→D, C→E, C→F, E→J, E→K, F→G, K→H, K→I
    # ------------------------------------------------------------------
    labels_1 = list("ABCDEFGHIJK")
    n = len(labels_1)
    idx = {l: i for i, l in enumerate(labels_1)}
    m = np.zeros((n, n), dtype=int)
    for src, dst in [("A","B"),("A","C"),("B","D"),("C","E"),("C","F"),
                     ("E","J"),("E","K"),("F","G"),("K","H"),("K","I")]:
        m[idx[src]][idx[dst]] = 1
    graphs["1.JPG — Tree (11 nodes)"] = Graph(m, labels_1, graph_type=None)

    # ------------------------------------------------------------------
    # 6.JPG — Directed graph (A-F)
    # A→D, D→B, D→E, B→C, E→C, E→F, F→C
    # ------------------------------------------------------------------
    labels_6 = list("ABCDEF")
    n = len(labels_6)
    idx = {l: i for i, l in enumerate(labels_6)}
    m = np.zeros((n, n), dtype=int)
    for src, dst in [("A","D"),("D","B"),("D","E"),("B","C"),("E","C"),("E","F"),("F","C")]:
        m[idx[src]][idx[dst]] = 1
    graphs["6.JPG — Directed graph (6 nodes)"] = Graph(m, labels_6, graph_type=False)

    # ------------------------------------------------------------------
    # 7.JPG — Expression tree: ln(20%(10-7)) - (e + sin(0))
    # Nodes: A(-), B(ln), C(+), D(%), E(e), F(sin), G(20), H(-), I(0), J(10), K(7)
    # ------------------------------------------------------------------
    labels_7 = ["A:-", "B:ln", "C:+", "D:%", "E:e", "F:sin", "G:20", "H:-", "I:0", "J:10", "K:7"]
    n = len(labels_7)
    m = np.zeros((n, n), dtype=int)
    # A→B, A→C, B→D, C→E, C→F, D→G, D→H, F→I, H→J, H→K
    edges_7 = [(0,1),(0,2),(1,3),(2,4),(2,5),(3,6),(3,7),(5,8),(7,9),(7,10)]
    for i, j in edges_7:
        m[i][j] = 1
    graphs["7.JPG — Expression tree"] = Graph(m, labels_7, graph_type=None)

    # ------------------------------------------------------------------
    # 8.JPG — Directed tree (A-K, different from 1.JPG)
    # A→B, A→C, B→D, C→E, C→F, F→J, F→K, F→G, G→H, G→I
    # ------------------------------------------------------------------
    labels_8 = list("ABCDEFGHIJK")
    n = len(labels_8)
    idx = {l: i for i, l in enumerate(labels_8)}
    m = np.zeros((n, n), dtype=int)
    for src, dst in [("A","B"),("A","C"),("B","D"),("C","E"),("C","F"),
                     ("F","J"),("F","K"),("F","G"),("G","H"),("G","I")]:
        m[idx[src]][idx[dst]] = 1
    graphs["8.JPG — Tree (11 nodes, variant)"] = Graph(m, labels_8, graph_type=None)

    # ------------------------------------------------------------------
    # 9.JPG — Directed graph (0-12 in circle)
    # Edges read from image: 2→0, 2→4, 2→6, 2→12, 12→10, 12→8, 10→8, 8→6
    # ------------------------------------------------------------------
    labels_9 = list(range(13))
    n = 13
    m = np.zeros((n, n), dtype=int)
    for src, dst in [(2,0),(2,4),(2,6),(2,12),(12,10),(12,8),(10,8),(8,6)]:
        m[src][dst] = 1
    graphs["9.JPG — Directed graph (13 nodes)"] = Graph(m, labels_9, graph_type=False)

    # ------------------------------------------------------------------
    # 10.JPG / 11.JPG — Tree (A-I)
    # A→B, A→C, B→D, C→E, C→F, D→G, G→H, G→I
    # ------------------------------------------------------------------
    labels_10 = list("ABCDEFGHI")
    n = len(labels_10)
    idx = {l: i for i, l in enumerate(labels_10)}
    m = np.zeros((n, n), dtype=int)
    for src, dst in [("A","B"),("A","C"),("B","D"),("C","E"),("C","F"),
                     ("D","G"),("G","H"),("G","I")]:
        m[idx[src]][idx[dst]] = 1
    graphs["10.JPG — Tree (9 nodes)"] = Graph(m, labels_10, graph_type=None)

    # ------------------------------------------------------------------
    # 3.JPG — Directed graph (0-12, different edges)
    # Edges: 0→3, 0→4, 0→5, 0→6, 0→8, 0→9, 2→3, 2→4, 3→4, 3→5, 11→0
    # ------------------------------------------------------------------
    labels_3 = list(range(13))
    n = 13
    m = np.zeros((n, n), dtype=int)
    for src, dst in [(0,3),(0,4),(0,5),(0,6),(0,8),(0,9),(2,3),(2,4),(3,4),(3,5),(11,0)]:
        m[src][dst] = 1
    graphs["3.JPG — Directed graph (13 nodes, variant)"] = Graph(m, labels_3, graph_type=False)

    # ------------------------------------------------------------------
    # 4.JPG — Weighted directed graph (A-P)
    # Edges with weights read from image
    # ------------------------------------------------------------------
    labels_4 = list("ABCDEFGHIJKLMOP")
    n = len(labels_4)
    idx = {l: i for i, l in enumerate(labels_4)}
    m = np.zeros((n, n), dtype=int)
    weighted_edges = [
        ("A","B",80), ("E","A",60), ("B","C",100), ("C","D",175),
        ("B","E",100), ("F","E",100), ("F","P",100), ("F","I",200),
        ("F","G",65), ("I","J",50), ("J","K",80), ("H","J",120),
        ("G","H",83), ("P","O",110), ("I","K",320), ("I","D",320),
        ("O","M",80), ("L","M",600), ("L","K",320), ("L","D",110),
        ("P","K",100),
    ]
    for src, dst, w in weighted_edges:
        m[idx[src]][idx[dst]] = w
    graphs["4.JPG — Weighted directed (16 nodes)"] = Graph(m, labels_4, graph_type=True)

    # ------------------------------------------------------------------
    # 5.JPG — Decision tree (flowchart)
    # A→B, A→C, B→C, C→D, C→E, B→F, D→G, E→H, F→I, G→I, H→I, I→J, I→K
    # ------------------------------------------------------------------
    labels_5 = list("ABCDEFGHIJK")
    n = len(labels_5)
    idx = {l: i for i, l in enumerate(labels_5)}
    m = np.zeros((n, n), dtype=int)
    for src, dst in [("A","B"),("A","C"),("B","C"),("C","D"),("C","E"),
                     ("B","F"),("D","G"),("E","H"),("F","I"),("G","I"),("H","I"),
                     ("I","J"),("I","K")]:
        m[idx[src]][idx[dst]] = 1
    graphs["5.JPG — Decision tree (11 nodes)"] = Graph(m, labels_5, graph_type=False)

    # ------------------------------------------------------------------
    # 12.JPG + 13.JPG — Molecular graphs (undirected)
    # Propane: chain of 3 carbon atoms with hydrogens (simplified)
    # ------------------------------------------------------------------
    # Simplified propane: C1-C2-C3 backbone
    labels_prop = ["C1", "C2", "C3"]
    m = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ])
    graphs["12.JPG — Propane backbone (undirected)"] = Graph(m, labels_prop, graph_type=False)

    return graphs


# ======================================================================
# Main — test all graphs
# ======================================================================

def main():
    print("=" * 60)
    print("  TASK 11: Graphs — Class with adjacency/incidence matrices")
    print("=" * 60)

    all_graphs = build_all_graphs()

    for name, g in all_graphs.items():
        g.pretty_print(title=name)
        g.summary()

        print(f"\n  --- Conversion test ---")
        inc = g.to_incidence()
        inc.pretty_print(title=f"{name} (converted to INCIDENCE)")

        back = inc.to_adjacency()
        matrices_match = np.array_equal(
            g.mat != 0,
            back.mat != 0
        )
        print(f"  Round-trip conversion match: {matrices_match}")

        print(f"\n{'#' * 60}\n")

    # ------------------------------------------------------------------
    # Extra demo: shortest path on weighted graph (4.JPG)
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  SHORTEST PATH DEMO — Weighted graph (4.JPG)")
    print("=" * 60)

    weighted_g = all_graphs["4.JPG — Weighted directed (16 nodes)"]
    test_paths = [("A", "D"), ("F", "M"), ("A", "K")]
    for start, end in test_paths:
        dist, path = weighted_g.shortest_path(start, end)
        if path:
            print(f"\n  {start} -> {end}: distance = {dist}, path = {' -> '.join(path)}")
        else:
            print(f"\n  {start} -> {end}: no path found")


if __name__ == "__main__":
    main()