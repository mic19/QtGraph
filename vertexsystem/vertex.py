from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QPoint
from graphutils import Vertex


class VertexWidget(QtWidgets.QLabel):
	vertex_size = 20

	def __init__(self, parent, color: QtGui.QColor = QtGui.QColor(0, 100, 200), text: str = "", vertex: Vertex = None):
		super().__init__(parent)
		self.setAutoFillBackground(True)

		self.setMinimumSize(VertexWidget.vertex_size, VertexWidget.vertex_size)
		self.setMaximumSize(VertexWidget.vertex_size, VertexWidget.vertex_size)
		self.setAlignment(QtCore.Qt.AlignCenter)

		self._color = color
		self._position = None
		self._text = text
		self._vertex = vertex

		self.empty = False
		if color is None:
			self.empty = True

		self.setText(str(self))
		self.mimeText = self.text()

	def paintEvent(self, event: QtGui.QPaintEvent):
		qp = QtGui.QPainter()
		qp.begin(self)

		if self._color is not None:
			qp.setPen(QtGui.QColor(255, 255, 255))
			qp.setBrush(self._color)
			circle_size = VertexWidget.vertex_size / 2
			qp.drawEllipse(QPoint(circle_size, circle_size), circle_size, circle_size)

			qp.setPen(QtGui.QColor(10, 10, 10))
			qp.drawText(QPoint(circle_size, circle_size) + QPoint(-3, 4), self._text)

		qp.end()

	def mouseMoveEvent(self, event):
		self.setText(str(self))

		mime_data = QtCore.QMimeData()
		mime_data.setText(self.mimeText)
		drag = QtGui.QDrag(self)
		drag.setMimeData(mime_data)
		drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

		self.update_position()

	def set_color(self, color: QtGui.QColor) -> None:
		self._color = color

	# Set text label inside the vertex
	def set_text(self, text: str) -> None:
		self._text = text

	# Setting QPoint position of the widget based on position in grid layout
	def update_position(self) -> None:
		curr_drag_widget = self.parent()

		grid_layout = DragAndDropWidget.grid_layout
		index = grid_layout.indexOf(curr_drag_widget)
		pos = grid_layout.getItemPosition(index)

		w_coeff = grid_layout.totalMinimumSize().width() / grid_layout.columnCount()
		h_coeff = grid_layout.totalMinimumSize().height() / grid_layout.rowCount()

		qpoint = QPoint(pos[1] * w_coeff, pos[0] * h_coeff)
		qpoint += QPoint(DragAndDropWidget.dag_size / 2, DragAndDropWidget.dag_size / 2)

		self._position = qpoint

	def get_postition(self) -> QtCore.QPoint:
		return self._position

	def get_vertex(self) -> Vertex:
		return self._vertex

"""
Widget contains exactly one VertexWidget.
The VertexWidget object can be replaced (by dragging) between two DragAndDropWidgets
"""
class DragAndDropWidget(QtWidgets.QWidget):
	margin = 2
	dag_size = VertexWidget.vertex_size + margin
	grid_layout = None

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

		size = VertexWidget.vertex_size + 2 * margin
		self.setFixedSize(size, size)

		DragAndDropWidget.grid_layout = parent.layout()

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

	def set_vertex(self, vertex: Vertex) -> None:
		self._vertex = vertex
