import pygame

class textDispBox(pygame.sprite.Sprite):
	def __init__(self, rect : pygame.Rect, font : pygame.font.Font, defaultTxt : str, maxtTextLen) -> None:
		super().__init__()

		self.rect = rect
		self.font = font
		self.text = defaultTxt

		self.textMaxLen = maxtTextLen

	def addText(self, newTxt):
		self.text += newTxt

		if len(self.text) > self.textMaxLen:
			self.text = self.text[-self.textMaxLen:]

	# I took this from the pygame wiki and modified it
	# draw some text into an area of a surface
	# automatically wraps words
	# returns any text that didn't get blitted
	def update(self, window):

		pygame.draw.rect(window, (97, 97, 97), self.rect)

		text = self.text
		y = self.rect.top
		lineSpacing = -2

		# get the height of the font
		fontHeight = self.font.size("Tg")[1]

		while text:
			i = 1

			# determine if the row of text will be outside our area
			if y + fontHeight > self.rect.bottom:
				break

			# determine maximum width of line
			while self.font.size(text[:i])[0] < self.rect.width and i < len(text):
				i += 1

			# if we've wrapped the text, then adjust the wrap to the last word      
			if i < len(text): 
				i = text.rfind(" ", 0, i) + 1

			# render the line and blit it to the surface
			image = self.font.render(text[:i], True, (0, 0, 0))

			window.blit(image, (self.rect.left, y))
			y += fontHeight + lineSpacing

			# remove the text we just blitted
			text = text[i:]

		return text