from abc import ABC


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
		State.window.set_step_button(False)
		State.window.set_select_button(True)

		gw = State.graph_widget
		gw.mouseReleaseEvent = lambda event: None

	def select_click(self):
		State.window.set_state(SelectSourceState())


class SelectSourceState(State):
	def __init__(self):
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


class SelectDestinationState(State):
	def __init__(self):
		State.window.set_step_button(False)
		State.window.set_select_button(False)

		gw = State.graph_widget
		gw.mouseReleaseEvent = lambda event: self.set_destination_vertex(gw.childAt(event.pos()))

	def set_destination_vertex(self, vertex_widget):
		print("selected: " + str(vertex_widget.get_vertex()))
		State.window.set_destination(vertex_widget.get_vertex())
		State.graph_widget.dijkstra_init(State.window.get_source(), vertex_widget)
		State.window.set_state(AlgorithmState())

	def reset_click(self):
		State.window.set_state(DefaultState())


class AlgorithmState(State):
	def __init__(self):
		State.window.set_step_button(True)
		State.window.set_select_button(False)
		State.window.dijkstra_init()

	def step_click(self):
		State.graph_widget.dijkstra_step()
		State.graph_widget.update()
		State.window.update()

	def reset_click(self):
		State.window.set_state(DefaultState())
