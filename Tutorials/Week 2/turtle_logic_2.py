import turtle
import math

def rectangle(width, height):
    distance = [width, height]
    for i in range(2):
        for j in range(2):
            turtle.forward(distance[j])
            turtle.left(90)
    turtle.exitonclick()

def rotated_rectangle(width, height, angle):
    turtle.right(angle)
    rectangle(width, height)

def polygon(radius, num_sides):
    side_length = radius * math.sin(math.pi / num_sides)
    print(360/num_sides)
    for i in range(0, num_sides):
        turtle.forward(side_length)
        turtle.left(360/num_sides)
    turtle.exitonclick()

def main():
    #rectangle(80, 40)

    #rotated_rectangle(80, 40, 30)

    polygon(50, 8)


if __name__ == "__main__" :
    main()
