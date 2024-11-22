import pygame

class textInput(pygame.sprite.Sprite):
	def __init__(self, rect : pygame.Rect, font : pygame.font.Font, txtColor : tuple, defaultTxt : str) -> None:
		super().__init__()

		self.rect = rect
		self.font = font
		self.txtColor = txtColor
		self.text = defaultTxt

		self.active = False

	def update(self, window : pygame.display):
		# Change text color to signify activity
		if self.active:
			text = self.font.render(self.text, True, (138, 88, 0))
		else:
			text = self.font.render(self.text, True, self.txtColor)
		txtSize = text.get_size()
		window.blit(text, (self.rect.left + (self.rect.width / 2) - (txtSize[0] / 2), self.rect.top + (self.rect.height / 2) - (txtSize[1] / 2)))

	def handleTextEvent(self, event : pygame.event.Event):
		if self.active:
			if event.key == pygame.K_RETURN:
				self.active = False  # Finish after pressing enter
			elif event.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]  # Remove the last character
			else:
				self.text += event.unicode

	def moveBox(self, newPos : tuple):
		self.rect = pygame.Rect(newPos[0], newPos[1], self.rect.width, self.rect.height)