

import ev3dev.ev3 as ev3
import math
import time
#import tkinter
#from tkinter import ttk
import library as robo

def main():
    following_mode()


def following_mode():
    print("--------------------------------------------")
    print(" Following ")
    print("--------------------------------------------")
    ev3.Sound.speak("I will follow you.").wait()
    print("Press the touch sensor to exit this program.") #CHANGE TO REMOTE

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 300
    x_values = [0, 0]
    direction = 0

    while not robot.touch_sensor.is_pressed:

        # DONE: 2. Read the Pixy values for x and y
        # Print the values for x and y
        print("value1: X", robot.pixy.value(1))
        pixy_x = robot.pixy.value(1)


        if robot.pixy.value(1) > 0:
            if robot.pixy.value(1) < 130: #130, 190
                robot.left(turn_speed, turn_speed)
            elif robot.pixy.value(1) > 190:
                robot.right(turn_speed, turn_speed)
            elif robot.pixy.value(1) >= 130 and robot.pixy.value(1) <= 190:
                robot.stop()
                time.sleep(.01)
                while robot.pixy.value(1) >= 130 and robot.pixy.value(1) <= 190:
                    robot.forward(600, 600)
                    time.sleep(.01)
                    del x_values[0]
                    x_values.append(pixy_x)
                    if x_values[1] > x_values[0]:
                        direction = 2  # right
                    if x_values[1] < x_values[0]:
                        direction = 1  # left
                    #you want it to keep oging while directin is true because when it starts circling it stores
                        # new values and that messes it up maybe. keep going as long as it is true because if see go straight

        else:
            # if x_values[1] > x_values[0]:
            #     while robot.pixy.value(1) < 0:
            #         robot.right(turn_speed, turn_speed)
            #         time.sleep(.5)
            # if x_values[1] < x_values[0]:
            #     while robot.pixy.value(1) < 0:
            #         robot.left(turn_speed, turn_speed)
            #         time.sleep(.5)
            if direction ==2:
                robot.right(turn_speed, turn_speed)
            if direction == 1:
                robot.left(turn_speed, turn_speed)
            else:
                robot.left(turn_speed, turn_speed)



        time.sleep(0.25)

    print("Cannot compute! Cannot compute! Human is too fast!")
    robot.stop()
    ev3.Sound.speak("Cannot compute! Cannot compute! Slow down human!").wait()


#---------------------
main()
