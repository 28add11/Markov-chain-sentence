import pygame
import math
from random import random

from textInput import textInput

class link(pygame.sprite.Sprite):
	def __init__(self, node1 : int, node2 : int, probability : float, font : pygame.font.Font) -> None:
		super().__init__()
		self.node1 = node1
		self.node2 = node2

		self.probability = probability
		self.probabilityText = textInput(pygame.Rect(0, 0, 75, 30), font, (36, 36, 36), f"{probability:.2f}")

		self.previousProb = probability
	
	def update(self, window, nodesDict):

		# Previous probability stuff solves an issue with updating probability values when adding new links
		if self.probabilityText.text != f"{self.previousProb:.2f}" and not self.probabilityText.active:
			self.probability = float(self.probabilityText.text)
		
		# Don't mess up what the user is doing
		if not self.probabilityText.active:
			self.probabilityText.text = f"{self.probability:.2f}"

		self.previousProb = self.probability

		currentNode1 = nodesDict[self.node1]
		currentNode2 = nodesDict[self.node2]
		node1Position = (currentNode1.position[0] + 37, currentNode1.position[1])
		node2Position = (currentNode2.position[0] + 37, currentNode2.position[1])
		pygame.draw.line(window, (0, 0, 0), node1Position, node2Position, width=2)

		# Now we make an arrow just off the halfway point in the right direction
		angle = math.atan2(node2Position[1] - node1Position[1], node2Position[0] - node1Position[0])
		# Trig is to offset from center
		midpoint = ((node1Position[0] + node2Position[0] + math.cos(angle) * 20) / 2, (node1Position[1] + node2Position[1] + math.sin(angle) * 20) / 2)

		# Get 45 degree (pi/4 rad) lines, creating an arrow
		seg1Angle = angle + (math.pi / 4)
		seg2Angle = angle - (math.pi / 4)

		# Get coordinates of each individual segment
		seg1Coords = (midpoint[0] - math.cos(seg1Angle) * 12, midpoint[1] - math.sin(seg1Angle) * 12)
		seg2Coords = (midpoint[0] - math.cos(seg2Angle) * 12, midpoint[1] - math.sin(seg2Angle) * 12)

		pygame.draw.line(window, (0, 0, 0), midpoint, seg1Coords, width=2)
		pygame.draw.line(window, (0, 0, 0), midpoint, seg2Coords, width=2)

		# Add text, always updating position cuz im tired of working on this
		if math.cos(angle) < 0:
			self.probabilityText.moveBox((midpoint[0] - 75, midpoint[1]))
		else:
			self.probabilityText.moveBox((midpoint[0], midpoint[1]))
		self.probabilityText.update(window)

class node(pygame.sprite.Sprite):
	def __init__(self, position : tuple, font : pygame.font.Font, id : int) -> None:
		super().__init__()
		self.position = position
		self.font = font
		self.id = id

		self.active = False

		self.links = []
		# Text box class automatically self-centers so we just give it our whole rect
		self.text = textInput(pygame.Rect(self.position[0], self.position[1], 75, 30), font, (143, 143, 143), "test")
	
	def update(self, window : pygame.display, nodesDict) -> None:
		# Just for drawing, all other functions are for actual stuff

		for i in self.links:
			i.update(window, nodesDict)
		
		if pygame.Rect(self.position[0] - 15, self.position[1], 105, 30).collidepoint(pygame.mouse.get_pos()) or self.active:
			pygame.draw.rect(window, (138, 88, 0), (self.position[0], self.position[1], 75, 30))
			pygame.draw.circle(window, (138, 88, 0), (self.position[0], self.position[1] + 15), 15)
			pygame.draw.circle(window, (138, 88, 0), (self.position[0] + 75, self.position[1] + 15), 15)
		else:
			pygame.draw.rect(window, (110, 110, 110), (self.position[0], self.position[1], 75, 30))
			pygame.draw.circle(window, (110, 110, 110), (self.position[0], self.position[1] + 15), 15)
			pygame.draw.circle(window, (110, 110, 110), (self.position[0] + 75, self.position[1] + 15), 15)

		pygame.draw.rect(window, (237, 237, 237), (self.position[0] + 1, self.position[1] + 3, 74, 24))
		pygame.draw.circle(window, (237, 237, 237), (self.position[0] + 1, self.position[1] + 15), 12)
		pygame.draw.circle(window, (237, 237, 237), (self.position[0] + 74, self.position[1] + 15), 12)

		pygame.draw.circle(window, (138, 88, 0), (self.position[0] + 37.5, self.position[1]), 7)
		pygame.draw.circle(window, (237, 237, 237), (self.position[0] + 37.5, self.position[1]), 4)

		self.text.update(window)

	def linkAddClicked(self, mouse) -> bool:
		return pygame.Rect(self.position[0] + 30.5, self.position[1] - 7, 14, 14).collidepoint(mouse)
	
	def addLink(self, linkedNode : int) -> None:
		for i in self.links:
			if linkedNode == i.node2:
				return

		# Calculate a new equal probability for each link
		newLinkValue = 1 / (len(self.links) + 1) 
		for i in self.links:
			i.probability = newLinkValue
		self.links.append(link(self.id, linkedNode, newLinkValue, self.font))

	def textEventHandler(self, event : pygame.event.Event):
		# Literally just to avoid an awful function call and member chain
		self.text.handleTextEvent(event)


