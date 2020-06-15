import random
def throwdice():
	options = ["1","2","3","4","5","r"]
	dice = random.choice(options)
	return dice

def multithrow(numberofdices):
	throwndices = []
	for i in range(numberofdices):
		dice = throwdice()
		throwndices.append(dice)
	return throwndices

def countpoints(list):
	totalpoints = 0
	for item in list:
		if item == "r":
			totalpoints += 5
		if item != "r":
			totalpoints += eval(item)
	return totalpoints

def eindscore(score,totalchosendices):
	#HIER OOK DE OGEN VAN DE WORP ZODAT JE KUNT VERGELIJKEN OF JE ALLEEN MAAR DINGEN HEBT GEGOOID DIE JE AL GEKOZEN HEBT
	if score < 21:
		print("Uw score is te laag, u bent af.")
		return 0
	if "r" not in totalchosendices:
		print("U heeft geen regenworm gegooid, u bent af.")
		return 0
	else:
		print("Uw eindscore is ", score)
		return score
###################################################################################

def onego(numberofdices,totalchosendices):
	chosendices = []
	throwndices = multithrow(numberofdices)
	print("U heeft dit gegooid: ", throwndices)
	gameover = 1
	for d in throwndices:
		if d not in totalchosendices:
			gameover = 0
	if gameover == 0:
		mychoice = input("Voer in welke dobbelstenenwaarde u wilt bewaren? (enter om te stoppen)")
		while mychoice not in throwndices or mychoice in totalchosendices:
			if mychoice not in throwndices:
				print("U heeft geen", mychoice, " gegooid\n")
			if mychoice in totalchosendices:
				print("U heeft al", mychoice, " gekozen\n")
			mychoice = input("Voer in welke dobbelstenenwaarde u wilt bewaren? (enter om te stoppen)")
		else:
			for dice in throwndices:
				if dice == mychoice:
					chosendices.append(dice)
	else:
		print("U kunt geen dobbelsteen meer kiezen, u bent af.")
		return "gameover"
	return chosendices

def playturn(score,dicesleft,totalchosendices):
	chosendices = onego(dicesleft, totalchosendices)
	if chosendices == "gameover":
		return "gameover"
	else:
		score += countpoints(chosendices)
		dicesleft = dicesleft - len(chosendices)
		totalchosendices += chosendices
		print("U heeft dit gekozen: ", totalchosendices)
		print("Uw score is ", score, "\n")
		return (score, dicesleft, totalchosendices)

def completeturn(table,playerdict,player):
	#start
	score = 0
	dicesleft = 8
	totalchosendices = []
	chosendices = "-"
	if dicesleft == 0:
		if score < 21:
			print("Uw score is te laag en u heeft geen dobbelstenen over, u bent af.")
			return "gameover"
		elif score > 34:
			print("Uw score is te hoog, u bent af.")
		elif "r" not in totalchosendices:
			print("U heeft geen regenworm gegooid en u heeft geen dobbelstenen over, u bent af.")
			return "gameover"
		else:
			printeindscore(score, totalchosendices)

	while dicesleft != 0: # and mychoice != "": MAAR HIER NIET BESCHIKBAAR
		if len(chosendices) == 0:
			print("Uw score is ", score, "\n")
		if chosendices != "":
			if score > 20 and "r" in totalchosendices:
				play = input("wilt u nog spelen? (j/n)")
				if play == "j":
					try:
						(score, dicesleft, totalchosendices) = playturn(score,dicesleft,totalchosendices)
					except:
						dicesleft = 0
				else:
					dicesleft = 0
			else:
				if len(totalchosendices) != 0:
					print("U moet doorspelen")
				try:
					(score, dicesleft, totalchosendices) = playturn(score,dicesleft, totalchosendices)
				except:
					dicesleft = 0

	if eindscore(score,totalchosendices) == 0:
		playerdict[player] = playerdict[player][:-1]
		table = table[:-1]
	else:
		if eindscore(score,totalchosendices) in table:
			table.remove(score)
			playerdict[player].append(score)
		else:
			for opponent in playerdict:
				if opponent != player and len(playerdict[opponent]) > 1:
					if eindscore(score, totalchosendices) == playerdict[player][-1]:
						playerdict[player].append(score)
						playerdict[opponent].remove(score)

	return (table, playerdict)

import itertools

def main():
	playerdict = {}
	table = [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
	name = "-"
	while name != "":
		name = input("Voer de namen in van de mensen die meedoen. ")
		if name != "":
			playerdict[name] = []
	while len(table) != 0:
		for player in itertools.cycle(playerdict.keys()):
			print(player.capitalize()+" is aan de beurt")
			(table, playerdict) = completeturn(table, playerdict, player)
			print(table,playerdict)


main()

#MAAK VAN MAIN COMPLETETURN DIE EINDSCORE RETURNT EN MAAK NIEUWE MAIN DIE EERST VRAAGT HOEVEEL SPELEERS ER ZIJN, ZOVEEL LIJSTEN IN EEN DICTIONARY INITIALISEERT EN 1 LIJST (TABLE)
#AVAILABLE_TILES = (FOR USER IN DICT: DICT[USER][-1]) + (TABLE)
#IF EINDSCORE IN AVAILABLE_TILES: WIL JE DIE PAKKEN?, YES -> WEGHALEN UIT LIJST EN TOEVOEGEN AAN LIJST VAN PERSOON, IF LEN(TABLE) == 0: GAME FINISHED
#MAAK COUNTPOINTS MODULE MET DICHT DIE VOOR IEDERE TEGEL T AANTAL WORMEN BEVAT









