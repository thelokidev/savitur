import support.constants as c
import support.general as gen
import os

# Chart dimensions to match South Indian chart layout (~486x327)
BASE_X = 43
BASE_Y = 10
W = 400
H = 320
CX = BASE_X + W // 2
CY = BASE_Y + H // 2
SCALE = min(W, H) / 280.0
STACK_DY = int(round(14 * SCALE))

def _house_positions():
    return [
        {"numX": CX, "numY": BASE_Y + int(round(20 * SCALE)), "planetX": CX, "planetY": BASE_Y + int(round(50 * SCALE)), "anchor": "middle"},
        {"numX": CX + int(round(60 * SCALE)), "numY": CY - int(round(50 * SCALE)), "planetX": CX + int(round(40 * SCALE)), "planetY": CY - int(round(30 * SCALE)), "anchor": "middle"},
        {"numX": BASE_X + W - int(round(20 * SCALE)), "numY": CY, "planetX": BASE_X + W - int(round(50 * SCALE)), "planetY": CY, "anchor": "middle"},
        {"numX": CX + int(round(60 * SCALE)), "numY": CY + int(round(50 * SCALE)), "planetX": CX + int(round(40 * SCALE)), "planetY": CY + int(round(30 * SCALE)), "anchor": "middle"},
        {"numX": CX, "numY": BASE_Y + H - int(round(20 * SCALE)), "planetX": CX, "planetY": BASE_Y + H - int(round(50 * SCALE)), "anchor": "middle"},
        {"numX": CX - int(round(60 * SCALE)), "numY": CY + int(round(50 * SCALE)), "planetX": CX - int(round(40 * SCALE)), "planetY": CY + int(round(30 * SCALE)), "anchor": "middle"},
        {"numX": BASE_X + int(round(20 * SCALE)), "numY": CY, "planetX": BASE_X + int(round(50 * SCALE)), "planetY": CY, "anchor": "middle"},
        {"numX": CX - int(round(60 * SCALE)), "numY": CY - int(round(50 * SCALE)), "planetX": CX - int(round(40 * SCALE)), "planetY": CY - int(round(30 * SCALE)), "anchor": "middle"},
        {"numX": BASE_X + int(round(30 * SCALE)), "numY": BASE_Y + int(round(50 * SCALE)), "planetX": BASE_X + int(round(50 * SCALE)), "planetY": BASE_Y + int(round(70 * SCALE)), "anchor": "start"},
        {"numX": BASE_X + W - int(round(30 * SCALE)), "numY": BASE_Y + int(round(50 * SCALE)), "planetX": BASE_X + W - int(round(50 * SCALE)), "planetY": BASE_Y + int(round(70 * SCALE)), "anchor": "end"},
        {"numX": BASE_X + W - int(round(30 * SCALE)), "numY": BASE_Y + H - int(round(30 * SCALE)), "planetX": BASE_X + W - int(round(50 * SCALE)), "planetY": BASE_Y + H - int(round(50 * SCALE)), "anchor": "end"},
        {"numX": BASE_X + int(round(30 * SCALE)), "numY": BASE_Y + H - int(round(30 * SCALE)), "planetX": BASE_X + int(round(50 * SCALE)), "planetY": BASE_Y + H - int(round(50 * SCALE)), "anchor": "start"},
    ]

############################################################################
################# Global Functions #########################################
############################################################################

def get_coordniates(housenum, planetidx):
    if planetidx in range(1, 9):
        pos = _house_positions()[housenum - 1]
        x_coordinate = int(pos["planetX"])
        y_coordinate = int(pos["planetY"] + STACK_DY * (planetidx - 1))
        return (x_coordinate, y_coordinate)
    print(f"INPUTERROR: planetidx must be in the range 1 to 8 but given value is {planetidx}.")
    return (0, 0)

def reset_chartcfg():
    chartcfg = {
                    "background-colour" : "black",
                    "outerbox-colour" : "red",
                    "line-colour" : "yellow",
                    "sign-colour" : "pink",
                    "house-colour" : {
                                        "tanbhav"      : "black",
                                        "dhanbhav"     : "black",
                                        "anujbhav"     : "black",
                                        "maatabhav"    : "black",
                                        "santanbhav"   : "black",
                                        "rogbhav"      : "black",
                                        "dampathyabhav": "black",
                                        "aayubhav"     : "black",
                                        "bhagyabhav"   : "black",
                                        "karmabhav"    : "black",
                                        "laabbhav"     : "black",
                                        "karchbhav"    : "black"
                                    },
                    "aspect-visibility"  : True
                }
    return(chartcfg)

