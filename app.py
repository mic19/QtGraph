import sys
from graphui import *
from state import *
from graphutils import Graph, Vertex


class GraphMainWindow(QtWidgets.QMainWindow):
	def __init__(self, graph: Graph):
		super().__init__()
		self._state = None
		self._source = None
		self._destination = None

		self._toolbar = QtWidgets.QToolBar()
		label = QtWidgets.QLabel("Dijkstra algorithm visualizer. Select starting and ending vertices \n"
								 + "and click Step to run the algorithm. ")

		self._graph = graph
		self._graph_widget = GraphWidget(graph=graph)
		self._select_button = QtWidgets.QPushButton("Select")
		self._select_button.setFixedSize(100, 30)
		self._select_button.clicked.connect(lambda: self._state.select_click())

		self._step_button = QtWidgets.QPushButton("Step")
		self._step_button.setFixedSize(100, 30)
		self._step_button.clicked.connect(lambda: self._state.step_click())

		self._reset_button = QtWidgets.QPushButton("Reset")
		self._reset_button.setFixedSize(100, 30)
		self._reset_button.clicked.connect(lambda: self._state.reset_click())

		self._toolbar.addWidget(label)
		self._toolbar.addWidget(self._select_button)
		self._toolbar.addWidget(self._step_button)
		self._toolbar.addWidget(self._reset_button)

		self.addToolBar(self._toolbar)
		self.setCentralWidget(self._graph_widget)

	def get_graph_widget(self) -> GraphWidget:
		return self._graph_widget

	def get_source(self) -> Vertex:
		return self._source

	def get_destination(self) -> Vertex:
		return self._destination

	def set_select_button(self, enabled: bool = True) -> None:
		self._select_button.setEnabled(enabled)

	def set_step_button(self, enabled: bool = True) -> None:
		self._step_button.setEnabled(enabled)

	def set_state(self, state: State) -> None:
		self._state = state

	def set_source(self, source: Vertex) -> None:
		self._source = source

	def set_destination(self, destination: Vertex) -> None:
		self._destination = destination

	def dijkstra_init(self) -> None:
		self._graph.dijkstra_init(self._source, self._destination)


if __name__ == '__main__':
	# Example
	app = QtWidgets.QApplication(sys.argv)

	vert_a = Vertex()
	vert_b = Vertex()
	vert_c = Vertex()
	vert_d = Vertex()
	vert_e = Vertex()
	vert_f = Vertex()
	vert_g = Vertex()
	vert_h = Vertex()
	vert_i = Vertex()
	vert_j = Vertex()

	graph = Graph()
	graph.append(vert_a)
	graph.append(vert_b)
	graph.append(vert_c)
	graph.append(vert_d)
	graph.append(vert_e)
	graph.append(vert_f)
	graph.append(vert_g)
	graph.append(vert_h)
	graph.append(vert_i)
	graph.append(vert_j)

	graph.connect(vert_a, vert_b, 1)
	graph.connect(vert_a, vert_c, 2)
	graph.connect(vert_b, vert_d, 1)
	graph.connect(vert_e, vert_a, 7)

	graph.connect(vert_a, vert_f, 4)
	graph.connect(vert_a, vert_g, 3)
	graph.connect(vert_h, vert_d, 3)
	graph.connect(vert_j, vert_e, 4)

	graph.connect(vert_j, vert_b, 5)
	graph.connect(vert_i, vert_c, 6)
	graph.connect(vert_h, vert_g, 7)
	graph.connect(vert_i, vert_f, 7)

	graph.connect(vert_a, vert_e, 8)
	graph.connect(vert_c, vert_i, 2)
	graph.connect(vert_b, vert_j, 4)
	graph.connect(vert_e, vert_h, 7)

	# UI
	window = GraphMainWindow(graph)
	State.window = window
	State.graph_widget = window.get_graph_widget()
	window.set_state(DefaultState())

	window.show()
	sys.exit(app.exec_())
