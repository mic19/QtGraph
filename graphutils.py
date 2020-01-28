

class Vertex:
	def __init__(self, name):
		# Dictionary of vertices this vertex is connected to {other_vertex, weigh}
		self._verts_dict = {}
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

	# Add two way connection
	def connect(self, vertex: "Vertex", weigh: float) -> None:
		self._verts_dict.update({vertex: weigh})
		self._keys_list.append(vertex)
		# the other way
		vertex._verts_dict.update({self: weigh})
		vertex._keys_list.append(self)

	def keys(self) -> list:
		return self._keys_list


class VertexIterator():
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
	def __init__(self):
		self._vertices = []

	def __getitem__(self, key):
		return self._vertices[key]

	def __iter__(self):
		return GraphIterator(self)

	def __len__(self):
		return len(self._vertices)

	def append(self, vertex: Vertex):
		self._vertices.append(vertex)


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
	vert_a = Vertex("vert_a")
	vert_b = Vertex("vert_b")
	vert_c = Vertex("vert_c")

	vert_a.connect(vert_b, 10)
	vert_a.connect(vert_c, 20)

	graph = Graph()
	graph.append(vert_a)
	graph.append(vert_b)
	graph.append(vert_c)

	for i in vert_a:
		print(i)

	for vert in graph:
		print(vert)


