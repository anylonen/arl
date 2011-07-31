"""
UI related stuff.
"""

class Panel(object):
    def __init__(self, x = 0, y = 0, width = 80, height = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.maximum_amount_of_messages = 5
        self.messages = []
        
    def add_message(self, message):
        if len(self.messages) >= self.maximum_amount_of_messages:
            self.messages.pop(0)
        self.messages.append(message)