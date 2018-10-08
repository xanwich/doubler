# doubler

import aifc

class doubler:
	def load(self, path_in, channel=1):
		if self.audio_in:
			self.audio_in.close()
		self.path_in = path_in
		self.audio_in = aifc.open(path_in, 'r')
		self.nchannels = self.audio_in.getnchannels()
		self.sampwidth = self.audio_in.getsampwidth()

		self.set_channel(channel)

		# print(self.nchannels, self.sampwidth)

	def setup(self, path_out, scale):
		assert self.audio_in != None
		self.set_scale

		if self.audio_out:
			self.audio_out.close()
		self.path_out = path_out
		self.audio_out = aifc.open(path_out, 'w')
		self.audio_out.aiff()
		self.scale = scale

		self.audio_out.setparams(self.audio_in.getparams())
		self.audio_out.setnframes(self.audio_in.getnframes()*self.scale)

	def set_scale(self, scale):
		assert type(scale) == int
		assert scale > 0
		self.scale = scale

	def set_channel(self, channel):
		assert type(channel) == int
		assert channel > 0
		self.channel = channel

	def __init__(self, path_in=None, path_out=None, scale=2, channel=1):
		self.path_in = path_in
		self.path_out = path_out
		self.scale = scale
		self.audio_in = None
		self.audio_out = None
		self.channel = None
		self.nchannels = None
		self.sampwidth = None
		if path_in:
			self.load(path_in, channel=channel)
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
		assert self.channel <= self.audio_in.getnchannels()

		index = self.sampwidth*(self.channel-1)
		buf = self.audio_in.readframes(1)
		last = int.from_bytes(buf[index:index+self.sampwidth], byteorder='big', signed=True)
		cross = False

		for i in range(1, self.audio_in.getnframes()):
			temp_b = self.audio_in.readframes(1)
			temp_i = int.from_bytes(temp_b[index:index+self.sampwidth], byteorder='big', signed=True)
			# print(temp_i)
			if temp_i != 0 and last != 0 and abs(temp_i)/temp_i != abs(last)/last:
				if cross:
					# print('x')
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

def main():
	import argparse
	parser = argparse.ArgumentParser(description='Scale AIFF files')
	parser.add_argument('input', action='store',
		help='path to input AIFF file')
	parser.add_argument('-o', '--output', action='store', default=None,
		help='path to output AIFF file. Default is [input]_x[scale].aiff')
	parser.add_argument('-s', '--scale', action='store', type=int, default=2,
		help='scale of output file. Scale=2 will produce output twice as long. Must be a positive integer')
	parser.add_argument('-c', '--channel', action='store', type=int, default=1,
		help='channel from which to determine waveforms to repeat')

	args = vars(parser.parse_args())
	if not args['output']:
		temp = args['input']
		if temp[-5:].lower() == '.aiff' or temp[-5:].lower() == '.aifc':
			temp = temp[:-5] + '_x{}.aiff'.format(args['scale'])
		elif temp[-4:].lower() == '.aif':
			temp = temp[:-4] + '_x{}.aiff'.format(args['scale'])
		else:
			temp += '_x{}.aiff'.format(args['scale'])
		args['output'] = temp

	worker = doubler(path_in=args['input'], path_out=args['output'], scale=args['scale'], channel=args['channel'])
	worker.write()
	worker.close()


if __name__ == '__main__':
	main()