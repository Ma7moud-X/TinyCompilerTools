from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QPushButton, QTextEdit, QLabel, QWidget, QMessageBox
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import sys
from Parser import Parser
from scanner import Scanner

matplotlib.use("TkAgg")


class TreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.node_mapping = {}
        self.hidden_edges = set()
        self.node_shapes = {}
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
            if 0 < x then
            fact := 1;
            repeat
            fact := fact * x;
            x := x - 1
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
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self,
                "Select Input File",
                "",
                "Text Files (*.txt);;All Files (*)"
            )
            
            if filename:
                output_filepath = "./output.txt"
                scanner = Scanner(filename, output_filepath)
                tokens = scanner.scan_file()

                parser = Parser(tokens, self)
                parse_tree, retry = parser.parse()
                
                if retry:
                    return
                    
                if parse_tree:
                    graph = nx.DiGraph()
                    self.build_graph(parse_tree, graph)
                    self.visualize_graph(graph, root=parse_tree.value, index=parse_tree.index)
                    
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Error opening file: {str(e)}")
            msg.setWindowTitle("File Error")
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
            
            retval = msg.exec_()
            
            if retval == QMessageBox.Retry:
                plt.close('all')
                self.choose_file()  # Retry file selection
            elif retval == QMessageBox.Close:
                plt.close('all')
                sys.exit()

    def parse_and_visualize(self):
        input_code = self.input_code.toPlainText()
        output_filepath = "./output.txt"


        scanner = Scanner(None, output_filepath)
        tokens = scanner.scan_string(input_code)

        parser = Parser(tokens, self)  # Pass self as GUI reference
        parse_tree, retry = parser.parse()
    
        if retry:
            return

        graph = nx.DiGraph()
        self.build_graph(parse_tree, graph)
        # print(graph)
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Accepted by TINY language")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
        self.visualize_graph(graph, root=parse_tree.value, index=parse_tree.index)
        
        

    def build_graph(self, tree, graph, parent=None):
        
        node_id = f"{tree.value}_{tree.index}"
        self.node_mapping[node_id] = tree.value
        self.node_shapes[node_id] = tree.shape

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
            self.node_shapes[sibling_id] = sibling.shape
            
            graph.add_edge(node_id, sibling_id)  
            self.build_graph(sibling, graph, parent)
            sibling = sibling.sibling

    def visualize_graph(self, graph, root, index):
        
        # Remove first node (Program) From the GUI
        g = graph.copy()
        first_node = list(graph.nodes())[0]
        g.remove_node(first_node)
        
        root_id = f"{root}_{index}"
        pos = self.layout(graph, root=root_id)

        # Calculate figure size based on number of nodes
        n_nodes = len(g.nodes())
        width = max(12, n_nodes * 0.5)  # Minimum width of 12
        height = max(8, n_nodes * 0.3)   # Minimum height of 8
        
        plt.figure(figsize=(width, height))
        labels = {node: self.node_mapping[node] for node in g.nodes()}
        visible_edges = [(u, v) for (u, v) in g.edges() if (u, v) not in self.hidden_edges]

        for node in g.nodes():
            nx.draw_networkx_nodes(g,
                pos,
                nodelist=[node],
                node_shape=self.node_shapes[node],
                node_size=3500,
                node_color="lightgreen")

        nx.draw_networkx_edges(g,
            pos,
            edgelist=visible_edges,
            arrows=True,
            edge_color='gray',
            width=2)
        nx.draw_networkx_labels(g,
            pos,
            labels=labels,
            font_size=10)
        
        plt.box(False)        
        plt.margins(0.1)
        plt.show()

    def layout(self, graph, root):
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