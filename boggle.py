#!/usr/bin/python


import sys, pygame, random
from pygame.locals import *

		
class Board:
	board = []

	def __init__(self):
		for i in range (0, 4):
			self.board.append([])
			for j in range (0, 4):
				self.board[i].append(Node(i, j, 'X'))
		return
				
	def printBoard(self):
		for i in range(0, 4):
			for j in range(0, 4):
				print (self.board[i][j].letter),
			print '\n'
		return
	
	def shuffle(self):
		spaces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		cubes = []
		cubes.append(['D', 'E', 'I', 'L', 'R', 'X'])
		cubes.append(['A', 'A', 'E', 'F', 'G', 'N'])
		cubes.append(['E', 'L', 'R', 'T', 'T', 'Y'])
		cubes.append(['A', 'O', 'O', 'T', 'T', 'W'])
		cubes.append(['A', 'B', 'B', 'J', 'O', 'O'])
		cubes.append(['E', 'H', 'R', 'T', 'V', 'W'])
		cubes.append(['C', 'I', 'M', 'O', 'T', 'V'])
		cubes.append(['D', 'I', 'S', 'T', 'T', 'Y'])
		cubes.append(['E', 'I', 'O', 'S', 'S', 'T'])
		cubes.append(['D', 'E', 'L', 'R', 'V', 'Y'])
		cubes.append(['A', 'C', 'H', 'O', 'P', 'S'])
		cubes.append(['H', 'I', 'M', 'N', 'Qu', 'E'])
		cubes.append(['E', 'E', 'I', 'N', 'S', 'U'])
		cubes.append(['E', 'E', 'G', 'H', 'N', 'W'])
		cubes.append(['A', 'F', 'F', 'K', 'P', 'S'])
		cubes.append(['H', 'L', 'N', 'N', 'R', 'Z'])
		
		for item in cubes:
			space = int(random.random() * 16)
			while spaces[space] != 0:
				space = int(random.random() * 16)
			spaces[space] = 1
			row = space / 4
			column = space % 4
			letter = int(random.random() * 6)
			self.board[row][column].letter = item[letter]
		return
	
class Node:
	def __init__(self, i, j, letter):
		self.i = i
		self.j = j
		self.letter = letter
		return
	isVisited = False
	
class Dictionary:
	tablesize = 60000
	words = []
	hashtable = {}
	prefixes = {}
	
	def readWords(self):
		with open('dict.txt') as f:
			content = f.readlines()
		for word in content:
			word = word.rstrip('\n')
			self.words.append(word)
		return
	
	def hashWords(self):
		for word in self.words:
			key = hash(word)
			self.hashtable[key] = word
			
			key2 = hash(word[0:3])
			self.prefixes[key2] = word
		return
	
	def lookup(self, word):
		key = hash(word)
		return key in self.hashtable

		
	def lookprefix(self, word):
		key = hash(word)
		return key in self.prefixes

class Solver:
	words = []
	d = Dictionary()
	b = Board()
	
	def __init__(self):		
		self.d.readWords()
		self.d.hashWords()		
		self.b.shuffle()
		self.b.printBoard()
		return
		
	def findWords(self, cube, word, visited):					
		word += cube.letter
		visited.append(word)
		
		if len(word) > 2:
			if self.d.lookup(word.lower()):
				self.words.append(word)
		
		if len(word) > 8:
			visited.pop()
			return
		
		if len(word) == 3:
			if not self.d.lookprefix(word.lower()):
				visited.pop()
				return
				
		i = cube.i
		j = cube.j
		
		if i + 1 < 4:
			self.findWords(self.b.board[i + 1][j], word, visited)
			if j + 1 < 4:
				self.findWords(self.b.board[i + 1][j + 1], word, visited)
			if j - 1 > 0:
				self.findWords(self.b.board[i + 1][j - 1], word, visited)
		if i - 1 > 0:
			self.findWords(self.b.board[i - 1][j], word, visited)
			if j + 1 < 4:
				self.findWords(self.b.board[i - 1][j + 1], word, visited)
			if j - 1 > 0:
				self.findWords(self.b.board[i - 1][j - 1], word, visited)
		if j + 1 < 4:
			self.findWords(self.b.board[i][j + 1], word, visited)
		if j - 1 > 0:
			self.findWords(self.b.board[i][j - 1], word, visited)
		visited.pop()
		return

s = Solver()
for row in range(0,4):
	for column in range(0,4):
				s.findWords(s.b.board[row][column], "", [])

print s.words


pygame.init()
fpsClock = pygame.time.Clock()
playerWords = []
playerWord = ""
timer = ""
time = 0
minutes = 0
seconds = 0
playing = True


