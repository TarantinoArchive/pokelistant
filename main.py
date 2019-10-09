from PIL import Image, ImageDraw, ImageFont
import re
import json
import math


def hpCalc(base, EVs, IVs):
    return math.floor(((2*base+IVs+math.floor(int(EVs)/4))*100)/100)+100+10


def statCalc(base, EVs, IVs, boost):
    return math.floor((math.floor(((2*base+IVs+math.floor(int(EVs)/4))*100)/100)+5)*boost)


def natureCalc(nature, stat):
    natures = {
        "Boosting": {
            "Atk": {
                "Lonely", "Adamant", "Naugthy", "Brave"
            },
            "Def": {
                "Bold", "Impish", "Lash", "Relaxed"
            },
            "SpAtk": {
                "Modest", "Mild", "Rash", "Quiet"
            },
            "SpDef": {
                "Calm", "Gentle", "Careful", "Sassy"
            },
            "Spe": {
                "Timid", "Hasty", "Jolly", "Naive"
            }

        },
        "NotBoosting": {
            "Atk": {
                "Bold", "Modest", "Calm", "Timid"
            },            
            "Def": {
                "Lonely", "Mild", "Gentle", "Hasty"
            },
            "SpAtk": {
                "Adamant", "Impish", "Careful", "Jolly"
            },
            "SpDef": {
                "Naugthy", "Lax", "Rash", "Naive"
            },
            "Spe": {
                "Brave", "Relaxed", "Quiet", "Sassy"
            }
        }
    }
    if nature in natures["Boosting"][stat]: 
        return 1.1
    elif nature in natures["NotBoosting"][stat]:
        return 0.9
    else:
        return 1


json_file = open('pokemon.json')
pokemon = json.load(json_file)  # Opening pokemon.json as a JSON object

image = Image.open('teamlist.jpg')  # Opening teamtlis image
draw = ImageDraw.Draw(image)  # Declaring
font = ImageFont.truetype('Roboto.ttf', size=25)  # Setting text font
black = 'rgb(0, 0, 0)'  # Setting text color

pok = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}  # Declaring
stat = []
val = []
stats = ["HP","Atk", "Def", "SpAtk", "SpDef", "Spe"]
for i in range(6):
    for k in stats:
        pok[i][k] = '0'

tlis, nome = [], ''
print("Hi"+nome+"!"+" paste here yout teamlist! \n")
while True:  # Getting multiline input
    line = input()
    if line:
        if line.find("Shiny:") > -1:
            line = input()
            tlis.append(line)
        elif line.find("Level") > -1:
            line = input()
            tlis.append(line)
        elif line.find("IVs:") > -1:
            line = input()
            tlis.append(line)
            modIv = True
        else:
            tlis.append(line)
    else:
        line = input()
        if line:
            tlis.append(line)
        else:
            break

# Setting Pokémon information
for i in range(6):
    pok[i]["Name"] = tlis[i*8].split(' @ ')[0]
    pok[i]["Item"] = tlis[i*8].split(' @ ')[1]
    pok[i]['Ability'] = tlis[i*8+1].split('Ability: ')[1]
    pok[i]["Nature"] = tlis[i*8+3].split(" Nature")[0]
    pok[i]["Move1"] = tlis[i*8+4].split("- ")[1]
    pok[i]["Move2"] = tlis[i*8+5].split("- ")[1]
    pok[i]["Move3"] = tlis[i*8+6].split("- ")[1]
    pok[i]["Move4"] = tlis[i*8+7].split("- ")[1]
    pok[i]["Name"] = pok[i]["Name"].split('-')[0] # With this I exclude the alternative forms

# Reading EVs
for i in range(6):
    stat.append(re.sub("[^A-Za-z ]", '', tlis[i*8+2])[5:])
    val.append(re.sub("[^0-9 ]", '', tlis[i*8+2])[1:])
for i in range(6):
    for k in range(6):
        pok[i][stat[i].split(' ')[k]] = val[i].split(' ')[k]

# Calculating stats
for i in range(6):
    for k in stats:
        if k=="HP":
            pok[i][k] = hpCalc(pokemon[pok[i]["Name"].lower()]["PS"], pok[i][k], 31)
        else:
            pok[i][k] = statCalc(pokemon[pok[i]["Name"].lower()][k], pok[i][k], 31, natureCalc(pok[i]["Nature"],k))

for i in range(2):
    for k in range(3):
        if i==0:
            draw.text((245+i*825,390+k*492),pok[k]["Name"],black,font=font)
        if i==1:
            draw.text((245+i*825,390+k*492),pok[k+3]["Name"],black,font=font)
#245 390
#245 882
#1070
image.save('prova.jpg')
