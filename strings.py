#Imports===================================================
import sys, os, time, random, wave, argparse, pygame
import numpy as np
from collections import deque
from readchar import readchar

# show plot of algorith in action
gShowPlot = False

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
		self.notes[fileName] = pygame.mixer.Sound(
			'./notes/' + fileName + '.wav')

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

	# initalise samples buffer
	samples = np.array([0] * nSamples, 'float32')

	for i in range(nSamples):
		samples[i] = buf[0]
		avg = 0.996 * 0.5 * (buf[0] + buf[1])
		buf.append(avg)
		buf.popleft()
		
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
	
	parser = argparse.ArgumentParser(
		description='Generates and plays strings using the '\
		'Karplus Strong Algorithm')
	parser.add_argument('--random', action='store_true', required=False,
		help='Plays random notes until manual exit')	
	parser.add_argument('--play', action='store_true', required=False,
		help='Interactivly plays notes based on user input')
	args = parser.parse_args()

	# create note player
	nplayer = NotePlayer()
	
	Notes = {'E2' : 82.41, 'A2' : 110, 'D3' : 146.8, 
	'G3' : 196, 'B3' : 246.9, 'E4' : 329.6}

	print('creating notes ...')
	for name, freq in list(Notes.items()):
		fileName = './notes/' + name + '.wav'
		if not os.path.exists(fileName):
			data = generateNote(freq)
			print('creating ' + fileName + ' ...')
			writeWAVE(fileName, data)
		else:
			print(fileName + ' already created (skipped)')

		# add note to player
		nplayer.addNote(name)

	# play random tone
	if args.random:
	
		print("Playing random notes. (Press 'Ctl-C' to exit)") 
		while True:
			try:
				nplayer.playRandom()
				time.sleep(0.5)
			except KeyboardInterrupt:
				exit()
	# interactivly play notes
	elif args.play:
	
		# key : file_name
		keyBindings = {
			'a' : 'E2',
			's' : 'A2',
			'd' : 'D3',
			'f' : 'G3',
			'g' : 'B3',
			'h' : 'E4'
		}
		#help string
		ctl_str = "\nNotes:\n\t'A' : E2\n\t'S' : A2\n\t'D' : D3\n\t"\
			"'F' : G3\n\t'G' : B3\n\t'H' : E4\n" \
			"\nPress 'N' for notes\nPress 'Q' to quit\n"

		print(ctl_str)
		while True:
			key = readchar().decode("utf-8")
			if key == 'q':
				exit()
			if key == 'n':
				print(ctl_str)
			if key in keyBindings.keys():
				print(keyBindings[key])
				nplayer.play(keyBindings[key])
			
if __name__ == '__main__':
	main()
