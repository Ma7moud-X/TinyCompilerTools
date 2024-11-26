import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QTextEdit, QLabel, QWidget
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
from parser import Parser
from scanner import Scanner

matplotlib.use("TkAgg")


class TreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.node_mapping = {}
        self.hidden_edges = set()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TINY Language Parser')

        layout = QVBoxLayout()

        self.label = QLabel("Enter TINY code:")
        layout.addWidget(self.label)
        self.input_code = QTextEdit()
        self.input_code.setPlainText(
            """
            read x;
            read x;
            read x;
            if 0 < x then
            fact := 14848;
            repeat
            fact := fact * x;
            xta := xta - 1
            until x = 0;
            write fact 
            end"""
        )
        layout.addWidget(self.input_code)

        self.parse_button = QPushButton("Parse and Visualize")
        self.parse_button.clicked.connect(self.parse_and_visualize)
        layout.addWidget(self.parse_button)

        self.choose_file_button = QPushButton("Choose File")
        self.choose_file_button.clicked.connect(self.choose_file)
        layout.addWidget(self.choose_file_button)

        self.setLayout(layout)
        self.setGeometry(100, 100, 400, 600)

    def choose_file(self):
        input_filepath = "./test.txt"
        output_filepath = "./output.txt"

        with open(input_filepath, "w") as f:
            f.write(self.input_code.toPlainText())

        scanner = Scanner(input_filepath, output_filepath)
        tokens = scanner.scan_file()

        parser = Parser(tokens)
        parse_tree = parser.parse()

        graph = nx.DiGraph()
        self.build_graph(parse_tree, graph)

        self.visualize_graph(graph, root=parse_tree.value)

    def parse_and_visualize(self):
        input_filepath = "./test.txt"
        output_filepath = "./output.txt"

        with open(input_filepath, "w") as f:
            f.write(self.input_code.toPlainText())

        scanner = Scanner(input_filepath, output_filepath)
        tokens = scanner.scan_file()

        parser = Parser(tokens)
        parse_tree = parser.parse()

        graph = nx.DiGraph()
        self.build_graph(parse_tree, graph)
        print(graph)
        self.visualize_graph(graph, root=parse_tree.value, index=parse_tree.index)

    def build_graph(self, tree, graph, parent=None):
        
        node_id = f"{tree.value}_{tree.index}"
        self.node_mapping[node_id] = tree.value
        
        graph.add_node(node_id)  
        if parent:
            graph.add_edge(parent, node_id)
            if not tree.edge:
                self.hidden_edges.add((parent, node_id))  
        for child in tree.children:
            self.build_graph(child, graph, node_id)

        sibling = tree.sibling
        while sibling:
            sibling_id = f"{sibling.value}_{sibling.index}"
            self.node_mapping[sibling_id] = sibling.value

            graph.add_edge(node_id, sibling_id)  
            self.build_graph(sibling, graph, parent)
            sibling = sibling.sibling

    def visualize_graph(self, graph, root, index):
        root_id = f"{root}_{index}"
        pos = self.layout(graph, root=root_id)

        # Calculate figure size based on number of nodes
        n_nodes = len(graph.nodes())
        width = max(12, n_nodes * 0.5)  # Minimum width of 12
        height = max(8, n_nodes * 0.3)   # Minimum height of 8
        
        plt.figure(figsize=(width, height))
        labels = {node: self.node_mapping[node] for node in graph.nodes()}
        visible_edges = [(u, v) for (u, v) in graph.edges() if (u, v) not in self.hidden_edges]

        nx.draw(graph, 
                pos, 
                labels=labels,
                with_labels=True, 
                node_size=3500,
                node_color="lightgreen", 
                font_size=10, 
                arrows=True,
                edge_color='gray',
                width=2,
                edgelist = visible_edges)
        plt.title("Parse Tree Visualization", fontsize=12)
        plt.margins(0.1)
        plt.show()

    def layout(self, graph, root):
        # Initialize positions dictionary
        pos = {}
           
        # Get all nodes and their levels from root
        levels = {node: len(nx.shortest_path(graph, root, node)) - 1 
                for node in graph.nodes()}
        
        # Group nodes by level
        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level:
                nodes_by_level[level] = []
            nodes_by_level[level].append(node)
        
        # Calculate max level for scaling
        max_level = max(levels.values())
        
        # Position nodes level by level
        for level in range(max_level + 1):
            nodes = nodes_by_level.get(level, [])
            n_nodes = len(nodes)
            
            # Calculate x spacing with left alignment
            x_base = 0.2  # Start from 20% of the width
            x_width = 0.6  # Use 60% of total width for spacing
            x_spacing = x_width / max(n_nodes, 1)
            
            for i, node in enumerate(nodes):
                # x coordinate starts from left
                x = x_base + (i * x_spacing)
                
                # y coordinate moves top to bottom
                y = 1.0 - (level / (max_level + 1))
                
                pos[node] = (x, y)
        
        return pos


if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = TreeVisualizer()
    visualizer.show()
    sys.exit(app.exec_())