from typing import Dict
from vertexsystem.vertex import *
from vertexsystem.overlay import *
from graphutils import Graph, Vertex

class GraphWidget(QtWidgets.QDialog):
	# Width and height are number of cells in grid - horizontally and vertically
	width = 30
	height = 30

	def __init__(self, graph: Graph, parent=None):
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
				empty_vertex.update_position()

		for vert, point in zip(graph, self._generate_points(len(graph))):
			item_to_remove = layout.itemAtPosition(point[0], point[1])
			widget = item_to_remove.widget()
			layout.removeItem(item_to_remove)
			widget.deleteLater()

			vertex_widget = VertexWidget(self, QtGui.QColor(150, 150, 150), vertex=vert)
			vertex_widget.set_text("a")
			vertex_widget.setToolTip(str(vert))
			drag_drop_vert = DragAndDropWidget(self, vertex_widget)

			layout.addWidget(drag_drop_vert, point[0], point[1])
			self._vert_widget_dict[vert] = vertex_widget

		self.layout = layout

		qsize = QtCore.QSize(DragAndDropWidget.dag_size * GraphWidget.width + 50,DragAndDropWidget.dag_size * GraphWidget.height + 50)
		self.setMinimumSize(qsize)

		# Widget on top of everything (drawing edges)
		self._overlay = OverlayWidget(self, [])
		self._overlay.setFixedSize(qsize)
		self._overlay.setGeometry(self.layout.geometry())
		self._overlay.raise_()
		self._overlay.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

	def paintEvent(self, event: QtGui.QPaintEvent):
		edges = []
		arrows = []
		iter = 0

		for vert in self._graph:
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

				a += QPoint(DragAndDropWidget.dag_size / 2, DragAndDropWidget.dag_size / 2)
				b += QPoint(DragAndDropWidget.dag_size / 2, DragAndDropWidget.dag_size / 2)

				weigh = conn[1]
				edges.append([a, b, weigh])

		self._overlay.set_edges(edges)
		self._overlay.update()

	# Generate QPoints coordinates to place vertices
	def _generate_points(self, count: int) -> Tuple[int, int]:
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

	def get_dict(self) -> Dict[Vertex, VertexWidget]:
		return self._vert_widget_dict

	def dijkstra_init(self, source: Vertex, destination: Vertex) -> None:
		self._graph.dijkstra_init(source, destination)

	def dijkstra_step(self, steps: int = 1) -> None:
		self._graph.dijkstra_step(steps)
		distance_dict = self._graph.get_distance_dict()

		for key in distance_dict:
			vertex_widget = self._vert_widget_dict[key]
			vertex_widget.set_text(str(distance_dict[key]))
