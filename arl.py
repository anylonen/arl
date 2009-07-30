#!/usr/bin/env python

"""
"""

import pyglet
import game
from game import player

# pyglet.options['debug_gl'] = False

pyglet.resource.path = ("data",)
pyglet.resource.reindex()

""" Set up a game window """
game_window = pyglet.window.Window(640, 480)

batch = pyglet.graphics.Batch()

""" List for game objects """
game_objects = []

player = player.Player(x=640/2, y = 480/2, batch = batch)

game_objects.append(player)

game_window.push_handlers(player)

""" Display for FPS """
clockDisplay = pyglet.clock.ClockDisplay()

@game_window.event
def on_draw():
    game_window.clear()
    batch.draw()
    clockDisplay.draw()

def update(dt):
	for obj in game_objects:
		obj.update(dt)
		

if __name__ == "__main__":
	# Game objects are updated 120 times per second
	pyglet.clock.schedule_interval(update, 1/120.0)
	
	pyglet.app.run()