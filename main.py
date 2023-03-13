# Main function for External Controller Application


# User interface to allow user to send commands
def user_interface():
    user_option = input('\nPlease type a number corresponding to the desired option and press ENTER:\n'
                        '1 - Connect to a monitor\n'
                        '2 - Set the volume of a monitor\n'
                        '3 - Send a Power On or Power Off command\n'
                        '4 - Exit the program\n')

    if user_option == '1':
        user_input_monitor_id = input('Please type the number of the monitor you would like to connect to and press ENTER.')