def draw_classicNorthChartSkeleton(chartSVG, chartCfg):
    chartSVG.write(f'''  <rect width="486" height="327" x="0" y="7" style="fill:{chartCfg["background-colour"]};stroke-width:3;stroke:{chartCfg["outerbox-colour"]}" />\n''')
    chartSVG.write(f'''  <rect x="{BASE_X}" y="{BASE_Y}" width="{W}" height="{H}" fill="transparent" stroke="{chartCfg["line-colour"]}" stroke-width="2" />\n''')
    chartSVG.write(f'''  <line x1="{BASE_X}" y1="{BASE_Y}" x2="{BASE_X + W}" y2="{BASE_Y + H}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    chartSVG.write(f'''  <line x1="{BASE_X}" y1="{BASE_Y + H}" x2="{BASE_X + W}" y2="{BASE_Y}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    chartSVG.write(f'''  <line x1="{BASE_X}" y1="{CY}" x2="{CX}" y2="{BASE_Y}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    chartSVG.write(f'''  <line x1="{CX}" y1="{BASE_Y}" x2="{BASE_X + W}" y2="{CY}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    chartSVG.write(f'''  <line x1="{BASE_X + W}" y1="{CY}" x2="{CX}" y2="{BASE_Y + H}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    chartSVG.write(f'''  <line x1="{CX}" y1="{BASE_Y + H}" x2="{BASE_X}" y2="{CY}" stroke="{chartCfg["line-colour"]}" stroke-width="1.5" />\n''')
    return

def write_signnumOnChart_nsc(chartSVG, signclr, signnumlist):
    positions = _house_positions()
    for i in range(12):
        pos = positions[i]
        chartSVG.write(f'''  <text x="{pos["numX"]}" y="{pos["numY"]}" fill="{signclr}" class="sign-num" text-anchor="{pos["anchor"]}">{signnumlist[i]:02}</text>\n''')
    return

def write_planetsOnChart_nsc(chartSVG, planets):
    chartSVG.write('\n  <!-- ********** Planets ********** -->\n')
    for planetname in planets:
        symbol = planets[planetname]["symbol"]
        retro = planets[planetname]["retro"]
        planetcolour = planets[planetname]["colour"]
        #Get planet position co-ordinates x and y on chart svg
        px = planets[planetname]["pos"]["x"]
        py = planets[planetname]["pos"]["y"]

        #Since all needed properties are computed, Now create the svg entry string for planet
        if(retro == True):
            Planet_SVGstring = f'''  <text y="{py}" x="{px}" fill="{planetcolour}" text-decoration="underline" class="planet">({symbol})</text>\n'''
        else:
            Planet_SVGstring = f'''  <text y="{py}" x="{px}" fill="{planetcolour}" class="planet">{symbol}</text>\n'''
        #write the planet to SVG chart
        chartSVG.write(Planet_SVGstring)
    return

def write_planetsAspectsOnChart_nsc(chartSVG, planets):
    chartSVG.write('\n  <!-- ********** Planets Aspects ********** -->\n')
    
    for planetname in planets:
        chartSVG.write(f'\n  <!-- ********** {planetname} Aspect ********** -->\n')
        symbol = planets[planetname]["aspect_symbol"]
        planetcolour = planets[planetname]["colour"]
        for aspectpositions in planets[planetname]["aspectpos"]:
            #Get planet position co-ordinates x and y on chart svg
            px = aspectpositions["x"]
            py = aspectpositions["y"]

            #Since all needed properties are computed, Now create the svg entry string for planet
            Planet_SVGstring = f'''  <text y="{py}" x="{px}" fill="{planetcolour}" class="aspect">{symbol}</text>\n'''
            #write the planet to SVG chart
            chartSVG.write(Planet_SVGstring)
    return

def create_chartSVG(chartObj,location,chartSVGfilename):
    ''' Creates SVG image of astrology chart as per the chart draw configuration
        with data in division. The divisional chart is mentioned by division and 
        hence named accordingly'''
    # open or create chart file 
    if((location[-1] == '\\') or (location[-1] == '/')):
        chartSVGFullname = f'{location}{chartSVGfilename}.svg'
    elif('/' in location):
        chartSVGFullname = f'{location}/{chartSVGfilename}.svg'
    else:
        chartSVGFullname = f'{location}\{chartSVGfilename}.svg'
    
    chartSVG = open(chartSVGFullname, 'w',  encoding='utf-16')
    

    #Write the content into the file
    #SVG chart open section
    chartSVG.write(f'''<svg id="{chartObj.chartname}_chart_{chartObj.personname}" height="330" width="490" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 490 340" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" charset="utf-16">\n''')
    chartSVG.write('  <style>\n')
    chartSVG.write('    .sign-num { font: bold 22px sans-serif; }\n')
    chartSVG.write('    .planet { font: bold 20px sans-serif; }\n')
    chartSVG.write('    .aspect { font: bold 22px sans-serif; }\n')
    chartSVG.write('  </style>\n')
    chartSVG.write('  <!-- ********** Chart Diagram ********** -->\n')

    #create chart North indian style
    draw_classicNorthChartSkeleton(chartSVG, chartObj.chartcfg)    #Create skeleton
    write_signnumOnChart_nsc(chartSVG, chartObj.chartcfg["sign-colour"],chartObj.housesigns)    #Update the sign numbers on chart skeleton
    write_planetsOnChart_nsc(chartSVG, chartObj.planets)    #Update the planets on chart for every house
    if(chartObj.chartcfg["aspect-visibility"] == True):
        write_planetsAspectsOnChart_nsc(chartSVG, chartObj.planets)
    
    #SVG chart End section
    chartSVG.write('\n  Sorry, your browser does not support inline SVG.\n')
    chartSVG.write('</svg>\n')

    #close the file
    chartSVG.close()

    return "Success"

if __name__ == '__main__':
    pos = get_coordniates(c.KARCH, 8)
    print(pos)





