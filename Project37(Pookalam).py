import turtle
import math

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
turtle.bgcolor("white")
turtle.title("Perfect Digital Pookalam")

def draw_petal(radius, angle, color):
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.circle(radius, angle)
        t.left(180 - angle)
    t.end_fill()

def petal_ring(radius, petals, petal_radius, angle, color):
    step = 360 / petals
    for i in range(petals):
        t.penup()
        t.setheading(step*i)
        t.forward(radius)
        t.pendown()
        draw_petal(petal_radius, angle, color)
        t.penup()
        t.home()

def leaf_ring(radius, count):
    leaf_colors = ["darkgreen", "green", "lime"]
    step = 360 / count
    for i in range(count):
        t.penup()
        t.setheading(step*i)
        t.forward(radius)
        t.pendown()
        for lc in leaf_colors:
            t.color(lc)
            t.begin_fill()
            for j in range(3):
                t.forward(40)
                t.left(120)
            t.end_fill()
            t.left(120)
        t.penup()
        t.home()

def center_layers(radii, colors):
    for r,c in zip(radii, colors):
        t.penup()
        t.goto(0,-r)
        t.pendown()
        t.color(c)
        t.begin_fill()
        t.circle(r)
        t.end_fill()

leaf_ring(250, 36)

petal_ring(200, 36, 80, 60, "orange")
petal_ring(200, 36, 60, 60, "yellow")

petal_ring(140, 18, 50, 60, "darkred")
petal_ring(100, 12, 40, 60, "orange")
petal_ring(70, 8, 30, 60, "yellow")

center_layers([60, 45, 30, 15], ["gold", "orange", "red", "yellow"])

petal_ring(20, 6, 15, 60, "orange")

turtle.done()
