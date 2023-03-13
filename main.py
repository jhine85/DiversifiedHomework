import connector
import destination_address
import power_control
import set_volume

# Code for main function. User interface c
from get_power_mode import parse_message


def main():
    global client_socket
    while True:
        print("What do you want to do? Enter the corresponding number:")
        print("0 - Connection for external controller")
        print("1 - Exit the program")
        choice = input()

        if choice == "0":
            print("Do you want to connect to a remote monitor? Enter 0 for No or 1 for Yes.")
            connect_choice = input()
            if connect_choice == "0":
                print("Okay, returning to main menu.")
            elif connect_choice == "1":
                connector.connect_to_monitor(ip_address="192.168.1.10", port=7142)
                print("Successfully connected to monitor!")
                client_socket = connector.connect_to_monitor(ip_address="192.168.1.10", port=7142)
            else:
                print("Invalid choice. Please enter 0 or 1.")

        elif choice == "1":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 1.")

            print("What do you want to do? Enter the corresponding number:")
            print("2 - Set the volume of a monitor")
            print("3 - Send a Power On or Power Off command")
            print("4 - Check Power State")
            print("5 - Disconnect")
            print("6 - Exit the program")

            choice = input()

            if choice == "2":
                print("Which monitor would you like to send a volume command 2.")
                monitor_id = input("Enter a number 1-26 or ALL.")
                volume_value = input("Please enter a number for volume value.")
                command = set_volume.set_volume(monitor_id,volume_value)
                print("Setting monitor " + monitor_id + " to volume " +volume_value)
                connector.send_command_to_monitor(client_socket, command, packet_interval=1000)

            elif choice == "3":
                print("Select a monitor to send a Power On or Power Off Command.")
                monitor_id = input("Enter a number 1-26 or ALL.")
                print("Would you like to Power On or Power Off?")
                power_mode = input("Type 0001 for Power On. Type 0004 for Power Off")
                command = power_control.construct_power_control_message(monitor_id, power_mode)
                print("Sending value " + power_mode + " to monitor " + monitor_id)
                connector.send_command_to_monitor(client_socket,command,packet_interval=1000)

            elif choice == "4":
                print("Checking power state...")
                message = connector.receive_message_from_monitor(client_socket)
                monitor_id, power_mode = parse_message(message)
                if power_mode == "0001":
                    print(f"Monitor {monitor_id} is on.")
                elif power_mode == "0004":
                    print(f"Monitor {monitor_id} is off.")
                else:
                    print(f"Unknown power mode {power_mode} received.")

            elif choice == "5":
                print("Disconnecting from monitor...")
                connector.disconnect_from_monitor(client_socket)
                client_socket = None
                print("Successfully disconnected from monitor.")

            elif choice == "6":
                print("Exiting program...")
                break

            else:
                print("Invalid choice. Please enter a number between 2 and 6.")

main()