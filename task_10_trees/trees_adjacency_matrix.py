import numpy as np

# ========================================================================
# Binary Tree Node and Tree classes
# ========================================================================

class TreeNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.value})"


class BinaryTree:

    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def get_all_nodes(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def get_edges(self):
        edges = []
        self._collect_edges(self.root, edges)
        return edges

    def _collect_edges(self, node, edges):
        if node:
            if node.left:
                edges.append((node.value, node.left.value))
                self._collect_edges(node.left, edges)
            if node.right:
                edges.append((node.value, node.right.value))
                self._collect_edges(node.right, edges)

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def print_tree(self, node=None, prefix="", is_left=True, is_root=True):
        if is_root:
            node = self.root
            if node is None:
                print("  (empty tree)")
                return
            print(f"  {node.value}")
            if node.right:
                self.print_tree(node.right, "  ", False, False)
            if node.left:
                self.print_tree(node.left, "  ", True, False)
            return

        connector = "└── " if is_left else "┌── "
        print(f"{prefix}{connector}{node.value}")
        new_prefix = prefix + ("    " if is_left else "│   ")
        if not is_left:
            if node.right:
                self.print_tree(node.right, new_prefix, False, False)
            if node.left:
                self.print_tree(node.left, new_prefix, True, False)
        else:
            if node.right:
                self.print_tree(node.right, new_prefix, False, False)
            if node.left:
                self.print_tree(node.left, new_prefix, True, False)


# ========================================================================
# Adjacency Matrix builder and analyzer
# ========================================================================

class AdjacencyMatrixAnalyzer:

    def __init__(self, tree):
        self.tree = tree
        self.nodes = sorted(tree.get_all_nodes())
        self.n = len(self.nodes)
        self.node_index = {v: i for i, v in enumerate(self.nodes)}
        self.matrix = self._build_matrix()

    def _build_matrix(self):
        mat = np.zeros((self.n, self.n), dtype=int)
        edges = self.tree.get_edges()
        for parent, child in edges:
            i = self.node_index[parent]
            j = self.node_index[child]
            mat[i][j] = 1
        return mat

    def print_matrix(self, matrix=None, label=""):
        if matrix is None:
            matrix = self.matrix
        if label:
            print(f"\n--- {label} ---")

        header = "     " + "".join(f"{self.nodes[j]:>4}" for j in range(self.n))
        print(header)
        print("     " + "----" * self.n)

        for i in range(self.n):
            row_label = f"{self.nodes[i]:>3} |"
            row_vals = "".join(f"{matrix[i][j]:>4}" for j in range(self.n))
            print(f"{row_label}{row_vals}")

    # ------------------------------------------------------------------
    # Task 5: Row sums, column sums, total sum
    # ------------------------------------------------------------------

    def row_sums(self):
        return np.sum(self.matrix, axis=1)

    def col_sums(self):
        return np.sum(self.matrix, axis=0)

    def total_sum(self):
        return np.sum(self.matrix)

    def print_sums(self):
        print("\n--- Task 5: Row sums, column sums, total sum ---")

        r_sums = self.row_sums()
        c_sums = self.col_sums()

        print(f"\n  Row sums (out-degree / number of children):")
        for i, node in enumerate(self.nodes):
            print(f"    Node {node}: {r_sums[i]}")

        print(f"\n  Column sums (in-degree / number of parents):")
        for i, node in enumerate(self.nodes):
            print(f"    Node {node}: {c_sums[i]}")

        print(f"\n  Total sum (number of edges): {self.total_sum()}")

    # ------------------------------------------------------------------
    # Task 6: Diagonal sum
    # ------------------------------------------------------------------

    def diagonal_sum(self):
        return np.trace(self.matrix)

    def print_diagonal(self):
        print(f"\n--- Task 6: Diagonal sum ---")
        print(f"  Diagonal sum: {self.diagonal_sum()}")
        print(f"  (In a tree, the diagonal is always 0 — no self-loops)")

    # ------------------------------------------------------------------
    # Task 7: Conclusions about the matrix and the tree (10 questions)
    # ------------------------------------------------------------------

    def find_leaves(self):
        r_sums = self.row_sums()
        return [self.nodes[i] for i in range(self.n) if r_sums[i] == 0]

    def find_root(self):
        c_sums = self.col_sums()
        roots = [self.nodes[i] for i in range(self.n) if c_sums[i] == 0]
        return roots[0] if roots else None

    def measure_depth(self, target_node):
        current = target_node
        depth = 0
        while True:
            col_idx = self.node_index[current]
            # Find parent: which row has a 1 in this column?
            parents = [self.nodes[i] for i in range(self.n) if self.matrix[i][col_idx] == 1]
            if not parents:
                break  # reached root
            current = parents[0]
            depth += 1
        return depth

    def measure_height(self):
        return max(self.measure_depth(node) for node in self.nodes)

    def count_edges(self):
        return int(self.total_sum())

    def count_nodes(self):
        return self.n

    def count_leaves(self):
        return len(self.find_leaves())

    def find_parent(self, node):
        col_idx = self.node_index[node]
        parents = [self.nodes[i] for i in range(self.n) if self.matrix[i][col_idx] == 1]
        return parents[0] if parents else None

    def find_children(self, node):
        row_idx = self.node_index[node]
        return [self.nodes[j] for j in range(self.n) if self.matrix[row_idx][j] == 1]

    def find_siblings(self, node):
        parent = self.find_parent(node)
        if parent is None:
            return []  # root has no siblings
        children = self.find_children(parent)
        return [c for c in children if c != node]

    def print_conclusions(self):
        print(f"\n--- Task 7: Conclusions about the matrix and the tree ---")

        leaves = self.find_leaves()
        print(f"\n  Q1. Leaves (row sum = 0, no outgoing edges): {leaves}")
        print(f"       -> To find a leaf, look for rows where all values are 0.")

        root = self.find_root()
        print(f"\n  Q2. Root (column sum = 0, no incoming edges): {root}")
        print(f"       -> To find the root, look for a column where all values are 0.")

        print(f"\n  Q3. Depth of each node (hops from root via matrix):")
        for node in self.nodes:
            d = self.measure_depth(node)
            print(f"       Node {node}: depth = {d}")
        print(f"       -> Trace parent pointers by checking which row has 1 in the node's column.")

        h = self.measure_height()
        print(f"\n  Q4. Tree height (max depth): {h}")
        print(f"       -> The maximum depth across all nodes.")

        print(f"\n  Q5. Edge count from matrix: {self.count_edges()}")
        print(f"       -> Total sum of all matrix elements = number of edges.")

        print(f"\n  Q6. Node count: {self.count_nodes()}")
        print(f"       -> Dimension of the matrix (N x N).")

        print(f"\n  Q7. Leaf count: {self.count_leaves()}")
        print(f"       -> Count of rows with sum = 0.")

        print(f"\n  Q8. Parent of each node:")
        for node in self.nodes:
            p = self.find_parent(node)
            print(f"       Node {node}: parent = {p if p else '(root, no parent)'}")
        print(f"       -> Find the row that has 1 in the node's column.")

        print(f"\n  Q9. Children of each node:")
        for node in self.nodes:
            ch = self.find_children(node)
            print(f"       Node {node}: children = {ch if ch else '(leaf)'}")
        print(f"       -> Look at the 1s in the node's row — those columns are children.")

        print(f"\n  Q10. Siblings of each node:")
        for node in self.nodes:
            sibs = self.find_siblings(node)
            print(f"       Node {node}: siblings = {sibs if sibs else '(none)'}")
        print(f"       -> Find parent, then find parent's other children.")

    # ------------------------------------------------------------------
    # Task 8: Other coefficients (weighted matrix)
    # ------------------------------------------------------------------

    def build_depth_matrix(self):
        mat = np.zeros((self.n, self.n), dtype=int)
        edges = self.tree.get_edges()
        for parent, child in edges:
            i = self.node_index[parent]
            j = self.node_index[child]
            mat[i][j] = self.measure_depth(child)
        return mat

    def build_subtree_size_matrix(self):
        mat = np.zeros((self.n, self.n), dtype=int)
        subtree_sizes = {}
        self._calc_subtree_sizes(self.tree.root, subtree_sizes)

        edges = self.tree.get_edges()
        for parent, child in edges:
            i = self.node_index[parent]
            j = self.node_index[child]
            mat[i][j] = subtree_sizes.get(child, 1)
        return mat

    def _calc_subtree_sizes(self, node, sizes):
        if node is None:
            return 0
        left_size = self._calc_subtree_sizes(node.left, sizes)
        right_size = self._calc_subtree_sizes(node.right, sizes)
        sizes[node.value] = 1 + left_size + right_size
        return sizes[node.value]

    def print_alternative_matrices(self):
        print(f"\n--- Task 8: Alternative coefficients ---")

        print(f"\n  Using DEPTH of child as coefficient:")
        print(f"  (Row sums give cumulative depth of children — useful for identifying deep branches)")
        depth_mat = self.build_depth_matrix()
        self.print_matrix(depth_mat, "Depth-weighted matrix")

        print(f"\n  Using SUBTREE SIZE of child as coefficient:")
        print(f"  (Helps identify unbalanced subtrees — large values indicate heavy branches)")
        size_mat = self.build_subtree_size_matrix()
        self.print_matrix(size_mat, "Subtree-size-weighted matrix")


# ========================================================================
# Task 9: Balancing the tree (AVL-style)
# ========================================================================

def sorted_array_to_bst(arr):
    if not arr:
        return None
    mid = len(arr) // 2
    node = TreeNode(arr[mid])
    node.left = sorted_array_to_bst(arr[:mid])
    node.right = sorted_array_to_bst(arr[mid + 1:])
    return node


def balance_tree(tree):
    sorted_values = tree.get_all_nodes()
    balanced = BinaryTree()
    balanced.root = sorted_array_to_bst(sorted_values)
    return balanced


# ========================================================================
# Main
# ========================================================================

def main():
    print("=" * 70)
    print("TASK 10: Trees and Binary Trees — Adjacency Matrix Analysis")
    print("=" * 70)

    print("\n--- Task 1: Creating a binary search tree ---")
    tree = BinaryTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 90]
    for v in values:
        tree.insert(v)

    print(f"  Inserted values: {values}")
    print(f"  Tree structure:")
    tree.print_tree()
    print(f"  Height: {tree.height()}")

    analyzer = AdjacencyMatrixAnalyzer(tree)
    analyzer.print_matrix(label="Task 2-4: Adjacency Matrix (1 = edge, 0 = no edge)")

    analyzer.print_sums()

    analyzer.print_diagonal()

    analyzer.print_conclusions()

    analyzer.print_alternative_matrices()

    print(f"\n{'='*70}")
    print("--- Task 9: Balancing the tree ---")
    print(f"{'='*70}")

    unbalanced = BinaryTree()
    skewed_values = [10, 20, 30, 40, 50, 60, 70]
    for v in skewed_values:
        unbalanced.insert(v)

    print(f"\n  Unbalanced (skewed) tree — values inserted: {skewed_values}")
    print(f"  Tree structure:")
    unbalanced.print_tree()
    print(f"  Height: {unbalanced.height()}")

    unb_analyzer = AdjacencyMatrixAnalyzer(unbalanced)
    unb_analyzer.print_matrix(label="Unbalanced tree matrix")

    balanced = balance_tree(unbalanced)
    print(f"\n  Balanced tree:")
    balanced.print_tree()
    print(f"  Height: {balanced.height()}")

    bal_analyzer = AdjacencyMatrixAnalyzer(balanced)
    bal_analyzer.print_matrix(label="Balanced tree matrix")

    print(f"\n--- Comparison ---")
    print(f"  Unbalanced: height={unbalanced.height()}, nodes={len(skewed_values)}")
    print(f"  Balanced:   height={balanced.height()}, nodes={len(skewed_values)}")
    print(f"\n  Characteristics of a balanced tree's adjacency matrix:")
    print(f"    - Row sums are more uniform (most nodes have 2 children)")
    print(f"    - The 1s are distributed more evenly across the matrix")
    print(f"    - In a skewed tree, 1s form a diagonal band (chain-like)")
    print(f"    - In a balanced tree, 1s are spread across multiple rows")
    print(f"    - Height is O(log n) vs O(n) for skewed")

    unb_rsums = unb_analyzer.row_sums()
    bal_rsums = bal_analyzer.row_sums()
    print(f"\n  Unbalanced row sums: {[int(x) for x in unb_rsums]} (most nodes have exactly 1 child)")
    print(f"  Balanced row sums:   {[int(x) for x in bal_rsums]} (most internal nodes have 2 children)")


if __name__ == "__main__":
    main()