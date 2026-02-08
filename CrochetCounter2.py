import json
import re

def saveData():
    with open (saveFile, "w") as f:
        json.dump(data, f, indent=4)

def countStitches(round):
    stitchSum = 0
    for i in pattern[round]:
        stitchSum += i[1]
    return stitchSum

def printNextStitch():
    curStitch = data['Stitch']
    stitchIndex = 0

    while curStitch > 0:
        if curStitch >= pattern[data["Round"]-1][stitchIndex][1]:
            curStitch -= pattern[data["Round"]-1][stitchIndex][1]
            stitchIndex += 1
        else:
            break
    
    print("Next Stitch(es): ", pattern[data["Round"]-1][stitchIndex][0], pattern[data["Round"]-1][stitchIndex][1] - curStitch)

saveFile = "CounterSaved2.json"
patternFile = "Pattern2.txt"
pattern = []
data = {}

#Compile patternFile into a readable format
with open(patternFile, "r") as f:

    temp = f.read()
    round_re = re.compile(
        r"""
        R(?P<start>\d+)          # starting round number
        (?:-(?P<end>\d+))?       # optional range (R4-5)
        :                        # colon
        \s*
        (?P<currentRound>[A-Z\s\d()]+) # the instructions
        """,
        re.VERBOSE
    )

    lines = temp.splitlines()

    for l in lines:
        stp = round_re.search(l)

        curR = []
        temp = []

        for e in stp.group("currentRound").split():
            try:
                num = int(e)
                if len(temp) > 1:
                    temp2 = []
                    for x in temp:
                        temp2.append([x,1])
                    curR = (temp2*num)
                    temp = []
                else:
                    curR.append([temp[0], num])
                    temp = []
            except:
                temp.append(e)

        try:
            for _ in range(int(stp.group("start")),int(stp.group("end")) + 1):
                pattern.append(curR)
        except:
            pattern.append(curR)
        


#Open saveFile
with open(saveFile, "r") as f:
    data = json.load(f)

totalStitchesInRound = countStitches(data["Round"]-1)

#Crochet loop

while True:
    printNextStitch()

    userIn = input()

    if userIn.lower() == "reset":
        data["Stitch"] = 0
        data["Round"] = 1
        totalStitchesInRound = countStitches(data["Round"]-1)

    elif userIn.lower() == "":
        data["Stitch"] += 1
        if data["Stitch"] >= totalStitchesInRound:
            data["Stitch"] = 0
            data["Round"] += 1
            if data["Round"]-1 >= len(pattern):
                print("Pattern Finished!!!")
                break
            totalStitchesInRound = countStitches(data["Round"]-1)
            print("New round started")

    elif userIn == "-":
        data["Stitch"] -= 1
        if data["Stitch"] < 0:
            data["Round"] -= 1
            if data["Round"] <= 0:
                print("\n Went too far back you muppet \n")
                data["Round"] += 1
                data["Stitch"] += 1
                break
            data["Stitch"] = countStitches(data["Round"]-1) - 1
            totalStitchesInRound = countStitches(data["Round"]-1)
        
    elif userIn.lower() == "end":
        break
    else:
        print("\nInvalid input: Press enter for the next stitch and '-' to go back.\n Type 'Reset' to fully reset the pattern progress.\n")
    saveData()