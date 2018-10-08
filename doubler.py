# doubler

import aifc

class doubler:
	def load(self, path_in):
		if self.audio_in:
			self.audio_in.close()
		self.path_in = path_in
		self.audio_in = aifc.open(path_in, 'r')

		# just for now
		assert self.audio_in.getnchannels() == 1

	def setup(self, path_out, scale):
		assert self.audio_in != None
		assert type(scale) == int
		assert scale > 0

		if self.audio_out:
			self.audio_out.close()
		self.path_out = path_out
		self.audio_out = aifc.open(path_out, 'w')
		self.audio_out.aiff()
		self.scale = scale

		self.audio_out.setparams(self.audio_in.getparams())
		self.audio_out.setnframes(self.audio_in.getnframes()*self.scale)

	def __init__(self, path_in=None, path_out=None, scale=2):
		if scale:
			assert type(scale) == int
			assert scale > 0

		self.path_in = path_in
		self.path_out = path_out
		self.scale = scale
		self.audio_in = None
		self.audio_out = None
		if path_in:
			self.load(path_in)
		if path_out and scale:
			self.setup(path_out, scale)

	def __del__(self):
		self.close()

	def read(self, n):
		pos = self.audio_in.tell()
		for i in range(n):
			print(int.from_bytes(self.audio_in.readframes(1), byteorder='big', signed=True))
		self.audio_in.setpos(pos)

	def write(self):
		buf = self.audio_in.readframes(1)
		last = int.from_bytes(buf, byteorder='big', signed=True)
		cross = False

		for i in range(1, self.audio_in.getnframes()):
			temp_b = self.audio_in.readframes(1)
			temp_i = int.from_bytes(temp_b, byteorder='big', signed=True)
			print(temp_b)
			if temp_i != 0 and last != 0 and abs(temp_i)/temp_i != abs(last)/last:
				if cross:
					print('x')
					self.audio_out.writeframes(buf*self.scale)
					buf = b''
				cross = not cross
			buf += temp_b
			last = temp_i
		self.audio_out.writeframes(buf*self.scale)

	def close(self):
		if self.audio_in:
			self.audio_in.close()
		if self.audio_out:
			self.audio_out.close()

if __name__ == '__main__':
	x = doubler(path_in='../../Desktop/SKR4PZ.aiff', path_out='test.aiff')
	x.write()
	x.close()