windowSurfaceObj = pygame.display.set_mode((940, 940))

pygame.display.set_caption('Boggle')

catSurfaceObj = pygame.image.load('boggle.png')
redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 180, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
blackColor = pygame.Color(0, 0, 0)
mousex, mousey = 0,0

fontObj = pygame.font.SysFont('helvetica.ttf', 40)
font2 = pygame.font.SysFont('helvetica.tff', 85)
font3 = pygame.font.SysFont('helvetica.tff', 185)
msg = 'Hit \'Enter\' to start. Type words followed by \'Enter\' to submit!'

started = False
while True:
	windowSurfaceObj.fill(whiteColor)
	windowSurfaceObj.blit(catSurfaceObj, (400,160))
	
	
	xCoord = 908
	yCoord = 100
	for row in range(0,4):
		xCoord -= 440
		yCoord += 110
		for column in range(0,4):
			string = s.b.board[row][column].letter
			stringObj = font2.render(string, False, blueColor)
			stringRectobj = stringObj.get_rect()
			stringRectobj.topleft = (xCoord, yCoord)
			windowSurfaceObj.blit(stringObj, stringRectobj)
			xCoord += 110
	
	msgSurfaceObj = fontObj.render(msg, False, greenColor)
	msgRectobj = msgSurfaceObj.get_rect()
	msgRectobj.topleft = (10, 20)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	
	wordSurfaceObj = fontObj.render(playerWord, False, blackColor)
	wordRectobj = wordSurfaceObj.get_rect()
	wordRectobj.topleft = (60, 70)
	windowSurfaceObj.blit(wordSurfaceObj, wordRectobj)
	
	yCoord = 140
	
	for word in playerWords:
		listSurfaceObj = fontObj.render(word, False, blackColor)
		listRectobj = listSurfaceObj.get_rect()
		listRectobj.topleft = (30, yCoord)
		windowSurfaceObj.blit(listSurfaceObj, listRectobj)
		yCoord += 30

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEMOTION:
			mousex, mousey = event.pos
		elif event.type == MOUSEBUTTONUP:
			mousex, mousey = event.pos

		if event.type == KEYDOWN:
			started = True
			if event.key == K_RETURN:
				playerWords.append(playerWord)
				playerWord = ""
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
			if event.key == K_BACKSPACE:
				playerWord = playerWord[:-1]
			if event.key == K_a:
				playerWord += 'a'
			if event.key == K_b:
				playerWord += 'b'
			if event.key == K_c:
				playerWord += 'c'
			if event.key == K_d:
				playerWord += 'd'
			if event.key == K_e:
				playerWord += 'e'
			if event.key == K_f:
				playerWord += 'f'
			if event.key == K_g:
				playerWord += 'g'
			if event.key == K_h:
				playerWord += 'h'
			if event.key == K_i:
				playerWord += 'i'
			if event.key == K_j:
				playerWord += 'j'
			if event.key == K_k:
				playerWord += 'k'
			if event.key == K_l:
				playerWord += 'l'
			if event.key == K_m:
				playerWord += 'm'
			if event.key == K_n:
				playerWord += 'n'
			if event.key == K_o:
				playerWord += 'o'
			if event.key == K_p:
				playerWord += 'p'
			if event.key == K_q:
				playerWord += 'q'
			if event.key == K_r:
				playerWord += 'r'
			if event.key == K_s:
				playerWord += 's'
			if event.key == K_t:
				playerWord += 't'
			if event.key == K_u:
				playerWord += 'u'
			if event.key == K_v:
				playerWord += 'v'
			if event.key == K_w:
				playerWord += 'w'
			if event.key == K_x:
				playerWord += 'x'
			if event.key == K_y:
				playerWord += 'y'
			if event.key == K_z:
				playerWord += 'z'
	if started == False:				
		s.b.shuffle()
	else:
		time += fpsClock.get_time()
		if playing:
			seconds = time / 1000
			if seconds == 180:
				seconds = 0
				minutes = 3
				playing = False
			elif seconds >= 120:
				seconds -= 120
				minutes = 2
			elif seconds >= 60:
				seconds -= 60
				minutes = 1
			if seconds < 10:
				timer = str(minutes) +':0'+ str(seconds)	
			else:
				timer = str(minutes) +':'+ str(seconds)
		timerSurfaceObj = font3.render(timer, False, blackColor)
		timerRectobj = timerSurfaceObj.get_rect()
		timerRectobj.topleft = (520, 670)
		windowSurfaceObj.blit(timerSurfaceObj, timerRectobj)
		print timer


	pygame.display.update()
	fpsClock.tick(10)