class mkChain(pygame.sprite.Group):
	# Class for managing the whole graph so we can actually make stuff happen in a nice order
	def __init__(self, font) -> None:
		super().__init__()
		self.nodes = {}

		self.font = font

	def getNodesHovered(self, mousePos : tuple) -> list:
		colidedNodes = []
		for i in self.nodes.values():
			bodyHitbox = pygame.Rect(i.position[0] - 15, i.position[1], 105, 30).collidepoint(mousePos)
			addLinkHitbox = pygame.Rect(i.position[0] + 30.5, i.position[1] - 7, 14, 14).collidepoint(mousePos)
			# Since part of the addLink button is outside of the main body we need additional logic for it
			if bodyHitbox or addLinkHitbox:
				colidedNodes.append(i.id)
		return colidedNodes
	
	def getTextboxHovered(self, mousePos : tuple) -> textInput:
		for i in self.nodes.values():
			if i.text.rect.collidepoint(mousePos):
				return i.text
			
			for j in i.links:
				if j.probabilityText.rect.collidepoint(mousePos):
					return j.probabilityText

	def deactivateTextInp(self):
		for i in self.nodes.values():
			i.text.active = False
			
			for j in i.links:
				j.probabilityText.active = False
	
	def handleEventTextBoxes(self, event : pygame.event.Event):
		for i in self.nodes.values():
			i.text.handleTextEvent(event)

			for j in i.links:
				j.probabilityText.handleTextEvent(event)
	
	def moveNode(self, nodeId : int, newPos : tuple) -> None:
		# Cursed line
		self.nodes[nodeId].text.moveBox(newPos)
		self.nodes[nodeId].position = newPos

	def addNode(self, nodeId : int):
		if nodeId not in self.nodes:
			self.nodes[nodeId] = node((480, 360), self.font, nodeId)
			self.add(self.nodes[nodeId])

	def deleteNode(self):
		activeNode = None
		for i in self.nodes.values():
			if i.active:
				activeNode = i.id
				break
		
		if activeNode != None:
			deletedNode = self.nodes.pop(activeNode)

			# This loop is so awful
			for i in self.nodes.values():
				for j in i.links:
					if deletedNode.id == j.node2:
						i.links.remove(j)
			self.remove(deletedNode)

	def setActiveNode(self, nodeId : int):
		for i in self.nodes.values():
			i.active = False
		self.nodes[nodeId].active = True

	def passActiveNode(self) -> str:
		# Find active node, loop because having a whole bunch of logic for which node was active was a pain in the ass
		for i in self.nodes.values():
			if i.active:
				activeNode = i.id
				break
		
		linkList = self.nodes[activeNode].links
		cumSum = 0

		randomVal = random()

		if len(linkList) == 0:
			nextNode = activeNode

		for i in linkList:
			cumSum += i.probability
			if randomVal <= cumSum:
				nextNode = i.node2
				break

		self.nodes[activeNode].active = False
		self.nodes[nextNode].active = True

		# Return the actual value of new text added
		return self.nodes[nextNode].text.text + " "
