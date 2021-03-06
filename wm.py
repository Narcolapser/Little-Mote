import cwiid
import time
import uinput

class WiiMote (object):

	def __init__(self,addr=None):
		#save the wiimote address for later reference
		self.addr = addr
		
		#connect to the wiimote
		self.mote = None
		while self.mote is None:
			try:
				self.mote = cwiid.Wiimote()
			except RuntimeError as e:
				print "failed to connect to wiimote."
		
		#for debugging, turn 1 LED on. 
		self.mote.led = 1
		self.ledNum = 1
		
		#prepare the callback list:
		self.calls = {
			'2':None,
			'1':None,
			'b':None,
			'a':None,
			'minus':None,
			'home':None,
			'left':None,
			'right':None,
			'down':None,
			'up':None,
			'plus':None
			}
		
		#prep the reactor variable.
		self.react = False
		
		#turn on the wiimote's reporting for buttons
		self.mote.rpt_mode = cwiid.RPT_BTN
		
		#initialize the mouse controller
		self.mouse = uinput.Device([
			uinput.BTN_LEFT,
			uinput.BTN_RIGHT,
			uinput.REL_X,
			uinput.REL_Y
			])
		
		self.lstate = 0
		self.rstate = 0
		
	def start(self):
		'''
		Start the reactor loop that listens for WiiMote events so the appropriate call back
		can be called.
		'''
		self.react = True
		while self.react:
			time.sleep(0.01)
			bstate = self.mote.state['buttons']
			if bstate % 2 and self.calls['2'] is not None:
				self.calls['2'](wm)
			if bstate / 2 % 2 and self.calls['1'] is not None:
				self.calls['1'](wm)
#			if bstate / 4 % 2 and self.calls['b'] is not None:
#				self.calls['b'](wm)
#			if bstate / 8 % 2 and self.calls['a'] is not None:
#				self.calls['a'](wm)
			if bstate / 16 % 2 and self.calls['minus'] is not None:
				self.calls['minus']()
			if bstate / 128 % 2 and self.calls['home'] is not None:
				self.calls['home']()
			if bstate / 256 % 2 and self.calls['left'] is not None:
				self.calls['left']()
			if bstate / 512 % 2 and self.calls['right'] is not None:
				self.calls['right']()
			if bstate / 1024 % 2 and self.calls['down'] is not None:
				self.calls['down']()
			if bstate / 2048 % 2 and self.calls['up'] is not None:
				self.calls['up']()
			if bstate / 4096 % 2 and self.calls['plus'] is not None:
				self.calls['plus']()
			leftClick(wm)
			rightClick(wm)
		
	def stop(self):
		'''
		stops the reactor loop.
		'''
		
		pass
	
	def release(self):
		'''
		releases the wiimote, which should effectively turn it off.
		'''
		pass

def testOut():
	print wm.mote.state['buttons']

def callmeMaybe():
	print "I was called!"

def countUp():
	wm.ledNum = (wm.ledNum + 0.1) % 16
	if wm.ledNum < 1:
		wm.ledNum = 1
	wm.mote.led = int(wm.ledNum)

def countDown():
	wm.ledNum = (wm.ledNum - 0.1) % 16
	if wm.ledNum < 1:
		wm.ledNum = 16
	wm.mote.led = int(wm.ledNum)

def mousetickDown():
	mousetick(0,int(wm.ledNum))
def mousetickUp():
	mousetick(0,int(-1*wm.ledNum))
def mousetickLeft():
	mousetick(int(-1*wm.ledNum),0)
def mousetickRight():
	mousetick(int(wm.ledNum),0)

def mousetick(x,y):
	wm.mouse.emit(uinput.REL_X,x)
	wm.mouse.emit(uinput.REL_Y,y)

def leftClick(wm):
	state = wm.mote.state['buttons'] / 8 % 2
	if state != wm.lstate:
		wm.mouse.emit(uinput.BTN_LEFT,state)
#		wm.mouse.emit(uinput.BTN_LEFT,1)
	wm.lstate = state

def rightClick(wm):
	wm.mouse.emit(uinput.BTN_LEFT,0)

if __name__ == "__main__":
	wm = WiiMote()
	wm.calls['2'] = testOut
	wm.calls['1'] = testOut
	wm.calls['b'] = leftClick
	wm.calls['a'] = rightClick
	wm.calls['minus'] = countDown
	wm.calls['home'] = callmeMaybe
	wm.calls['left'] = mousetickLeft
	wm.calls['right'] = mousetickRight
	wm.calls['down'] = mousetickDown
	wm.calls['up'] = mousetickUp
	wm.calls['plus'] = countUp
	wm.start()

