import pygame
from node import mkChain
from buttonhandle import button
from textDisplayBox import textDispBox

def main():
	pygame.init()

	pygame.display.set_caption("Markov Sentence Generator", "Brainrot Sim")

	gamefont = pygame.font.Font(r"c:\WINDOWS\Fonts\CONSOLA.TTF", 15)

	screen = pygame.display.set_mode((960, 720))
	running = True
	clock = pygame.time.Clock()
	
	mbu = False
	clickAndDrag = False
	addLink = False
	activeTextBox = None # Stupid work around for special case
	actionNodeId = 0
	prevMousePos = (0, 0)

	graphRunning = False
	framesSinceLastChange = 0

	graph = mkChain(gamefont)
	
	graph.addNode(0)
	maxNodeId = 0

	addNodeButton = button((20, 650, 50, 50), (210, 194, 191))
	playPauseButton = button((100, 650, 50, 50), (130, 42, 42))
	trashCanButton = button((180, 650, 50, 50), (28, 28, 28))

	mainTxtBox = textDispBox(pygame.Rect(635, 530, 325, 190), gamefont, "", 550)

	#-----setup stuff-----#

	while running:

		#-----mainloop-----#

		clock.tick(60)

		screen.fill((174, 174, 174))

		mouse = pygame.mouse.get_pos()

		#for every event, if that event is useful, do smthin
		for i in pygame.event.get():            
			match i.type:
				case pygame.QUIT:
					running = False
				case pygame.MOUSEBUTTONDOWN:
					hoveredNodes = graph.getNodesHovered(mouse)
					# Do not let this happen if addLink is true since it resets actionNodeId
					if len(hoveredNodes) and not addLink:
						clickAndDrag = True
						actionNodeId = hoveredNodes[0]
						prevMousePos = mouse
				case pygame.MOUSEBUTTONUP:
					mbu = True
					hoveredNodes = graph.getNodesHovered(mouse)
					hoveredTextInp = graph.getTextboxHovered(mouse)
					if len(hoveredNodes):
						if (graph.nodes[hoveredNodes[0]].linkAddClicked(mouse)):
							if not addLink:
								addLink = True
								actionNodeId = hoveredNodes[0]
							else:
								graph.nodes[actionNodeId].addLink(hoveredNodes[0])
								addLink = False
						else:
							graph.setActiveNode(hoveredNodes[0])

					elif addLink: # Stop the link adding process if user clicks off
						addLink = False

					if hoveredTextInp != None:
						# Special case for if the user clicks one box then another
						if activeTextBox != None and activeTextBox != hoveredTextInp:
							activeTextBox.active = False
						activeTextBox = hoveredTextInp
						hoveredTextInp.active = True
					elif activeTextBox != None: 
						activeTextBox.active = False

					clickAndDrag = False

				case pygame.KEYDOWN:
					graph.handleEventTextBoxes(i)

		if clickAndDrag:
			nodePos = graph.nodes[actionNodeId].position
			graph.moveNode(actionNodeId, ((nodePos[0] + (mouse[0] - prevMousePos[0])), (nodePos[1] + (mouse[1] - prevMousePos[1]))))
			prevMousePos = mouse

		if addLink:
			nodePos = graph.nodes[actionNodeId].position
			pygame.draw.line(screen, (0, 0, 0), (nodePos[0] + 37, nodePos[1]), mouse, width=2)

		# Update all our buttons
		if addNodeButton.update(screen, mouse, mbu):
			maxNodeId += 1
			graph.addNode(maxNodeId)
		if playPauseButton.update(screen, mouse, mbu):
			if playPauseButton.color == (130, 42, 42):
				playPauseButton.color = (42, 130, 48)
			else:
				playPauseButton.color = (130, 42, 42)

			graphRunning = not graphRunning
		if trashCanButton.update(screen, mouse, mbu):
			graph.deleteNode()

		# Half a second period before updating the graph
		if framesSinceLastChange == 30:
			framesSinceLastChange = 0
			if graphRunning:
				newText = graph.passActiveNode()
				mainTxtBox.addText(newText)

		mainTxtBox.update(screen)

		graph.update(screen, graph.nodes)
		framesSinceLastChange += 1

		mbu = False

		pygame.display.update()


	pygame.quit

if __name__ == "__main__":
	main()
	