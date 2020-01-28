import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPoint
from graphutils import Graph, Vertex
from math import sin, cos


class VertexWidget(QtWidgets.QLabel):
	widget_size = 16

	def __init__(self, parent, color : QtGui.QColor = QtGui.QColor(0 ,100, 200)):
		super().__init__(parent)
		self.setAutoFillBackground(True)

		self.setMinimumSize(VertexWidget.widget_size, VertexWidget.widget_size)
		self.setMaximumSize(VertexWidget.widget_size, VertexWidget.widget_size)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self._color = color

		self.empty = False
		if color is None:
			self.empty = True

		self.setText(str(self))
		self.mimeText = self.text()

	def paintEvent(self, event: QtGui.QPaintEvent):
		qp = QtGui.QPainter()
		qp.begin(self)

		qp.setPen(QtGui.QColor(255, 255, 255))
		if self._color is not None:
			qp.setBrush(self._color)
			circle_size = VertexWidget.widget_size / 2
			qp.drawEllipse(QPoint(circle_size, circle_size), circle_size, circle_size)

		qp.end()

	def set_color(self, color: QtGui.QColor):
		self._color = color

	def mouseMoveEvent(self, event):
		self.setText(str(self))

		mime_data = QtCore.QMimeData()
		mime_data.setText(self.mimeText)
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime_data)
		drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)


"""
Widget contains exactly one VertexWidget.
The VertexWidget object can be replaced (by dragging) between two DragAndDropWidgets
"""
class DragAndDropWidget(QtWidgets.QWidget):
	margin = 2
	widget_size = VertexWidget.widget_size + margin

	def __init__(self, parent, vertex_widget: VertexWidget = None):
		super().__init__(parent)
		self.setAcceptDrops(True)
		self._content_layout = QtWidgets.QVBoxLayout(self)
		self._content_layout.setAlignment(QtCore.Qt.AlignCenter)
		margin = DragAndDropWidget.margin
		self._content_layout.setContentsMargins(margin, margin, margin, margin)
		self.setLayout(self._content_layout)

		self._vertex = vertex_widget
		if self._vertex is not None:
			self._content_layout.addWidget(self._vertex)
			self._vertex.setParent(self)

		size = VertexWidget.widget_size + 2 * margin
		self.setFixedSize(size, size)

	def dragEnterEvent(self, event):
		if event.mimeData().hasText():
			event.setDropAction(QtCore.Qt.CopyAction)
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasText():
			vertex_source = event.source()

			if vertex_source not in self.children():
				self._content_layout.removeWidget(self._vertex)

				self.set_vertex(vertex_source)
				self._content_layout.addWidget(self._vertex)
				self._vertex.setParent(self)

				vertex_source.clear()
			else:
				event.ignore()
		else:
			event.ignore()

	def paintEvent(self, event: QtGui.QPaintEvent):
		qp = QtGui.QPainter()
		qp.begin(self)

		qp.setPen(QtGui.QColor(200, 200, 200))
		qp.setBrush(QtGui.QColor(200, 200, 200))

		size = self.size()
		width = size.width() - 1
		height = size.height() - 1

		qp.drawLine(0, 0, width, 0)
		qp.drawLine(0, 0, 0, height)
		qp.drawLine(width, height, width, 0)
		qp.drawLine(width, height, 0, height)

		qp.end()

	def set_vertex(self, vertex: VertexWidget):
		self._vertex = vertex


