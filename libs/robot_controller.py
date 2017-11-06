"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)


        assert self.pixy
        assert self.ir_sensor
        assert self.color_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        #using encoder
        #Take in distance in inches, speed in degrees per seconds

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

        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=left_position, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=right_position, stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp= 900)
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
        self.arm_motor.run_forever(speed_sp = 900)
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
                # DONE: 4. Implement the following strategy to find the beacon.
                # If the absolute value of the current_heading is less than 2, you are on the right heading.
                #     If the current_distance is 0 return from this function, you have found the beacon!  return True
                #     If the current_distance is greater than 0 drive straight forward (forward_speed, forward_speed)
                # If the absolute value of the current_heading is NOT less than 2 but IS less than 10, you need to spin
                #     If the current_heading is less than 0 turn left (-turn_speed, turn_speed)
                #     If the current_heading is greater than 0 turn right  (turn_speed, -turn_speed)
                # If the absolute value of current_heading is greater than 10, then stop and print Heading too far off
                #
                # Using that plan you should find the beacon if the beacon is in range.  If the beacon is not in range your
                # robot should just sit still until the beacon is placed into view.  It is recommended that you always print
                # something each pass through the loop to help you debug what is going on.  Examples:
                #    print("On the right heading. Distance: ", current_distance)
                #    print("Adjusting heading: ", current_heading)
                #    print("Heading is too far off to fix: ", current_heading)

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



