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
	if score < 21:
		print("Uw score is te laag, u bent af.")
		return 0
	if "r" not in totalchosendices:
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
	available_opponent_dices = []
	for opponent in playerdict:
		if player != opponent:
			try:
				available_opponent_dices.append(playerdict[opponent][-1])
			except:
				pass

	if dicesleft == 0:
		if score < 21:
			print("Uw score is te laag en u heeft geen dobbelstenen over, u bent af.")
			(table, playerdict, player) = gameover(table,playerdict,player)
		elif score > 34:
			print("Uw score is te hoog, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)
		elif "r" not in totalchosendices:
			print("U heeft geen regenworm gegooid en u heeft geen dobbelstenen over, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)

		elif score not in table and score not in available_opponent_dices:
			print("De gekozen tegel is niet beschikbaar, u bent af.")
			(table, playerdict, player) = gameover(table, playerdict, player)

		else:
			pass

	while dicesleft != 0:
		if len(chosendices) == 0:
			print("Uw score is ", score, "\n")
		if chosendices != "":
			if score > 20 and "r" in totalchosendices and score in available_opponent_dices+table:
				play = "-"
				while play[0].lower() not in "jn":
					play = input("wilt u stoppen? (j/n)")
				if play[0].lower() == "n":
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
		(table, playerdict, player) = gameover(table,playerdict,player)
	else:
		if eindscore(score,totalchosendices) in table:
			table.remove(score)
			playerdict[player].append(score)
		elif eindscore(score, totalchosendices) in available_opponent_dices:
			for opponent in playerdict:
				if opponent != player and eindscore(score, totalchosendices) == playerdict[opponent][-1]:
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