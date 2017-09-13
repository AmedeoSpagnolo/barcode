import sys
import math
import itertools

names = sys.argv[1:]

colors = ["#071c2c","#ff4c00","#792183","#a6228e","#cd242b","#f47920", "#faa61a"]

svg = ('<?xml version="1.0" encoding="utf-8"?>\n'
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"\n'
    'viewBox="0 0 {{width}} {{height}}" style="enable-background:new 0 0 {{width}} {{height}};" xml:space="preserve">{{content}}\n'
    '</svg>\n')

rect = '<rect x="{{x}}px" y="0px" fill="{{fill}}" width="{{width}}" height="{{height}}"/>\n'

def string_to_ascii(mystr):
    return [ord(x) for x in mystr]

def encrypt(arr, colours, spacing, h):
    # get an array of decimals (ascii converted)
    # and return a converted array
    rectWidth = [(math.sin(a)+1)*50 + 50 for a in arr]
    rectColor = [colours[a%len(colours)] for a in arr]
    rectShift = [sum(rectWidth[:a[0]]) + len(rectWidth[:a[0]]) * spacing for a in enumerate(rectWidth)]
    docWidth = sum(rectWidth) + (len(rectWidth) - 1) * spacing
    return [{
        "width": rectWidth[a[0]],
        "color": rectColor[a[0]],
        "shift": rectShift[a[0]],
        "height": h
    } for a in enumerate(arr)], docWidth

def generateSvg(obj, w, h):
    # generate rectangles
    content = [rect
        .replace("{{x}}", str(a["shift"]))
        .replace("{{fill}}", str(a["color"]))
        .replace("{{width}}", str(a["width"]))
        .replace("{{height}}", str(a["height"])) for a in obj]
    # generate svg
    mySvg = svg\
        .replace("{{content}}", ''.join(content))\
        .replace("{{height}}", str(h))\
        .replace("{{width}}", str(w))
    return mySvg

def write_new_file(file_name, content):
    with open(file_name, "w+") as out:
        out.write(content)

def exportArtboard(word, colours, docheight, spacing):
    obj, docwidth = encrypt(string_to_ascii(word), colours, spacing, docheight)
    content = generateSvg(obj, docwidth, docheight)
    filename = "export/" + word + ".svg"
    write_new_file(filename, content)
    print filename + " saved!!"

for name in names:
    for c in enumerate([list(itertools.permutations(colors))[71]]):
        for h in [220, 200]:
            for s in [30,40]:
                outfile =  name\
                    + "_c" + str(c[0])\
                    + "_h" + str(h)\
                    + "_s" + str(s)
                exportArtboard(outfile, c[1], h, s)
