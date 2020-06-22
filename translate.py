import re
import sys
import json

##	scoreList contains all the final score output, 


def inputsplit(inputstring):
	inputstring = re.sub(r'\s+', '', inputstring)							#Remove all whitespace
	if len(inputstring) == 24:
		inputList = [inputstring[i:i+2] for i in range(0, len(inputstring), 2)]
		return inputList, inputstring

	else:
		print("ERROR: Invalid Hex Input, expected 24 characters (12 Hexadecimals) while read characters is :", len(inputstring))
		sys.exit()


def buildSimpleScoreList(inputList,scoreList):
	scoreList[0] = hextodec(inputList[0])
	scoreList[1] = "30"
	scoreList[2] = buildSection(inputList[2])
	scoreList[3] = hextodec(inputList[3])
	scoreList[4] = hextodec(inputList[4])
	scoreList[5] = hextodec(inputList[5])
	scoreList[6] = hextodec(inputList[6])
	scoreList[7] = "00"
	scoreList[8] = "00"
	scoreList[9], scoreList[10], scoreList[11] = buildContract(inputList[9])
	scoreList[12], scoreList[13] = buildDeclarerResult(inputList[10])
	scoreList[14] = buildOpeningCard(inputList[11], scoreList[12])

	return scoreList


def writeSimpleScoreList(scoreList, inputstring):
	jsonList = {
	"hex input string": inputstring,
	"table number": scoreList[0],
	"default1": "30",
	"section": scoreList[2],
	"round number": scoreList[3],
	"board number": scoreList[4],
	"player pair E-W": scoreList[5],
	"player pair N-S": scoreList[6],
	"default2": "00",
	"default3": "00",
	"contract value": scoreList[9],
	"contract symbol": scoreList[10],
	"contract doubles": scoreList[11],
	"declarer": scoreList[12],
	"result": scoreList[13],
	"lead card": scoreList[14],
	}
	json_object = json.dumps(jsonList, indent = 4) 

	with open("bmlist1.json", "w") as outfile: 
		outfile.write(json_object) 


def buildOpeningCard(openingCardHex, declarer):
	openingCardDec = hextodec(openingCardHex)
	symbolModulo, updatedOpenCardDec = findOpenCardModulo(openingCardDec, declarer)
	openCardValue = findOpenCardValue(symbolModulo)
	openCardSymbol = findOpeningSymbol(updatedOpenCardDec)
	openingCardTotal = str(openCardValue) + openCardSymbol

	return openingCardTotal


def findOpenCardValue(symbolModulo):
	if symbolModulo not in (11, 12, 13, 14):
		openCardValue = symbolModulo
	elif symbolModulo == 14:
		openCardValue = "Ace of "
	elif symbolModulo == 13:
		openCardValue = "King of "
	elif symbolModulo == 12:
		openCardValue = "Queen of "
	elif symbolModulo == 11:
		openCardValue = "Jack of "

	return openCardValue


def findOpenCardModulo(openingCardDec, declarer):
	if declarer in ("N", "S"):
		updatedOpenCardDec = openingCardDec - 64
	else:
		updatedOpenCardDec = openingCardDec

	symbolModulo = openingCardDec % 16

	return symbolModulo, updatedOpenCardDec


def findOpeningSymbol(updatedOpenCardDec):
	if   updatedOpenCardDec < 15:
		symbolOpenCard = "C"
	elif updatedOpenCardDec < 32:
		symbolOpenCard = "D"
	elif updatedOpenCardDec < 47:
		symbolOpenCard = "H"
	elif updatedOpenCardDec < 65:
		symbolOpenCard = "S"
	else:
		symbolOpenCard = "Invalid Opening Card Hex"

	return symbolOpenCard


def buildDeclarerResult(declarerResultHex):
	declarerResultDec = hextodec(declarerResultHex)
	result, posneg = findResult(declarerResultHex)
	declarer = findDeclarer(declarerResultHex)
	totalResult = posneg + result

	return declarer, totalResult


def findResult(declarerResultHex):
	result = declarerResultHex[1]
	x = declarerResultHex[0]
	if result == "0":
		posneg = "="
	elif declarerResultHex[0] in ("0", "4", "8", "C"):
		posneg = "-"
	elif declarerResultHex[0] in ("1", "5", "9", "D"):
		posneg = "+"
	else:
		posneg = "Hex Declarer Invalid"

	return result, posneg


def findDeclarer(declarerResultHex):
	declarerResultDec = hextodec(declarerResultHex)

	if 0 < declarerResultDec < 25:
		declarer = "N"
	elif 64 < declarerResultDec < 89:
		declarer = "E"
	elif 128 < declarerResultDec < 153:
		declarer = "W"
	elif 192 < declarerResultDec < 217:
		declarer = "S"
	else:
		declarer = "Hex Declarer Invalid"

	return declarer


def buildSection(sectionHex):
	if   sectionHex == "00":
		return "A"
	elif sectionHex == "01":
		return "B"
	elif sectionHex == "02":
		return "C"
	elif sectionHex == "03":
		return "D"
	else:
		return "Nonexisting Section"


def buildContract(hexContract):
	contractDec = hextodec(hexContract)
	contractDoubles, contractDec = findContractDoubles(contractDec)
	contractSymbol, contractValue = findContractSymbol(contractDec)

	return contractValue, contractSymbol, contractDoubles


def findContractSymbol(contractDec):
	if contractDec < 8:
		contractValue = contractDec
		return "D", contractValue

	elif contractDec < 16:
		contractValue = contractDec - 8
		return "C", contractValue

	elif contractDec < 24:
		contractValue = contractDec - 16
		return "H", contractValue

	elif contractDec < 32:
		contractValue = contractDec - 24
		return "S", contractValue

	elif contractDec < 40:
		contractValue = contractDec - 32
		return "NT", contractValue


def findContractDoubles(contractDec):
	if contractDec < 64:
		contractDoubles = 0

	elif contractDec > 128:
		contractDoubles = 2
		contractDec = contractDec - 128

	elif contractDec > 64:
		contractDoubles = 1
		contractDec = contractDec - 64

	return contractDoubles, contractDec


def hextodec(hex):
	dec = int(hex, 16)

	return dec


def buildScore(hexInput):
	inputList, inputstring = inputsplit(hexInput)

	scoreList = [0] * 15
	buildSimpleScoreList(inputList, scoreList)
	writeSimpleScoreList(scoreList,hexInput)


	return scoreList


def inputLoop():
	while True:
		stringInput = input('Enter hex score string:')
		if stringInput == 'exit':
			break;
		print(buildScore(stringInput))


def main():
	inputLoop()

if __name__ == "__main__":
    main()