import random
from turtle import Screen,Turtle
import time

START = [(0,0),(-20,0),(-40,0)]
MOVE = 20
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.penup()
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.color('blue')
        self.speed('fastest')
        random_x = random.randint(-280,280)
        random_y = random.randint(-280, 280)
        self.goto(random_x,random_y)

    def ref(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)

class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score =0
        with open('data.txt')as data:
            self.high = int(data.read())

        self.high =0
        self.color('white')
        self.penup()
        self.goto(0,260)
        self.update()
        self.hideturtle()
    def update(self):
        self.clear()
        self.write(f"Score : {self.score} High score : {self.high}", align="center", font=('Courier', 24, 'normal'))

    def reset(self):
        if self.score> self.high:
            self.high = self.score
            with open('data.txt',mode='w') as data :
                data.write(f'{self.high}')
        self.score = 0
        self.update()

    def incr(self):
        self.score += 1
        self.update()

class Snake :
        def __init__(self):
            self.segment = []
            self.create_snake()
            self.head = self.segment[0]

        def create_snake(self):
            for position in START:
                self.add(position)

        def add(self,position):
            s_n = Turtle('square')
            s_n.color('White')
            s_n.penup()
            s_n.goto(position)
            self.segment.append(s_n)

        def resset(self):
            for seg in self.segment:
              seg.goto(1000,1000)
            self.segment.clear()
            self.create_snake()
            self.head = self.segment[0]

        def extend(self):
            self.add(self.segment[-1].position())


        def move (self):
            for seg_num in range(len(self.segment) - 1, 0, -1):
                new_x = self.segment[seg_num - 1].xcor()
                new_y = self.segment[seg_num - 1].ycor()
                self.segment[seg_num].goto(new_x, new_y)
            self.head.forward(MOVE)
        def up(self):
            if self.head.heading () != DOWN :
                self.head.setheading(UP)

        def down(self):
            if self.head.heading() != UP:
                self.head.setheading(DOWN)

        def left(self):
            if self.head.heading() != RIGHT:
                self.head.setheading(LEFT)

        def right(self):
            if self.head.heading() != LEFT:
                self.head.setheading(RIGHT)


screen = Screen()
screen.setup(width=600 , height=600)
screen.bgcolor('black')
screen.title("My Snake Game ")

screen.tracer(0)

snake = Snake()
food = Food()
screen.listen()
score = Score()
screen.onkey(snake.up,'Up')
screen.onkey(snake.down,'Down')
screen.onkey(snake.left,'Left')
screen.onkey(snake.right,'Right')
game = True

while game:
    screen.update()
    time.sleep(0.10)

    snake.move()

    if snake.head.distance(food) < 15:
        food.ref()
        snake.extend()
        score.incr()

    if (
    snake.head.xcor() > 280 or snake.head.xcor() < -280 or
    snake.head.ycor() > 280 or snake.head.ycor() < -280):
        score.reset()
        snake.resset()

    for seg in snake.segment:
        if seg == snake.head:
            pass
        elif snake.head.distance(seg) < 10 :
            score.reset()
            snake.resset()



screen.exitonclick()