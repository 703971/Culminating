class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input #stores the text in function
		self.text = self.font.render(self.text_input, True, self.base_color) #uses text_input to create text in gui
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #creates rect for text-input #Rect objects to store and manipulate rectangular areas. A Rect can be created from a combination of left, top, width, and height values.
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect) #blits image to postion of the rect on screen
		screen.blit(self.text, self.text_rect) # blits text to postion of text rect on screen

	def checkForInput(self, position): # checks if the mouse positions are within the bounds of the button (in rage of the highest, lowest, farthest left and right corrdinates of the button)
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position): # changes color once postion of the mouse hovers over text 
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)