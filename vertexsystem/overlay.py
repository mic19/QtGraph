from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QPoint
from typing import List
from math import atan, sin, cos


def adjust_line(a: QPoint, b: QPoint, r: int) -> tuple[QPoint, QPoint]:
	if a.x() > b.x():
		a, b = b, a
	elif a.x() == b.x():
		if a.y() >= b.y():
			a, b = b, a

		y_a = a.y() + r + 1
		y_b = b.y() - r + 1

		return QPoint(a.x() + 1, y_a), QPoint(b.x() + 1, y_b)

	x_a, y_a = a.x(), a.y()
	x_b, y_b = b.x(), b.y()

	tg = (y_a - y_b) / (x_b - x_a)
	angle = atan(tg)

	x_a = int(a.x() + r * cos(angle)) + 1
	y_a = int(a.y() - r * sin(angle)) + 1

	x_b = int(b.x() - r * cos(angle)) + 1
	y_b = int(b.y() + r * sin(angle)) + 1

	return QPoint(x_a, y_a), QPoint(x_b, y_b)


class OverlayWidget(QtWidgets.QWidget):
	def __init__(self, parent, edges: List[QtCore.QPoint], arrows: List[QtCore.QPoint] = []):
		super().__init__(parent)
		self._edges = edges
		self._arrows = arrows

	def paintEvent(self, event: QtGui.QPaintEvent):
		qp = QtGui.QPainter()
		qp.begin(self)

		edge_color = QtGui.QColor(250, 10, 10)
		text_color = QtGui.QColor(10, 10, 10)

		qpen = QtGui.QPen(edge_color)
		qpen.setWidth(2)
		qfont = QtGui.QFont()
		qfont.setPixelSize(16)

		qp.setPen(qpen)
		qp.setFont(qfont)

		for edge in self._edges:
			a = edge[0]
			b = edge[1]

			qpen.setColor(edge_color)
			qp.setPen(qpen)

			a, b = adjust_line(a, b, 10)
			qp.drawLine(a, b)

			qpen.setColor(text_color)
			qp.setPen(qpen)
			center = QPoint(int((a.x() + b.x())/2), int((a.y() + b.y())/2))
			qp.drawText(center + QPoint(10, 10), str(edge[2]))

		for arrow in self._arrows:
			a = arrow[0]
			b = arrow[1]

			rect = QtCore.QRect(a, b)
			qp.drawArc(rect, 30 * 16, 120 * 16)

		qp.end()

	def set_edges(self, edges: list) -> None:
		self._edges = edges

	def set_arrows(self, arrows: list) -> None:
		self._arrows = arrows
