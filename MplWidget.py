from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy, QWidget

class MplWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def addFigure(self, qt_layout):
		self.fig = Figure()
		canvas = FigureCanvas(self.fig)
		canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		canvas.updateGeometry()
		qt_layout.addWidget(canvas)

