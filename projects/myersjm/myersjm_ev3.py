import mqtt_remote_method_calls as com
import library as lib


def main():
    robot = lib.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    loop_forever()  # Calls a function that has a while True: loop within it to avoid letting the program end.


def loop_forever():
    while True:
        pass
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()