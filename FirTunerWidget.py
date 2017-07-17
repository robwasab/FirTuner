import sys
from PyQt5.QtWidgets import QApplication
from Ui_FirTuner import Ui_FirTuner
from MplWidget import MplWidget
import numpy as np
from FirTuner import FirTuner

from numpy.random import rand

class FirTunerWidget(MplWidget, Ui_FirTuner):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setupMpl()
		self.initialize()
		self.fig.tight_layout()
		self.show()

	def initialize(self):
		ax1 = self.fig.add_subplot(121)
		ax2 = self.fig.add_subplot(122)
		self.tuner = FirTuner(mag_ax=ax1, fir_ax=ax2)

		if self.tuner.mode == 'lowpass':
			self.radioButton_lowpass.setChecked(True)
			self.radioButton_highpass.setChecked(False)
			self.radioButton_bandpass.setChecked(False)
		elif self.tuner.mode == 'highpass':
			self.radioButton_lowpass.setChecked(False)
			self.radioButton_highpass.setChecked(True)
			self.radioButton_bandpass.setChecked(False)
		elif self.tuner.mode == 'bandpass':
			self.radioButton_lowpass.setChecked(False)
			self.radioButton_highpass.setChecked(False)
			self.radioButton_bandpass.setChecked(True)

		if self.tuner.window == 'blackman':
			self.radioButton_blackman.setChecked(True)
			self.radioButton_hamming.setChecked(False)
			self.radioButton_rectangular.setChecked(False)
		elif self.tuner.window == 'hamming':
			self.radioButton_blackman.setChecked(False)
			self.radioButton_hamming.setChecked(True)
			self.radioButton_rectangular.setChecked(False)
		elif self.tuner.window == 'rectangular':
			self.radioButton_blackman.setChecked(False)
			self.radioButton_hamming.setChecked(False)
			self.radioButton_rectangular.setChecked(True)

		self.lineEdit_n.setText('%d'%self.tuner.n)
		self.lineEdit_fp.setText('%d'%int(self.tuner.fp))
		self.lineEdit_fc.setText('%d'%int(self.tuner.fc))

		self.lineEdit_n.returnPressed.connect(self.slot_returnPressed)
		self.lineEdit_fp.returnPressed.connect(self.slot_returnPressed)
		self.lineEdit_fc.returnPressed.connect(self.slot_returnPressed)

		self.radioButton_lowpass.toggled[bool].connect(self.slot_lowpassChecked)
		self.radioButton_highpass.toggled[bool].connect(self.slot_highpassChecked)
		self.radioButton_bandpass.toggled[bool].connect(self.slot_bandpassChecked)

		self.radioButton_blackman.toggled[bool].connect(self.slot_blackmanChecked)
		self.radioButton_hamming.toggled[bool].connect(self.slot_hammingChecked)
		self.radioButton_rectangular.toggled[bool].connect(self.slot_rectangularChecked)
		self.button_printCoefficients.clicked.connect(self.tuner.printCoef)

	def setupMpl(self):
		self.addFigure(self.layout_mpl)

	def redraw(self):
		self.tuner.calculate()
		self.tuner.plot()
		self.fig.canvas.draw()

	def slot_returnPressed(self):
		n = int(self.lineEdit_n.text())
		fp = int(self.lineEdit_fp.text())
		fc = int(self.lineEdit_fc.text())
		self.tuner.setN(n)
		self.tuner.setFp(fp)
		self.tuner.setFc(fc)
		self.redraw()

	def slot_lowpassChecked(self, checked):
		if checked:
			self.tuner.setMode('lowpass')
			self.redraw()

	def slot_highpassChecked(self, checked):
		if checked:
			self.tuner.setMode('highpass')
			self.redraw()

	def slot_bandpassChecked(self, checked):
		if checked:
			self.tuner.setMode('bandpass')
			self.redraw()

	def slot_blackmanChecked(self, checked):
		if checked:
			self.tuner.setWindow('blackman')
			self.redraw()

	def slot_hammingChecked(self, checked):
		if checked:
			self.tuner.setWindow('hamming')
			self.redraw()

	def slot_rectangularChecked(self, checked):
		if checked:
			self.tuner.setWindow('rectangular')
			self.redraw()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	wig = FirTunerWidget()
	sys.exit(app.exec_())
