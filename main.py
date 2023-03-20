import connector
import power_control
import set_volume
import get_power_mode

from get_power_mode import parse_message


# Code for main function. User interface
def main():
    while True:
        print("What do you want to do? Enter the corresponding number:")
        print("0 - Connection for external controller")
        print("1 - Exit the program")
        print("2 - Other options")
        choice = input()

        # User input 0, connection to external monitor
        if choice == "0":
            print("Do you want to connect to a remote monitor? Enter 0 for No or 1 for Yes.")
            connect_choice = input()
            if connect_choice == "0":
                print("Okay, returning to main menu.")
            elif connect_choice == "1":
                connector.connect_to_monitor(ip_address="192.168.0.10", port=7142)
                client_socket = connector.connect_to_monitor(ip_address="192.168.0.10", port=7142)
            else:
                print("Invalid choice. Please enter 0 or 1.")

        # User input 1, closes the program
        elif choice == "1":
            print("Exiting program...")
            break

        # Other User input
        else:

            print("What do you want to do? Enter the corresponding number:")
            print("3 - Set the volume of a monitor")
            print("4 - Send a Power On or Power Off command")
            print("5 - Check Power State")
            print("6 - Disconnect")
            print("7 - Exit the program")

            choice = input()

            # User input 3, Volume command
            if choice == "3":
                print("Which monitor would you like to send a volume command to.")
                monitor_id = input("Enter a number 1-26 or ALL.")
                volume_value = input("Please enter a number for volume value.")
                command = set_volume.set_volume(monitor_id, int(volume_value))
                vlm_command = input("Is the command correct? 1 for Yes. 2 for No")
                if vlm_command == "1":
                    print("Sending value " + volume_value + " to monitor " + monitor_id)
                    connector.send_command_to_monitor(client_socket, str(command), packet_interval=1000)
                else:
                    print("Command not sent.")

            # User input 4, Power On or Power Off Command
            elif choice == "4":
                print("Select a monitor to send a Power On or Power Off Command.")
                monitor_id = input("Enter a number 1-26 or ALL.")
                print("Would you like to Power On or Power Off?")
                power_mode = input("Type 0001 for Power On. Type 0004 for Power Off")
                command = power_control.construct_power_control_message(monitor_id, int(power_mode))
                print(f"Command to be sent to monitor: {command}")
                pwr_command = input("Is the command correct? 1 for Yes. 2 for No")
                if pwr_command == "1":
                    print("Sending value " + power_mode + " to monitor " + monitor_id)
                    connector.send_command_to_monitor(client_socket, str(command), packet_interval=1000)
                else:
                    print("Command not sent.")

            # User input 5, Displays power state
            elif choice == "5":
                monitor_id = input("Select a monitor")
                print("Checking power state...")
                get_power_mode.get_power_setting(monitor_id)
                message = connector.receive_message_from_monitor(client_socket)
                monitor_id, power_mode = parse_message(message)
                if power_mode == "0001":
                    print(f"Monitor {monitor_id} is on.")
                elif power_mode == "0004":
                    print(f"Monitor {monitor_id} is off.")
                else:
                    print(f"Unknown power mode {power_mode} received.")

            # User input 6, Disconnects from monitor
            elif choice == "6":
                print("Disconnecting from monitor...")
                connector.disconnect_from_monitor(client_socket)
                client_socket = None
                print("Successfully disconnected from monitor.")

            # User input 7, Closes the program
            elif choice == "7":
                print("Exiting program...")
                break

            # User input invalid
            else:
                print("Invalid choice. Please enter a number between 3 and 7.")


main()
