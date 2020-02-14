from typing import List, Dict
import math
import string


class Vertex:
	available_names = list(string.ascii_lowercase)

	def __init__(self, name=None):
		# Dictionary of vertices this vertex is connected to {other_vertex, weigh}
		self._verts_dict = {}

		if name in Vertex.available_names:
			Vertex.available_names.remove(name)
		elif name is None:
			name = Vertex.available_names.pop(0)
		self._name = name

		self._keys_list = []

	def __iter__(self):
		return VertexIterator(self)

	def __str__(self):
		return self._name

	def __len__(self):
		return len(self._verts_dict)

	def __getitem__(self, key):
		return self._verts_dict[key]

	def __lt__(self, other):
		return str(self) < str(other)

	def keys(self) -> List:
		return self._keys_list

	def connect(self, vertex: "Vertex", weigh: float) -> None:
		self._verts_dict.update({vertex: weigh})
		self._keys_list.append(vertex)


class VertexIterator:
	def __init__(self, vertex):
		self._vertex = vertex
		self._keys = vertex.keys()
		self._index = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self._index < len(self._keys):
			key = self._keys[self._index]
			self._index += 1
			return key, self._vertex[key]

		raise StopIteration


class Graph:
	def __init__(self, *args, **kwargs):
		self._vertices = []
		# Fields to be initialized in dijkstra_init
		self._distance_dict = None
		self._queue = None
		self._source = None
		self._destination = None
		self._iter = None
		self._vert = None
		self._vert_iter = None
		self._done_with_for_loop = None

		for arg in args:
			self._vertices.append(arg)

	def __getitem__(self, key):
		return self._vertices[key]

	def __iter__(self):
		return GraphIterator(self)

	def __len__(self):
		return len(self._vertices)

	def append(self, vertex: Vertex) -> None:
		self._vertices.append(vertex)

	def connect(self, vert_1: Vertex, vert_2: Vertex, weigh: float) -> None:
		if vert_1 in self._vertices and vert_2 in self._vertices:
			vert_1.connect(vert_2, weigh)
			vert_2.connect(vert_1, weigh)

	def dijkstra(self, source: Vertex, destination: Vertex) -> Dict[Vertex, float]:
		distance_dict = {vert: math.inf for vert in self._vertices}
		distance_dict[source] = 0
		queue = {k: v for k, v in sorted(distance_dict.items(), key=lambda item: item[1])}

		while len(queue) > 0:
			vert = next(iter(queue))
			queue.pop(vert)

			for conn in vert:
				neighbor, weigh = conn[0], conn[1]

				if distance_dict[vert] + weigh < distance_dict[neighbor]:
					distance_dict[neighbor] = distance_dict[vert] + weigh
					queue[neighbor] = distance_dict[vert] + weigh

					queue = {k: v for k, v in sorted(queue.items(), key=lambda item: item[1])}

		return distance_dict[destination]

	def dijkstra_init(self, source: Vertex, destination: Vertex) -> None:
		self._distance_dict = {vert: math.inf for vert in self._vertices}
		self._distance_dict[source] = 0
		self._queue = {k: v for k, v in sorted(self._distance_dict.items(), key=lambda item: item[1])}
		self._source = source
		self._destination = destination
		self._vert = next(iter(self._queue))
		self._done_with_for_loop = True

	def dijkstra_step(self, steps=1) -> None:
		if steps == 0:
			return

		steps -= 1
		self.dijkstra_step(steps)

		# Step by step while loop from self.dijkstra
		if len(self._queue) > 0 and self._done_with_for_loop is True:
			self._vert = next(iter(self._queue))
			self._vert_iter = iter(self._vert)

			self._queue.pop(self._vert)
			self._done_with_for_loop = False

		# Step by step for loop
		try:
			conn = next(self._vert_iter)
			neighbor, weigh = conn[0], conn[1]
			vert = self._vert

			if self._distance_dict[vert] + weigh < self._distance_dict[neighbor]:
				self._distance_dict[neighbor] = self._distance_dict[vert] + weigh
				self._queue[neighbor] = self._distance_dict[vert] + weigh

				self._queue = {k: v for k, v in sorted(self._queue.items(), key=lambda item: item[1])}
		except StopIteration:
			self._done_with_for_loop = True

	def get_distance_dict(self) -> Dict[Vertex, float]:
		return self._distance_dict

	def get_curr_vert(self) -> Vertex:
		return self._vert


class GraphIterator:
	def __init__(self, graph):
		self._graph = graph
		self._index = 0

	def __iter__(self):
		return self

	def __next__(self):
		if self._index < len(self._graph):
			out = self._graph[self._index]
			self._index += 1
			return out

		raise StopIteration


if __name__ == "__main__":
	# Example
	vert_a = Vertex("vert_a")
	vert_b = Vertex("vert_b")
	vert_c = Vertex("vert_c")
	vert_d = Vertex("vert_d")
	vert_e = Vertex("vert_e")
	vert_f = Vertex("vert_f")

	graph = Graph(vert_a, vert_b, vert_c, vert_d, vert_e, vert_f)

	graph.connect(vert_a, vert_c, 14)
	graph.connect(vert_a, vert_d, 9)
	graph.connect(vert_a, vert_e, 7)

	graph.connect(vert_b, vert_c, 9)
	graph.connect(vert_b, vert_f, 6)

	graph.connect(vert_d, vert_c, 2)
	graph.connect(vert_d, vert_e, 10)
	graph.connect(vert_d, vert_f, 11)

	graph.connect(vert_e, vert_f, 15)

	graph.dijkstra(vert_a, vert_b)

	# Show algorithm step by step
	graph.dijkstra_init(vert_a, vert_b)
	graph.dijkstra_step(15)

	distance_dict = graph.get_distance_dict()
	for key in distance_dict:
		print(str(key) + " " + str(distance_dict[key]))



