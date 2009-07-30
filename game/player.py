import pyglet
from pyglet.window import key
 
class Player(pyglet.sprite.Sprite):
	"""Player class. At this point only moving around is supported. """
    
	def __init__(self, *args, **kwargs):
		self.player_image = pyglet.resource.image("player.png")
		self.player_image.anchor_x = self.player_image.width / 2
		self.player_image.anchor_y = self.player_image.height / 2
		
		super(Player, self).__init__(img=self.player_image, *args, **kwargs)
        
    	def on_key_press(self, symbol, modifiers):
		if symbol == key.UP:
			self.moveUp()
		elif symbol == key.RIGHT:
			self.moveRight()
		elif symbol == key.DOWN:
			self.moveDown()
		elif symbol == key.LEFT:
			self.moveLeft()
			
	def moveUp(self):
		self.y = self.y + 32
		self.check_bounds()
		pass

	def moveRight(self):
		self.x = self.x + 32
		self.check_bounds()
		pass

	def moveDown(self):
		self.y = self.y - 32
		self.check_bounds()
		pass

	def moveLeft(self):
		self.x = self.x - 32
		self.check_bounds()
		pass

	def check_bounds(self):
		""""""
		min_x = self.player_image.width/2
		min_y = self.player_image.height/2
		max_x = 640 - self.player_image.width/2
		max_y = 480 - self.player_image.height/2
		if self.x < min_x:
		    self.x = max_x
		elif self.x > max_x:
		    self.x = min_x
		if self.y < min_y:
		    self.y = max_y
		elif self.y > max_y:
		    self.y = min_y

	def update(self, dt):
		""" Update player """
		pass
 