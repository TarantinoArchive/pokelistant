from PIL import Image, ImageDraw, ImageFont
import re
import json
import math


def hpCalc(base, EVs, IVs):
    return int(((2*base+IVs+int(int(EVs)/4))*100)/100)+100+10


def statCalc(base, EVs, IVs, boost):
    return int(((((2*base+IVs+int(int(EVs)/4))*100)/100)+5)*boost)


def natureCalc(nature, stat):
    natures = {
        "Boosting": {
            "Atk": {
                "Lonely", "Adamant", "Naughty", "Brave"
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
                "Naughty", "Lax", "Rash", "Naive"
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
ivstats = ["HPIV","AtkIV", "DefIV", "SpAtkIV", "SpDefIV", "SpeIV"]
stats = ["HP","Atk", "Def", "SpAtk", "SpDef", "Spe"]
for i in range(6):
    for k in stats:
        pok[i][k] = '0'
    for k in ivstats:
        pok[i][k] = '31'
i=0
tlis, nome, tempIVs1, tempIVs2 = [], '', [], []
for opopo in range(6):
    tempIVs1.append('')
    tempIVs2.append('')
print("Hi"+nome+"!"+" paste here yout teamlist! \n")
while True:  # Getting multiline input
    line = input()
    if line:
        if line.find("Shiny:") > -1:
            line = input()
            tlis.append(line)
            i += 1
        elif line.find("Level") > -1:
            line = input()
            tlis.append(line)
            i += 1
        elif line.find("IVs:") > -1:
            templine = line.split("IVs: ")[1]
            tempIVs1.append(re.sub("[^A-Za-z ]", '',templine)[1:])
            tempIVs2.append(re.sub("[^0-9 ]",'', templine))
            for j in range(len(tempIVs1)):
                for k in range(len(tempIVs1[j].split(" "))-1): # non salva niente nell'array pok risolvere
                    actstat = tempIVs1[j].split(" ")[k]
                    actva = tempIVs2[j].split(" ")[k]
                    pok[int(i/8)][actstat+"IV"] = actva
            line = input()
            tlis.append(line)
            i += 1
        else:
            tlis.append(line)
            i += 1
    else:
        line = input()
        if line:
            tlis.append(line)
            i += 1
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
            pok[i][k] = hpCalc(pokemon[pok[i]["Name"].lower()]["PS"], pok[i][k], int(pok[i][k+"IV"]))
        else:
            pok[i][k] = statCalc(pokemon[pok[i]["Name"].lower()][k], pok[i][k], int(pok[i][k+"IV"]), natureCalc(pok[i]["Nature"],k))

for i in range(2):
    for k in range(3):
        if i==0:
            draw.text((245+i*825,390+k*492),pok[k]["Name"],black,font=font)
            draw.text((245+i*825,459+k*492),pok[k]["Nature"],black,font=font)
            draw.text((245+i*825,514+k*492),pok[k]["Ability"],black,font=font)
            draw.text((245+i*825,568+k*492),pok[k]["Item"],black,font=font)
            draw.text((245+i*825,623+k*492),pok[k]["Move1"],black,font=font)
            draw.text((245+i*825,677+k*492),pok[k]["Move2"],black,font=font)
            draw.text((245+i*825,731+k*492),pok[k]["Move3"],black,font=font)
            draw.text((245+i*825,784+k*492),pok[k]["Move4"],black,font=font)
            draw.text((650+i*825,459+k*492),"100",black,font=font)
            draw.text((650+i*825,514+k*492),str(pok[k]["HP"]),black,font=font)
            draw.text((650+i*825,568+k*492),str(pok[k]["Atk"]),black,font=font)
            draw.text((650+i*825, 623+k*492), str(pok[k]["Def"]), black, font=font)
            draw.text((650+i*825,677+k*492),str(pok[k]["SpAtk"]),black,font=font)
            draw.text((650+i*825,731+k*492),str(pok[k]["SpDef"]),black,font=font)
            draw.text((650+i*825,784+k*492),str(pok[k]["Spe"]),black,font=font)
        if i==1:
            draw.text((245+i*825,390+k*492),pok[k+3]["Name"],black,font=font)
            draw.text((245+i*825,459+k*492),pok[k+3]["Nature"],black,font=font)
            draw.text((245+i*825,514+k*492),pok[k+3]["Ability"],black,font=font)
            draw.text((245+i*825,568+k*492),pok[k+3]["Item"],black,font=font)
            draw.text((245+i*825,623+k*492),pok[k+3]["Move1"],black,font=font)
            draw.text((245+i*825,677+k*492),pok[k+3]["Move2"],black,font=font)
            draw.text((245+i*825,731+k*492),pok[k+3]["Move3"],black,font=font)
            draw.text((245+i*825,784+k*492),pok[k+3]["Move4"],black,font=font)
            draw.text((650+i*825, 459+k*492), "100", black, font=font)
            draw.text((650+i*825, 514+k*492), str(pok[k+3]["HP"]), black, font=font)
            draw.text((650+i*825, 568+k*492), str(pok[k+3]["Atk"]), black, font=font)
            draw.text((650+i*825, 623+k*492), str(pok[k+3]["Def"]), black, font=font)
            draw.text((650+i*825, 677+k*492),str(pok[k+3]["SpAtk"]), black, font=font)
            draw.text((650+i*825, 731+k*492),str(pok[k+3]["SpDef"]), black, font=font)
            draw.text((650+i*825, 784+k*492), str(pok[k+3]["Spe"]), black, font=font)
image.save('list.jpg')
