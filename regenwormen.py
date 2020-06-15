import random
def throwdice():
	options = ["1","2","3","4","5","r"]
	dice = random.choice(options)
	return dice

def multithrow(numberofdice):
	throwndice = []
	for i in range(numberofdice):
		die = throwdice()
		throwndice.append(die)
	return throwndice

def countpoints(list):
	totalpoints = 0
	for item in list:
		if item == "r":
			totalpoints += 5
		if item != "r":
			totalpoints += eval(item)
	return totalpoints

def eindscore(score,totalchosendice):
	if score < 21:
		print("Uw score is te laag, u bent af.")
		return 0
	if "r" not in totalchosendice:
		print("U heeft geen regenworm gegooid, u bent af.")
		return 0
	else:
		print("Uw eindscore is ", score)
		return score

def gameover(table, playerdict, player):
	uppertile = 0
	if len(playerdict[player]) > 0:
		uppertile = playerdict[player][-1]
		playerdict[player].remove(uppertile)
		table.append(uppertile)
		print(uppertile, " teruggelegd.")
		table = sorted(table)
	if(uppertile) != max(table):
		print(table[-1], " omgedraaid")
		table = table[:-1]
	return (table, playerdict, player)

###################################################################################

def onego(numberofdice,totalchosendice):
	chosendice = []
	throwndice = multithrow(numberofdice)
	print("U heeft dit gegooid: ", throwndice)
	gameover = 1
	for d in throwndice:
		if d not in totalchosendice:
			gameover = 0
	if gameover == 0:
		mychoice = input("Voer in welke dobbelstenenwaarde u wilt bewaren? (enter om te stoppen)")
		while mychoice not in throwndice or mychoice in totalchosendice:
			if mychoice not in throwndice:
				print("U heeft geen", mychoice, " gegooid\n")
			if mychoice in totalchosendice:
				print("U heeft al", mychoice, " gekozen\n")
			mychoice = input("Voer in welke dobbelstenenwaarde u wilt bewaren? (enter om te stoppen)")
		else:
			for die in throwndice:
				if die == mychoice:
					chosendice.append(die)
	else:
		print("U kunt geen dobbelsteen meer kiezen, u bent af.")
		return "gameover"
	return chosendice

def playturn(score,diceleft,totalchosendice):
	chosendice = onego(diceleft, totalchosendice)
	if chosendice == "gameover":
		return "gameover"
	else:
		score += countpoints(chosendice)
		diceleft = diceleft - len(chosendice)
		totalchosendice += chosendice
		print("U heeft dit gekozen: ", totalchosendice)
		print("Uw score is ", score, "\n")
		return (score, diceleft, totalchosendice)

def completeturn(table,playerdict,player):
	#start
	score = 0
	diceleft = 8
	totalchosendice = []
	chosendice = "-"
	available_opponent_dice = []
	for opponent in playerdict:
		if player != opponent:
			try:
				available_opponent_dice.append(playerdict[opponent][-1])
			except:
				pass

	if diceleft == 0:
		if score < 21:
			print("Uw score is te laag en u heeft geen dobbelstenen over, u bent af.")
			(table, playerdict, player) = gameover(table,playerdict,player)
		elif score > 34:
			print("Uw score is te hoog, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)
		elif "r" not in totalchosendice:
			print("U heeft geen regenworm gegooid en u heeft geen dobbelstenen over, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)

		elif score not in table and score not in available_opponent_dice:
			print("De gekozen tegel is niet beschikbaar, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)

		else:
			pass

	while diceleft != 0:
		if len(chosendice) == 0:
			print("Uw score is ", score, "\n")
		if chosendice != "":
			if score > 20 and "r" in totalchosendice and score in available_opponent_dice+table:
				play = "-"
				while play[0].lower() not in "jn":
					play = input("wilt u stoppen? (j/n)")
				if play[0].lower() == "n":
					try:
						(score, diceleft, totalchosendice) = playturn(score,diceleft,totalchosendice)
					except:
						diceleft = 0
				else:
					diceleft = 0
			else:
				if len(totalchosendice) != 0:
					print("U moet doorspelen")
				try:
					(score, diceleft, totalchosendice) = playturn(score,diceleft, totalchosendice)
				except:
					diceleft = 0

	if eindscore(score,totalchosendice) == 0:
		(table, playerdict, player) = gameover(table,playerdict,player)
	else:
		if eindscore(score,totalchosendice) in table:
			table.remove(score)
			playerdict[player].append(score)
		elif eindscore(score, totalchosendice) in available_opponent_dice:
			for opponent in playerdict:
				if opponent != player and eindscore(score, totalchosendice) == playerdict[opponent][-1]:
					playerdict[player].append(score)
					print(score, " toegevoegd aan stapel van", player)
					playerdict[opponent].remove(score)
					print(score, " weggehaald van stapel van", opponent)
		else:
			(table, playerdict, player) = gameover(table, playerdict, player)

	return (table, playerdict)

import itertools

def countscore(tileslist):
	scoredict = {21:1, 22:1,23:1,24:1,25:2,26:2,27:2,28:2,29:3,30:3,31:3,32:3,33:4,34:4,35:4,36:4}
	score = 0
	for item in tileslist:
		score += scoredict[item]
	return score

def masked(list):
	if len(list) > 0:
		visible = list[-1]
		maskedlist = ["X" for i in range(len(list) - 1)] + [visible]
		return maskedlist
	else:
		return []
def main():
	playerdict = {}
	table = [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
	#table = [21,22,23,24]
	name = "-"
	while name != "":
		name = input("Voer de namen in van de mensen die meedoen. ")
		if name != "":
			playerdict[name] = []
	while len(table) != 0:
		for player in itertools.cycle(playerdict.keys()):
			print(player.capitalize()+" is aan de beurt")
			(table, playerdict) = completeturn(table, playerdict, player)
			print(table)
			for player in playerdict:
				print(player,":",masked(playerdict[player]))

			if len(table) == 0:
				print("Het spel is ten einde.")
				winnaarpunten = -1
				winnaar = "-"

				for player in playerdict:
					if countscore(playerdict[player]) > winnaarpunten:
						winnaarpunten = countscore(playerdict[player])
						winnaar = player

				print(winnaar, " heeft gewonnen!!!")
				
				for player in playerdict:
					print(player,": ", countscore(playerdict[player]), "punten")
				break

main()

#TODO:
#tegel lager pakken als tegel niet beschikbaar is