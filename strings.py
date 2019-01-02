#Imports===================================================
import sys, os, time, random, wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
from readchar import readchar

# show plot of algorith in action
gShowPlot = False

# note of a Pentatonic Minor Scale
# piano C4, E(b), F, G, C5
pmNotes = {'C4' : 262, 'Eb' : 311, 'F' : 349, 'G' : 391, 'Bb' : 446}

#Classes===================================================
''' Used to play WAV files generated '''
class NotePlayer:
	def __init__(self):
		pygame.mixer.pre_init(44100, -16, 1, 2048)
		pygame.mixer.init()
		pygame.init()
		# dict of notes
		self.notes = {}

	def addNote(self, fileName):
		self.notes[fileName] = pygame.mixer.Sound(fileName)

	def play(self, fileName):
		try:
			self.notes[fileName].play()
		except:
			print(fileName + ' not found')

	def playRandom(self):
		index = random.randint(0, len(self.notes) - 1)
		note = list(self.notes.keys())[index]
		self.notes[note].play()

#Fuctions==================================================
''' Generate note of a given frequency '''
def generateNote(freq):
	nSamples = 44100
	sampleRate = 44100
	N = int(sampleRate / freq)
	
	# initalise ring buffer
	buf = deque([random.random() - 0.5 for i in range(N)])

	# plot of flag set 
	if gShowPlot:
		fig = plt.figure()
		ax = fig.add_subplot(111)
		axline, = ax.plot(buf)
		plt.show(block=False)
 
	# initalise samples buffer
	samples = np.array([0] * nSamples, 'float32')

	for i in range(nSamples):
		samples[i] = buf[0]
		avg = 0.996 * 0.5 * (buf[0] + buf[1])
		buf.append(avg)
		buf.popleft()
		
		# plot of flag set 
		if gShowPlot:
			if i % 1000 == 0:
				axline.set_ydata(buf)
				fig.canvas.draw()

	# convert samples to 16-bit values and then to sting
	# (max val for 16-bit int is 32767)
	samples = np.array(samples * 32767, 'int16')
	return samples.tostring()

''' Writes sound data to WAV file '''
def writeWAVE(fname, data):
	file = wave.open(fname, 'wb')
	# WAV file parameters
	nChannels = 1
	sampleWidth = 2
	frameRate = 44100
	nFrames = 44100
	# set params
	file.setparams((nChannels, sampleWidth, frameRate, nFrames, 
		'NONE', 'noncompressed'))
	file.writeframes(data)
	file.close()

#Program===================================================
def main():
	#declare global var
	global gShowPlot
	
	parser = argparse.ArgumentParser(
		description='Generating sounds with the Karplus Strong Algorithm')
	parser.add_argument('--display', action='store_true', required=False,
		help='Plots note waves')
	parser.add_argument('--random', action='store_true', required=False,
		help='Plays random notes until manually exited')	
	parser.add_argument('--play', action='store_true', required=False,
		help='Interactivly plays notes based on user input')
	args = parser.parse_args()

	# plot flag set
	if args.display:
		gShowPlot = True
		plt.ion()

	# create note player
	nplayer = NotePlayer()
	
	print('creating notes ...')
	for name, freq in list(pmNotes.items()):
		fileName = name + '.wav'
		if not os.path.exists(fileName) or args.display:
			data = generateNote(freq)
			print('creating ' + fileName + ' ...')
			writeWAVE(fileName, data)
		else:
			print('fileName already created (skipped)')

		# add note to player
		nplayer.addNote(name + '.wav')

		# if display set
		if args.display:
			nplayer.play(name + '.wav')
			time.sleep(0.5)

	# play random tone
	if args.random:
	
		print('Playing random notes. (Press ctrl-C to exit)') 
		try:
			while True:
				nplayer.playRandom()
				time.sleep(0.5)
		except KeyboardInterrupt:
			exit()

	# interactivly play notes
	elif args.play:
	
		# key : file_name
		keyBindings = {
			'a' : 'C4.wav',
			's' : 'Eb.wav',
			'd' : 'F.wav',
			'f' : 'G.wav',
			'g' : 'Bb.wav',
		}
		#help string
		ctl_str = "\nNotes:\n\t'A' : C4\n\t'S' : E(b)\n\t'D' : F\n\t"\
			"'F' : G\n\t'G' : B(b)\n\nPress 'H' for help\n"\
			"Press 'Q' to quit\n"


		print(ctl_str)
		while True:
			key = readchar().decode("utf-8")
			if key == 'q':
				exit()
			if key == 'h':
				print(ctl_str)
			if key in keyBindings.keys():
				print(keyBindings[key])
				nplayer.play(keyBindings[key])
			

if __name__ == '__main__':
	main()
