"""
Jessica Myers
CSSE120 Robot Final Project
'Follow Me'
8 November 2017
"""

import ev3dev.ev3 as ev3
import math
import time
import tkinter
from tkinter import ttk
import library as robo
import mqtt_remote_method_calls as com

global break_check

def main():
    print("Running...")

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    #robot = robo.Snatch3r()

    # root = tkinter.Tk()
    # root.title("MQTT Remote")
    #
    # main_frame = ttk.Frame(root, padding=20, relief='raised')
    # main_frame.grid()
    #
    # left_speed_label = ttk.Label(main_frame, text="Left")
    # left_speed_label.grid(row=0, column=0)
    # left_speed_entry = ttk.Entry(main_frame, width=8)
    # left_speed_entry.insert(0, "600")
    # left_speed_entry.grid(row=1, column=0)
    #
    # forward_button = ttk.Button(main_frame, text="Forward")
    # forward_button.grid(row=2, column=1)
    # # forward_button and '<Up>' key is done for your here...
    # forward_button['command'] = lambda: forward(mqtt_client, left_speed_entry, right_speed_entry)
    # root.bind('<Up>', lambda event: forward(mqtt_client, left_speed_entry, right_speed_entry))


    # ------------------------------------------------------------------------------------------------------
    # REMOTE CONTROL -- button for follow me mode, stop following me mode, status? say something mode
    # ------------------------------------------------------------------------------------------------------
    # class DataContainer(object):
    #     """ Helper class that might be useful to communicate between different callbacks."""
    #
    #     def __init__(self):
    #         self.running = True
    #
    # print("--------------------------------------------")
    # print("IR Remote")
    # print(" - Use IR remote channel 1.")
    # print(" - Press red up to start following")
    # print(" - Press red down to STOP following")
    # print(" - Press blue up for dog to bark")
    # print("--------------------------------------------")
    #
    # ev3.Leds.all_off()  # Turn the leds off
    # robot = robo.Snatch3r()
    # dc = DataContainer()
    # left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    # right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
    # assert left_motor.connected
    # assert right_motor.connected
    #
    # rc1 = ev3.RemoteControl(channel=1)
    # rc1.on_red_up = lambda state: follow_me(state, robot)  # FOllow me
    # rc1.on_red_down = lambda state: stop_following(state, robot)  # Stop following me
    # rc1.on_blue_up = lambda state: bark(state, robot)  # Say something
    #
    # btn = ev3.Button()
    # btn.on_backspace = lambda state: handle_shutdown(state, dc)
    #
    # while dc.running:
    #     # Process the RemoteControl objects.
    #     rc1.process()
    #     btn.process()
    #     time.sleep(0.01)
    #
    # robot.shutdown = lambda state: handle_shutdown(dc)


