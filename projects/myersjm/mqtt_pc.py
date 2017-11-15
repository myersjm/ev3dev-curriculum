"""
Jessica Myers
CSSE120 Robot Final Project
'Robo-Dog'
8 November 2017
Project Files: myersjm_ev3, mqtt_pc, and library, as well as assorted sounds
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

    #------------------------------------------------------------------------------------------------------
    # TKinter Interface GUI
    #------------------------------------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("Robo-Dog")
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

    intro_label = ttk.Label(frame, text="See what Robo-Dog has to say.", font=("Helvetica", 12))
    intro_label.grid(row=0, column=2)

    button1 = ttk.Button(frame, text="Follow Me!")
    button1.grid(row=1, column=1)
    button1['command'] = lambda: follow_me(mqtt_client)

    button1_label = ttk.Label(frame, text="Have Robo-Dog follow you around!", font=("Helvetica", 12))
    button1_label.grid(row=1, column=2)

    button2 = ttk.Button(frame, text="Pet Me!")
    button2.grid(row=2, column=1)
    button2['command'] = lambda: pet_me(mqtt_client)

    intro_label = ttk.Label(frame, text="Pet Robo-Dog for various reactions.", font=("Helvetica", 12))
    intro_label.grid(row=2, column=2)

    fetch_button = ttk.Button(frame, text="Fetch")
    fetch_button.grid(row=4, column=1)
    fetch_button['command'] = lambda: fetch_ball(mqtt_client)

    fetch_label = ttk.Label(frame, text="Have Robo-Dog fetch.", font=("Helvetica", 12))
    fetch_label.grid(row=4, column=2)

    e_button = ttk.Button(frame, text="Exit")
    e_button.grid(row=5, column=1)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def follow_me(mqtt_client):
    mqtt_client.send_message("following_mode")


def pet_me(mqtt_client):
    mqtt_client.send_message("petting_mode")


def intro(mqtt_client):
    mqtt_client.send_message("introduce")


def fetch_ball(mqtt_client):
    mqtt_client.send_message("fetch")


# ----------------------------------------------------------------------
main()