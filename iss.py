#!/usr/bin/env python

import turtle
import requests
import time


__author__ = 'Randy Charity Jr'
def get_iss_info():
    position=[]
    x = requests.get('http://api.open-notify.org/astros.json').json()
    print(f'Number of Occupants: {x["number"]}')
    for i in x["people"]:
        print(f'Craft: {i["craft"]},',f'Name: {i["name"]}')
    y = requests.get('http://api.open-notify.org/iss-now.json').json()
    position.extend(y["iss_position"].values())
    print(y)

    return position

def get_passover_data():
    r = requests.get('http://api.open-notify.org/iss-pass.json?lat=39.7684&lon=86.1581').json()
    passover_time = r["response"][1]["risetime"]
    passover_data = f'Next Passover Indianpolis: {time.ctime(passover_time)}'
    print(passover_data)
    return(passover_data)


def turtle_graphic():
    lat,longitude = get_iss_info()
    indylat=float(39.791000)
    indylong=float(-86.148003)
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic('map.gif')
    screen.register_shape('iss.gif')
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(float(longitude),float(lat))
    curr = turtle.Turtle()
    curr.color('red')
    curr.penup()
    curr.goto(-170, -65)
    curr.hideturtle()
    curr.write('Current: '+str(longitude)+', '+str(lat))
    indypin = turtle.Turtle()
    indypin.penup()
    indypin.goto(indylong,indylat)
    indypin.color('yellow')
    indypin.dot(5)
    indypin.write(get_passover_data())
    screen.exitonclick()

def main():
    
    turtle_graphic()

if __name__ == '__main__':
    main()
