import sys
from PyQt5.QtWidgets import QApplication
from gui import TreeVisualizer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = TreeVisualizer()
    visualizer.show()
    sys.exit(app.exec_())