#def interface():
    #------------------------------------------------------------------------------------------------------
    # TKinter Interface GUI ## To mirror the REMOTE
    #------------------------------------------------------------------------------------------------------
    root = tkinter.Tk()
    root.minsize(width=300, height=400)

    frame = ttk.Frame(root, padding=10)
    frame.grid(row=1, column=1)

    root.grid_columnconfigure(0, minsize=100)
    root.grid_columnconfigure(2, minsize=100)
    root.grid_rowconfigure(0, minsize=100)
    root.grid_rowconfigure(2, minsize=100)

    root.configure(bg="turquoise")

    title_label = ttk.Label(root, text="Robo-Dog", font=("Helvetica", 30))
    title_label.grid(row=0, column=1)

    description_label = ttk.Label(root, text="Meet Robo-Dog, the most on-demand, interactive dog you will"
                                             " ever play with!", font=("Helvetica", 15))
    description_label.grid(row=2, column=1)

    fine_print = ttk.Label(root, text="Jessica Myers", font=("Helvetica", 10))
    fine_print.grid(row=5, column=1)

    fine_print2 = ttk.Label(root, text="Robo-Dog Inc.", font=("Helvetica", 10))
    fine_print2.grid(row=6, column=1)

    intro_button = ttk.Button(frame, text="Introduction")
    intro_button.grid(row=0, column=1)
    intro_button['command'] = lambda: intro(mqtt_client)

    button1 = ttk.Button(frame, text="Follow Me!")
    button1.grid(row=1, column=1)
    button1['command'] = lambda: follow_me(mqtt_client)

    button2 = ttk.Button(frame, text="Pet Me!")
    button2.grid(row=2, column=1)
    button2['command'] = lambda: pet_me(mqtt_client)

    q_button = ttk.Button(frame, text="Quit")
    q_button.grid(row=3, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(frame, text="Exit")
    e_button.grid(row=4, column=1)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    #
    # new = ttk.Button(frame, text="New")
    # new.grid(row=5, column=1)
    # new['command'] = (lambda: follow_me_2(mqtt_client, robot, root, frame))
    #
    # extra = ttk.Button(frame, text="STOP NOW")
    # extra.grid(row=5, column=1)
    # extra['command'] = (lambda: check(mqtt_client))

    #
    # button2 = ttk.Button(frame, text="Go, enter name..")
    # button2.grid(row=0, column=0)
    # button1['command'] = lambda: SOMECOMMAND()

    # def forward(mqtt_client, left_speed_entry, right_speed_entry):
    #     left_speed = int(left_speed_entry.get())
    #     right_speed = int(right_speed_entry.get())
    #     mqtt_client.send_message("forward", [left_speed, right_speed])
    #
    root.mainloop()


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def follow_me(mqtt_client):
    mqtt_client.send_message("old_following_mode")


def pet_me(mqtt_client):
    mqtt_client.send_message("petting_mode")

def intro(mqtt_client):
    mqtt_client.send_message("introduce")

# def follow_me_2(mqtt_client, robot, root, frame):
#     print("--------------------------------------------")
#     print(" Following ")
#     print("--------------------------------------------")
#     ev3.Sound.speak("I will follow you.").wait()
#     print("Press the touch sensor to exit this program.")  # CHANGE TO REMOTE
#
#     robot.pixy.mode = "SIG1"
#     turn_speed = 300
#     x_values = [0, 0]
#     direction = 0
#
#     status = False
#
#     while not robot.touch_sensor.is_pressed:
#         robot.following_mode(turn_speed, x_values, direction)
#         status = check_state()
#         if status == True:
#             break
#     print("I will stop following you.")
#     robot.stop()
#     ev3.Sound.speak("I will stop following you.").wait()
#
# def check(mqtt_client):
#     break_check == True
#
# def check_state():
#     return break_check
#------------------------------------------------------------------------------------------------------
# Pixy Following Mode
#------------------------------------------------------------------------------------------------------

def following_mode():
    print("--------------------------------------------")
    print(" Following ")
    print("--------------------------------------------")
    ev3.Sound.speak("I will follow you.").wait()
    print("Press the touch sensor to exit this program.")  # CHANGE TO REMOTE

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 300
    x_values = [0, 0]
    direction = 0

    while not robot.keep_going:          #not robot.touch_sensor.is_pressed:

        # DONE: 2. Read the Pixy values for x and y
        # Print the values for x and y
        print("value1: X", robot.pixy.value(1))
        pixy_x = robot.pixy.value(1)

        if robot.pixy.value(1) > 0:
            if robot.pixy.value(1) < 130:  # 130, 190
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
                        # you want it to keep oging while directin is true because when it starts circling it stores
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
            if direction == 2:
                robot.right(turn_speed, turn_speed)
            if direction == 1:
                robot.left(turn_speed, turn_speed)
            else:
                robot.left(turn_speed, turn_speed)

        time.sleep(0.25)

    print("Cannot compute! Cannot compute! Human is too fast!")
    robot.stop()
    ev3.Sound.speak("Cannot compute! Cannot compute! Slow down human!").wait()

# def follow_me(button_state, robot):
#     if button_state:
#         ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
#         robot.keep_going = robot.touch_sensor.is_pressed
#         following_mode()
#
#
# def stop_following(button_state, robot):
#     if button_state:
#         ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
#         robot.keep_going = False
#
#
# def bark(button_state, robot):
#     if button_state:
#         ev3.Sound.play("Dog-barking-short.wav")
#
#
# def handle_shutdown(button_state, dc):
#     """
#     Exit the program.
#
#     Type hints:
#       :type button_state: bool
#       :type dc: DataContainer
#     """
#     if button_state:
#         dc.running = False


# ----------------------------------------------------------------------
main()