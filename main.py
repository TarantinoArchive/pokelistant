from PIL import Image, ImageDraw, ImageFont
import re
nome = ''
image = Image.open('teamlist.jpg') # Opening teamtlis image 
draw = ImageDraw.Draw(image) # Declaring 
font = ImageFont.truetype('Roboto.ttf', size=45) # Setting text font
black = 'rgb(0, 0, 0)' # Setting text color 
pok = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}}  # Declaring the matrix where user Pokémon will be stored
stat = []
val = []
stats = ["Atk", "Def", "SpAtk", "SpDef", "Spe"]
for i in range(6):
    for k in stats:
        pok[i][k] = '0'
print("Hi"+nome+"!"+" paste here yout teamtlis! \n")
tlis = []
while True: # Getting multiline input
    line = input()
    if line:
        # If line is IVs or Shiny it deletes it; it will ask later for modified IVs
        if line.find("Shiny:")>-1: 
            line = input()
            tlis.append(line)
        elif line.find("Level")>-1:
            line = input()
            tlis.append(line)
        elif line.find("IVs:")>-1:
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

# Setting Pokémon name, item and ability
for i in range(6):
    pok[i]["Name"] = tlis[i*8].split(' @ ')[0]
    pok[i]["Item"] = tlis[i*8].split(' @ ')[1]
    pok[i]['Ability'] = tlis[i*8+1].split('Ability: ')[1]
    
# Reading EVs
for i in range(6):
    stat.append(re.sub("[^A-Za-z ]", '', tlis[i*8+2])[5:])
for i in range(6):
    val.append(re.sub("[^0-9 ]",'',tlis[i*8+2])[1:])
for i in range(6):
    for k in range(6):
        pok[i][stat[i].split(' ')[k]] = val[i].split(' ')[k]

for i in range(6):
    pok[i]["Nature"] = tlis[i*8+3].split("Nature: ")[1]
    pok[i]["Move1"] = tlis[i*8+4].split("- ")[1]
    pok[i]["Move1"] = tlis[i*8+5].split("- ")[1]
    pok[i]["Move1"] = tlis[i*8+6].split("- ")[1]
    pok[i]["Move1"] = tlis[i*8+7].split("- ")[1]

#draw.text((x, y), message, fill=black, font=font)
image.save('prova.jpg')
