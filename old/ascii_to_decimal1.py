import sys
import math

names = sys.argv[1:]

colors = ["#071c2c","#ff4c00","#792183","#a6228e","#cd242b","#f47920", "#faa61a"]

docHeight = 200
docWidth = 0

svg = ('<?xml version="1.0" encoding="utf-8"?>\n'
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\n'
    'viewBox="0 0 {{width}} {{height}}" style="enable-background:new 0 0 {{width}} {{height}};" xml:space="preserve">{{content}}\n'
    '</svg>\n')

rect = '<rect x="{{x}}px" y="0px" fill="{{fill}}" width="{{width}}" height="{{height}}"/>\n'

def string_to_ascii(mystr):
    return [ord(x) for x in mystr]

def encrypt(arr):
    # get an array of decimals (ascii converted)
    # and return a converted array
    space = 70
    rectWidth = [(math.sin(a)+1)*50 + 50 for a in arr]
    rectColor = [colors[a%len(colors)] for a in arr]
    rectShift = [sum(rectWidth[:a[0]]) + len(rectWidth[:a[0]]) * space for a in enumerate(rectWidth)]
    global docWidth
    docWidth = sum(rectWidth) + (len(rectWidth) - 1) * space
    return [{
        "width": rectWidth[a[0]],
        "color": rectColor[a[0]],
        "shift": rectShift[a[0]],
        "height": docHeight
    } for a in enumerate(arr)]

def generateSvg(obj):
    # generate rectangles
    content = [rect
        .replace("{{x}}", str(a["shift"]))
        .replace("{{fill}}", str(a["color"]))
        .replace("{{width}}", str(a["width"]))
        .replace("{{height}}", str(a["height"])) for a in obj]
    # generate svg
    mySvg = svg\
        .replace("{{content}}", ''.join(content))\
        .replace("{{height}}", str(docHeight))\
        .replace("{{width}}", str(docWidth))
    return mySvg

def write_new_file(file_name, content):
    with open(file_name, "w+") as out:
        out.write(content)

for i, name in enumerate(names):
    dec = string_to_ascii(name)
    enc = encrypt(dec)
    content = generateSvg(enc)

    filename = "export/" + name + ".svg"
    write_new_file(filename, content)
    print filename + " saved!!"