class GraphWidget(QtWidgets.QDialog):
	# Width and height are number of cells in grid - horizontally and vertically
	width = 30
	height = 30

	class OverlayWidget(QtWidgets.QWidget):
		def __init__(self, parent, edges: list):
			super().__init__(parent)
			self._edges = edges

		def setEdges(self, edges: list):
			self._edges = edges

		def paintEvent(self, event: QtGui.QPaintEvent):
			qp = QtGui.QPainter()
			qp.begin(self)

			qp.setPen(QtGui.QColor(10, 10, 10))
			qp.setBrush(QtGui.QColor(200, 200, 200))

			for edge in self._edges:
				a = edge[0]
				b = edge[1]

				qp.drawLine(a, b)
				qp.drawText((a + b)/2, str(edge[2]))

			qp.end()

	def __init__(self, graph : Graph, parent=None):
		super(GraphWidget, self).__init__(parent)

		self.setMinimumSize(200, 200)
		self.setWindowTitle("Drag and Drop Graph")
		self._graph = graph
		self._vert_widget_dict = {}
		self._vert_point_dict = {}

		layout = QtWidgets.QGridLayout(self)
		layout.setHorizontalSpacing(0)
		layout.setVerticalSpacing(0)
		layout.setMargin(0)

		# Insert empty vertices
		for i in range(GraphWidget.width):
			for j in range(GraphWidget.height):
				empty_vertex = VertexWidget(self, None)
				layout.addWidget(DragAndDropWidget(self, empty_vertex), i, j)

		for vert, point in zip(graph, self._generate_points(len(graph))):
			item_to_remove = layout.itemAtPosition(point[0], point[1])
			widget = item_to_remove.widget()
			layout.removeItem(item_to_remove)
			widget.deleteLater()

			vertex_widget = VertexWidget(self, QtGui.QColor(200, 10, 20))
			vertex_widget.setToolTip(str(vert))
			drag_drop_vert = DragAndDropWidget(self, vertex_widget)

			layout.addWidget(drag_drop_vert, point[0], point[1])
			self._vert_widget_dict[vert] = vertex_widget

		self.layout = layout

		# Widget on top of everything (drawing edges)
		self._overlay = GraphWidget.OverlayWidget(self, [])
		self._overlay.setFixedSize(622, 622)
		self._overlay.setGeometry(self.layout.geometry())
		self._overlay.raise_()
		self._overlay.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

	# Generate QPoints coordinates to place vertices
	def _generate_points(self, count: int) -> list:
		r = min(GraphWidget.width, GraphWidget.height) / 2 - 3
		center = (GraphWidget.width / 2, GraphWidget.height / 2)
		alpha = 360 / count

		for i in range(count):
			angle = alpha * i
			x, y = r * sin(angle), r * cos(angle)

			if alpha * i <= 90:
				pass
			elif alpha * i <= 180:
				y = -1 * y
			elif alpha * i <= 270:
				x, y = -1 * x, -1 * y
			elif alpha * i <= 360:
				x = -1 * x

			yield center[0] + x, center[1] + y

	def paintEvent(self, event: QtGui.QPaintEvent):
		edges = []
		for vert in graph:
			for conn in vert:
				widget_a = self._vert_widget_dict[vert].parent()
				widget_b = self._vert_widget_dict[conn[0]].parent()

				index_a = self.layout.indexOf(widget_a)
				index_b = self.layout.indexOf(widget_b)

				pos_a = self.layout.getItemPosition(index_a)
				pos_b = self.layout.getItemPosition(index_b)

				w_coeff = self.layout.totalMinimumSize().width() / self.layout.columnCount()
				h_coeff = self.layout.totalMinimumSize().height() / self.layout.rowCount()

				a = QPoint(pos_a[1] * w_coeff, pos_a[0] * h_coeff)
				b = QPoint(pos_b[1] * w_coeff, pos_b[0] * h_coeff)

				a += QPoint(DragAndDropWidget.widget_size / 2, DragAndDropWidget.widget_size / 2)
				b += QPoint(DragAndDropWidget.widget_size / 2, DragAndDropWidget.widget_size / 2)

				weigh = conn[1]
				edges.append([a, b, weigh])

		self._overlay.setEdges(edges)
		self._overlay.update()


if __name__ == '__main__':
	# Example
	app = QtWidgets.QApplication(sys.argv)

	vert_a = Vertex("vert_a")
	vert_b = Vertex("vert_b")
	vert_c = Vertex("vert_c")
	vert_d = Vertex("vert_d")
	vert_e = Vertex("vert_e")

	vert_a.connect(vert_b, 10)
	vert_a.connect(vert_c, 20)
	vert_b.connect(vert_d, 10)

	graph = Graph()
	graph.append(vert_a)
	graph.append(vert_b)
	graph.append(vert_c)
	graph.append(vert_d)
	graph.append(vert_e)

	window = GraphWidget(graph=graph)
	window.show()
	sys.exit(app.exec_())