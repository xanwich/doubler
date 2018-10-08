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
		if self.audio_in:
			self.audio_in.close()
		if self.audio_out:
			self.audio_out.close()

	def read(self, n):
		pos = self.audio_in.tell()
		print(self.audio_in.readframes(n))
		self.audio_in.setpos(pos)
