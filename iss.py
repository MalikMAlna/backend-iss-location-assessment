#!/usr/bin/env python
import sys
import requests as req
import turtle as trt
import time

__author__ = '''https://timestamp.online/article/
                how-to-convert-timestamp-to-datetime-in-python,
                Watched ISS Demo by Piero and Daniel'''

# if sys.version_info[0] < 3:
#     raise RuntimeError("This program requires Python 3+")


iss_icon = "iss.gif"
world_map = "map.gif"

base_url = "http://api.open-notify.org/"


def get_astronaut_info():
    """Returns Dict of Astronaut Names and Spacecraft"""
    r = req.get(base_url + "astros.json")
    r.raise_for_status()
    return r.json()["people"]


def get_iss_location():
    """Returns Current ISS (lat, lon) in float tuple"""
    r = req.get(base_url + "iss-now.json")
    r.raise_for_status()
    iss_pos = r.json()["iss_position"]
    lat = float(iss_pos["latitude"])
    lon = float(iss_pos["longitude"])
    return lat, lon


def draw_iss_map(lat, lon):
    """Draws World Map and Places ISS at (lon, lat) Location"""
    screen = trt.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_icon)
    iss = trt.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90)
    iss.penup()
    # Note the reverse below. That's normal. Don't change it.
    iss.goto(lon, lat)

    return screen


def compute_rise_time(lat, lon):
    """Returns the next horizon log time for specific lon, lat"""
    params = {"lat": lat, "lon": lon}
    r = req.get(base_url + "iss-pass.json", params=params)
    r.raise_for_status()
    passover_time = r.json()["response"][1]["risetime"]
    return time.ctime(passover_time)


def main(args):
    astro_dict = get_astronaut_info()
    print("\nCurrent people in spaaaaace: {}".format(len(astro_dict)))
    for astro in astro_dict:
        print("- {} in {}".format(astro["name"], astro["craft"]))

    lat, lon = get_iss_location()
    print("\nCurrent ISS coordinates: latitude: {:.02f}, longitude: {:.02f}"
          .format(lat, lon))

    screen = None
    try:
        screen = draw_iss_map(lat, lon)

        indy_lat = 39.768403
        indy_lon = -86.158068
        location_1 = trt.Turtle()
        location_1.penup()
        location_1.color("blue")
        location_1.goto(indy_lon, indy_lat)
        location_1.dot(5)
        location_1.hideturtle()
        next_pass_1 = compute_rise_time(indy_lat, indy_lon)
        location_1.write(next_pass_1, align="center",
                         font=("Arial", 10, "normal"))

        # Now, to compute the next passover time for my location in Jordan
        amman_lat = 31.963158
        amman_lon = 35.930359
        location_2 = trt.Turtle()
        location_2.penup()
        location_2.color("red")
        location_2.goto(amman_lon, amman_lat)
        location_2.dot(5)
        location_2.hideturtle()
        next_pass_2 = compute_rise_time(amman_lat, amman_lon)
        location_2.write(next_pass_2, align="center",
                         font=("Arial", 10, "normal"))

    except RuntimeError as e:
        print("ERROR: Problem loading graphics: " + str(e))

    if screen is not None:
        print("Click on screen to exit.")
        screen.exitonclick()


if __name__ == '__main__':
    main(sys.argv[1:])
