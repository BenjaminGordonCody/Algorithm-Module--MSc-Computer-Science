"""
This program uses the Turtle module to draw a series of heptagons.

Whilst coding I made the assumption that I might want Tegan the turtle 
to draw other shapes and colours at some point in the future. The "initial 
variables" at the top of the file may be altered to facilitate regular polygons
of any variety.
"""

# imports
import turtle

# initial variables
angles = 7
color = "grey"


def draw_regular_polygon(tegan, angles):

    angle = float(360/angles)
    tegan.begin_fill()
    for i in range(angles):
        tegan.forward(50)  # This value determines length of sides.
        tegan.left(angle)
    tegan.end_fill()
    tegan.penup()
    tegan.forward(150)  # This value determines space between polygons.
    tegan.pendown()


def get_turtle(color):

    tegan = turtle.Turtle()
    tegan.pencolor(color)
    tegan.fillcolor(color)
    return tegan


def main():

    try:
        user_input = int(input("How many septagons shall I draw?"))
    except:
        print("Usage: Input an integer value.")
        return 1

    # initialise turtle object
    tegan = get_turtle(color)

    for i in range(user_input):
        draw_regular_polygon(tegan, angles)


main()
