from abc import ABC
from PySide2 import QtCore, QtWidgets, QtGui
from vertexsystem.vertex import *


# State design pattern
class State(ABC):
	window = None
	graph_widget = None

	def __init__(self):
		pass

	def select_click(self):
		pass

	def step_click(self):
		pass

	def reset_click(self):
		pass


class DefaultState(State):
	def __init__(self):
		super().__init__()
		State.window.set_step_button(False)
		State.window.set_select_button(True)

		self.gw = State.graph_widget
		self.gw.contextMenuEvent = self.context_menu

	def select_click(self):
		State.window.set_state(SelectSourceState())
		self.gw.contextMenuEvent = None

	def context_menu(self, event):
		self.gw = State.graph_widget
		menu = QtWidgets.QMenu(self.gw)
		action = QtWidgets.QAction("Add Vertex")

		menu.addAction(action)
		action.triggered.connect(self.add_vertex)
		self.event = event

		menu.exec_(event.globalPos())

	def add_vertex(self):
		vert = Vertex()

		pos = self.gw.get_grid_cell(self.event.pos())
		self.gw.add_vertex(vert, pos[0], pos[1])


class BuildGraphState(State):
	def __init__(self):
		super().__init__()


class SelectSourceState(State):
	def __init__(self):
		super().__init__()
		State.window.set_step_button(False)
		State.window.set_select_button(False)

		gw = State.graph_widget
		gw.mouseReleaseEvent = lambda event: self.set_source_vertex(gw.childAt(event.pos()))

	def set_source_vertex(self, vertex_widget):
		print("selected: " + str(vertex_widget.get_vertex()))
		vertex_widget.select_animatinon()

		State.window.set_source(vertex_widget.get_vertex())
		State.window.set_state(SelectDestinationState())

	def reset_click(self):
		State.window.set_state(DefaultState())
		State.graph_widget.reset()


class SelectDestinationState(State):
	def __init__(self):
		super().__init__()
		State.window.set_step_button(False)
		State.window.set_select_button(False)

		gw = State.graph_widget
		gw.mouseReleaseEvent = lambda event: self.set_destination_vertex(gw.childAt(event.pos()))

	def set_destination_vertex(self, vertex_widget):
		print("selected: " + str(vertex_widget.get_vertex()))
		vertex_widget.select_animatinon()

		State.window.set_destination(vertex_widget.get_vertex())
		State.graph_widget.dijkstra_init(State.window.get_source(), vertex_widget)
		State.window.set_state(AlgorithmState())

		gw = State.graph_widget
		gw.mouseReleaseEvent = lambda event: None

	def reset_click(self):
		State.window.set_state(DefaultState())
		State.graph_widget.reset()


class AlgorithmState(State):
	def __init__(self):
		super().__init__()
		State.window.set_step_button(True)
		State.window.set_select_button(False)
		State.window.dijkstra_init()

	def step_click(self):
		State.graph_widget.dijkstra_step()
		State.graph_widget.update()
		State.window.update()

	def reset_click(self):
		State.window.set_state(DefaultState())
		State.graph_widget.reset()
