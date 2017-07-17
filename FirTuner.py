import numpy as np
from numpy.fft import fft

def lpf(num, fp, fs):
	ns = np.arange(num) - num/2 
	F = fp / fs
	def sinc(x):
		return np.sin(x) / x if np.abs(x) > 1E-6 else 1.0
	return np.array([ 2.0 * F * sinc(2.0 * np.pi * F * n) for n in ns])

def hpf(num, fp, fs):
	ns = np.arange(num) - num/2
	# find the zero index
	zero_index = -1
	for k in range(num):
		if np.abs(ns[k]) < 1E-6:
			zero_index = k
			break
	if zero_index < 0:
		raise Exception('Could not find the zero index!')

	fir = lpf(num, fp, fs)
	fir *= -1;
	fir[zero_index] += 1.0
	return fir

def bpf(num, fp, fc, fs):
	fir = lpf(num, fp, fs)
	fir *= np.cos(2.0 * np.pi * fc * np.arange(num) / fs) * 2.0
	return fir

def blackman(num):
	ns = np.arange(num)
	return 0.42 - 0.5 * np.cos(2.0 * np.pi * ns / (num - 1)) + 0.08 * np.cos(4.0 * np.pi * ns / (num - 1))

def hamming(num):
	ns = np.arange(num)
	return 0.54 - 0.46 * np.cos(2.0 * np.pi * ns / (num - 1))

class FirTuner(object):
	def __init__(self, **kwargs):
		self.fir_ax = None
		self.mag_ax = None
		self.fir_handle = None
		self.mag_handle = None
		self.window = 'blackman'
		self.mode = 'lowpass'
		self.fs = 44.1E3
		self.fp = 4E3
		self.fc = 10E3
		self.n = 7

		for kw in kwargs:
			if kw == 'mag_ax':
				self.mag_ax = kwargs[kw]
			if kw == 'fir_ax':
				self.fir_ax = kwargs[kw]
			elif kw == 'window':
				self.window = kwargs[kw]
			elif kw == 'mode':
				self.mode = kwargs[kw]
			elif kw == 'fs':
				self.fs = float(kwargs[kw])
			elif kw == 'fp':
				self.fp = float(kwargs[kw])
			elif kw == 'fc':
				self.fc = float(kwargs[kw])
			elif kw == 'n':
				self.n = int(kwargs[kw])

		self.setWindow(self.window)
		self.setMode(self.mode)
		self.setN(self.n)
		self.calculate()
		self.plot()

	def setFc(self, fc):
		self.fc = float(fc)

	def setFp(self, fp):
		self.fp = float(fp)

	def setN(self, n):
		self.n = int(n)
		self.num = int(np.power(2.0, n))

	def setMode(self, mode):
		if mode == 'lowpass' or mode == 'highpass' or mode == 'bandpass':
			self.mode = mode
		else:
			raise Exception('Unknown mode: %s'%mode)

	def setWindow(self, window):
		if window == 'blackman' or window == 'hamming' or window == 'rectangular':
			self.window = window
		else:
			raise Exception('Unknown window: %s'%window)

	def calculate(self):
		if self.mode == 'lowpass':
			self.fir = lpf(self.num, self.fp, self.fs)

		elif self.mode == 'highpass':
			self.fir = hpf(self.num, self.fp, self.fs)

		elif self.mode == 'bandpass':
			self.fir = bpf(self.num, self.fp, self.fc, self.fs)

		if self.window == 'blackman':
			self.fir *= blackman(self.num)

		elif self.window == 'hamming':
			self.fir *= hamming(self.num)

		self.indecies = np.arange(self.num)

		fft_size = 4 * self.num
		self.fft = fft( np.append(self.fir, np.zeros(fft_size - self.num)) )
		self.freqs = np.arange(fft_size) / float(fft_size) * self.fs / 1000.0
		self.mag = 20.0 * np.log10( np.abs(self.fft) )

	def printCoef(self):
		for k in range(self.num):
			print("[%4d]: %+.10f"%(k, self.fir[k]))

	def plot(self):
		if self.mag_ax is not None:
			if self.mag_handle is None:
				self.mag_handle, = self.mag_ax.plot(self.freqs, self.mag)

			else:
				self.mag_handle.set_xdata(self.freqs)
				self.mag_handle.set_ydata(self.mag)

			self.mag_ax.relim()
			self.mag_ax.autoscale_view()
			self.mag_ax.set_xlim((0, self.fs/2.0/1000.0))

		if self.fir_ax is not None:
			if self.fir_handle is None:
				self.fir_handle, = self.fir_ax.plot(self.indecies, self.fir)

			else:
				self.fir_handle.set_ydata(self.fir)
				self.fir_handle.set_xdata(self.indecies)

			self.fir_ax.relim()
			self.fir_ax.autoscale_view()


if __name__ == '__main__':
	import matplotlib
	matplotlib.use('TkAgg')
	import matplotlib.pyplot as plt
	n = 7
	fs = 44.1E3
	fp = 10E3
	fc = 10E3
	ax1 = plt.subplot(121)
	ax2 = plt.subplot(122)

	tuner = FirTuner(mode='highpass', mag_ax=ax1, fir_ax=ax2, n=n, fs=fs, fc=fc, fp=fp)

	plt.show()
