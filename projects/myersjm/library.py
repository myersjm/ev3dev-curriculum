import ev3dev.ev3 as ev3
import math
import time
import traceback


class Snatch3r(object):
    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        #  self.keep_going = self.touch_sensor.is_pressed
        self.break_out = False

        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        # using encoder
        # Take in distance in inches, speed in degrees per seconds

        # Check that the motors are actually connected


        position = 90 * inches_target

        if inches_target != 0 and speed_deg_per_second != 0:
            self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=position,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
            self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=position,
                                            stop_action=ev3.Motor.STOP_ACTION_BRAKE)

            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
            ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        assert self.left_motor.connected
        assert self.right_motor.connected

        if degrees_to_turn > 0:
            left_position = degrees_to_turn * -5.3
            right_position = degrees_to_turn * 5.3
        if degrees_to_turn < 0:
            left_position = degrees_to_turn * -5.3
            right_position = degrees_to_turn * 5.3

        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=left_position,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=right_position,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=900)
        while True:
            if self.touch_sensor.is_pressed:
                break
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while True:
            if self.touch_sensor.is_pressed:
                break
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep()

    def arm_down(self):
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()
        self.arm_motor.position = 0

    def forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def left(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def right(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def back(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def seek_beacon(self):
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            print("Adjusting heading: ", current_heading)
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:

                # Here is some code to help get you started
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                    if current_distance == 1:
                        self.forward(forward_speed, forward_speed)
                        time.sleep(.5)
                        self.stop()
                        return True
                    elif current_distance > 1:
                        self.forward(forward_speed, forward_speed)
                elif math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.left(turn_speed, turn_speed)
                    elif current_heading > 0:
                        self.right(turn_speed, turn_speed)
                elif math.fabs(current_heading) > 10:
                    self.stop()
                    print("Heading too far off.", current_heading)

            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    # ------------------------------------------------------------------------------------------------------
    # Pixy Following Mode
    # ------------------------------------------------------------------------------------------------------
    def following_mode(self):
        print("--------------------------------------------")
        print(" Following ")
        print("--------------------------------------------")
        ev3.Sound.speak("I will follow you.").wait()
        print("Press the touch sensor to exit this program.")  # CHANGE TO REMOTE

        self.pixy.mode = "SIG1"
        turn_speed = 300
        x_values = [0, 0]
        direction = 0

        while not self.touch_sensor.is_pressed:
            if self.ir_sensor.proximity < 10: #self.break_out == True:
                break

            # DONE: 2. Read the Pixy values for x and y
            # Print the values for x and y
            print("value1: X", self.pixy.value(1))
            pixy_x = self.pixy.value(1)

            if self.pixy.value(1) > 0:
                if self.pixy.value(1) < 130:  # 130, 190
                    self.left(turn_speed, turn_speed)
                elif self.pixy.value(1) > 190:
                    self.right(turn_speed, turn_speed)
                elif self.pixy.value(1) >= 130 and self.pixy.value(1) <= 190:
                    self.stop()
                    time.sleep(.01)
                    while self.pixy.value(1) >= 130 and self.pixy.value(1) <= 190:
                        self.forward(600, 600)
                        time.sleep(.01)
                        ev3.Sound.play("DOGBARK.wav")
                        del x_values[0]
                        x_values.append(pixy_x)
                        if x_values[1] > x_values[0]:
                            direction = 2  # right
                        if x_values[1] < x_values[0]:
                            direction = 1  # left

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
                    self.right(turn_speed, turn_speed)
                if direction == 1:
                    self.left(turn_speed, turn_speed)
                else:
                    self.left(turn_speed, turn_speed)

            time.sleep(0.25)

        print("I will stop following you.")
        self.stop()
        ev3.Sound.speak("I will stop following you.").wait()

    def loop_forever(self):
        while True:
            pass

    def shutdown(self):
        self.break_out = True


    def petting_mode(self):
        print("--------------------------------------------")
        print(" Pet Me Mode")
        print("--------------------------------------------")
        ev3.Sound.speak("Bark!").wait()
        ev3.Sound.speak("I like it when my buttons are petted.").wait()
        print("Pet Robo-Dog by pressing: ")
        print("Up, Down, Left, and Right buttons.")
        print("See which button he likes petted the best based on his barks!")

        print("--------------------------------------------")
        print("To exit, press the back button on Robo-Dog.")

        class DataContainer(object):
            def __init__(self):
                self.running = True

        dc = DataContainer()

        btn = ev3.Button()

        btn.on_up = self.handle_up_button
        btn.on_down = self.handle_down_button
        btn.on_left = self.handle_left_button
        btn.on_right = self.handle_right_button

        btn.on_backspace = lambda button_state: self.handle_shutdown(button_state, dc)

        while dc.running:
            btn.process()  # This command is VERY important when using button callbacks!
            time.sleep(0.01)  # A short delay is important to allow other things to happen.

        ev3.Sound.speak("Bark").wait()

    def handle_left_button(self, button_state):
        """Handle IR / button event."""
        if button_state:
            print("Left button is pressed")
            ev3.Sound.speak("Bark!").wait()
        else:
            print("Left button was released")

    def handle_right_button(self, button_state):
        """Handle IR / button event."""
        if button_state:
            print("Right button is pressed")
            ev3.Sound.play("Agressive Bark.wav").wait()
            time.sleep(2)
        else:
            print("Right button was released")

    def handle_up_button(self, button_state):
        if button_state:
            print("Up button is pressed")
            ev3.Sound.play("Longer Whining Bark.wav").wait()
            time.sleep(2)
        else:
            print("Up button was released")

    def handle_down_button(self, button_state):
        if button_state:
            print("Down button is pressed")
            ev3.Sound.play("Whimpering Bark.wav").wait()
            time.sleep(2)
        else:
            print("Down button was released")

    def handle_shutdown(self, button_state, dc):
        if button_state:
            print("back")
            dc.running = False

    def introduce(self):
        ev3.Sound.speak("Hello I am Robo Dog").wait()

    def fetch(self):
        print("--------------------------------------------")
        print(" Fetch Beacon")
        print("--------------------------------------------")
        ev3.Sound.speak("Woof. Woof. I will fetch the beacon.").wait()

        try:
            while True:
                found_beacon = self.seek_beacon()
                if found_beacon:
                    ev3.Sound.speak("I got the beacon")
                    self.arm_up()
                    time.sleep(1)
                    self.shortened_following()
                    self.arm_down()
                command = input("Hit enter to throw the ball again or enter q to quit: ")
                if command == "q":
                    break
        except:
            traceback.print_exc()
            ev3.Sound.speak("Error")

        print("Thanks for playing!")
        ev3.Sound.speak("Thanks for playing!").wait()

    def shortened_following(self):
        self.pixy.mode = "SIG1"
        turn_speed = 300
        x_values = [0, 0]
        direction = 0
        timeout = time.time() + 5
        while True:
            if time.time() > timeout:
                break
            print("value1: X", self.pixy.value(1))
            pixy_x = self.pixy.value(1)

            if self.pixy.value(1) > 0:
                if self.pixy.value(1) < 130:  # 130, 190
                    self.left(turn_speed, turn_speed)
                elif self.pixy.value(1) > 190:
                    self.right(turn_speed, turn_speed)
                elif self.pixy.value(1) >= 130 and self.pixy.value(1) <= 190:
                    self.stop()
                    time.sleep(.01)
                    while self.pixy.value(1) >= 130 and self.pixy.value(1) <= 190:
                        self.forward(600, 600)
                        time.sleep(.01)
                        del x_values[0]
                        x_values.append(pixy_x)
                        if x_values[1] > x_values[0]:
                            direction = 2  # right
                        if x_values[1] < x_values[0]:
                            direction = 1  # left

            else:
                if direction == 2:
                    self.right(turn_speed, turn_speed)
                if direction == 1:
                    self.left(turn_speed, turn_speed)
                else:
                    self.left(turn_speed, turn_speed)

            time.sleep(0.25)

        print("Found you.")
        self.stop()
        ev3.Sound.speak("Found you. I got the ball for you. I'm a good dog.").wait()
