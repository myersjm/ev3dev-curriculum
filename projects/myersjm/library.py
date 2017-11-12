import ev3dev.ev3 as ev3
import math
import time


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
        self.keep_going = self.touch_sensor.is_pressed

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



