# guitar_strings
Generates and plays guitar strings in terminal. The string sounds are generated useing the Karplus-Strong Algorithm.

## Set-up
Clone this repo, go to this directory and install the necessary modules.
```
$ git clone https://github.com/SeanFitz1997/guitar_strings.git
$ cd guitar_strings
$ pip install -r requirements.txt
```

## Usage
Runnig this program with no arguments will generate the sound files for strings in the *notes* directory.
```
$ python strings.py
creating notes ...
creating ./notes/E2.wav ...
creating ./notes/A2.wav ...
creating ./notes/D3.wav ...
creating ./notes/G3.wav ...
creating ./notes/B3.wav ...
creating ./notes/E4.wav ...
```

To interactivly play strings add the *--play* flag.
```
$ python strings.py --play

Notes:
	'A' : E2
	'S' : A2
	'D' : D3
	'F' : G3
	'G' : B3
	'H' : E4

Press 'N' for notes
Press 'Q' to quit
```

To play random notes add the *--random* flag.
```
$ python strings.py --random
```

For help add the *--help* or *-h* help flags.
```
$ python strings.py -h
usage: strings.py [-h] [--random] [--play]

Generates and plays strings using the Karplus Strong Algorithm

optional arguments:
  -h, --help  show this help message and exit
  --random    Plays random notes until manual exit
  --play      Interactivly plays notes based on user input
```

# Demo
