from pygame import *
import requests, json, pickle, os
from getWeather import getWeather
from mapbox import Geocoder
screen = display.set_mode((340,700))
running = True
phone = screen.blit(transform.smoothscale(image.load('phone.png'),(330,680)),(5,10))
font.init()
avenirBold = font.Font('Avenir-Bold.ttf',48)
menuFont = font.Font('Avenir-Bold.ttf',24)
heightText = menuFont.render('sample',True,(0,255,0))
startPos = (27+5,80+10)
endPos = (306+5,600+10)
lat,long = (0,0)
##weather = requests.get('https://api.darksky.net/forecast/b8e5c750132fea6cfea17f7284b91e95/%s,%s' %(lat,long))
##weather = json.loads(weather.text)
weather = pickle.load(open('weather.pckl','rb'))
menuIcon = image.load('menu.png')
print(weather.keys())
menuMode = False
typing = False
request_exit = False
cities = {}
menuItems = ['Add Locations','Current Location']
mode = 'Current Location'
txt = ''
citiesDarkSky = {}
def renderWeather(weather):
    text = avenirBold.render('It is',True,(42,82,152))
    weatherEvent = avenirBold.render(str(round((weather['currently']['temperature']-32)*5/9,1))+'°C',True,(238,168,73))
    text2 = avenirBold.render('And',True,(42,82,152))
    weatherCond = weather['currently']['summary'].split()
    weatherWords = []
    for i in range(len(weatherCond)):
        screen.blit(avenirBold.render(weatherCond[i],True,(238,168,73)),(50,320+(3+i)*text.get_height()+5*(3+i)))
    screen.blit(text,(50,320))
    screen.blit(weatherEvent,(50,320+text.get_height()+5))
    screen.blit(text2,(50,320+text.get_height()+5+weatherEvent.get_height()+5))
while running:
    draw.rect(screen, (233,236,233), (startPos[0],startPos[1],endPos[0]-startPos[0],endPos[1]-startPos[1]),0)
    for e in event.get():
        if e.type == QUIT:
            running = False
        if typing:
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:
                    if len(txt) > 0:
                        txt = txt[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN:
                    request_exit = True
                elif e.key < 256:
                    txt += e.unicode
    menuItems = ['Add Locations','Current Location']+list(cities.keys())
    menu = screen.blit(menuIcon, (endPos[0]-70,90))
    m = mouse.get_pressed()
    mx,my = mouse.get_pos()
    if mode == 'Current Location':
        renderWeather(weather)
    if m[0] == 1 and menu.collidepoint(mx,my) or menuMode:
        menuMode = True
        menuSurf = Surface((endPos[0]-startPos[0]-30,endPos[1]-startPos[1]-30))
        menuSurf.set_alpha(160)
        menuSurf.fill((42,82,152))
        screen.blit(menuSurf,(startPos[0]+15,startPos[1]+15))
        obj = []
        for item in range(len(menuItems)):
            obj.append(screen.blit(menuFont.render(menuItems[item],True,(238,168,73)),(50,150+item*heightText.get_height()+20*item)))
        for o in obj:
            if m[0] == 1 and o.collidepoint(mx,my):
                mode = menuItems[obj.index(o)]
    if m[0] == 1 and not menu.collidepoint(mx,my) and menuMode:
        menuMode = False
    if mode not in menuItems[:2]:
        if citiesDarkSky[mode] == '':
            cityWeather = requests.get('https://api.darksky.net/forecast/b8e5c750132fea6cfea17f7284b91e95/%s,%s' %(cities[mode][0],cities[mode][1]))
            citiesDarkSky[mode] = json.loads(cityWeather.text)
        renderWeather(citiesDarkSky[mode])
    elif mode == 'Add Locations':
        geocoder = Geocoder(access_token='pk.eyJ1IjoieHVqYW1lczAwNyIsImEiOiJjamduc2R3Nmwwc3psMzBxc2dtMjI5aDZvIn0.1kHtKbs9h_rVW63x2RPf2w')
        dialog = Surface((endPos[0]-startPos[0]-30,40))
        dialog.set_alpha(160)
        dialog.fill((42,82,152))
        box = screen.blit(dialog,(startPos[0]+15,(endPos[1]+startPos[1])//2))
        size = 24
        inputFont = font.Font('Avenir-Bold.ttf',size)
        if m[0] == 1 and box.collidepoint((mx,my)) or typing:
            typing = True
        renderTXT = inputFont.render(txt,True,(255,255,255))
        screen.blit(renderTXT,(startPos[0]+18,(endPos[1]+startPos[1])//2+5))
        if m[0] == 1 and not box.collidepoint((mx,my)):
            typing = False
        if request_exit:
            response = geocoder.forward(txt,limit=3)
            first = response.geojson()['features'][0]
            long,lat = [round(coord,3) for coord in first['geometry']['coordinates']]
            cities[txt] = (lat,long)
            citiesDarkSky[txt] = ''
            txt = ''
            request_exit = False
    display.flip()
quit()
