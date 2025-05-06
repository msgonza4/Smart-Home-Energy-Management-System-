


#this creates variables in the python file assigned to values grabbed from the raspberry pi

timestamp = "12:03"
kWh = "insert name of raspberry pi val 1 here"
voltage = "insert name of raspberry pi val 2 here"
current = "insert name of raspberry pi val 3 here"


#test vals

test_data = {
"e1" : 62.5,
"e2" : 382.6,
"e3" : 500,
}


def create_graph(test_data, max_width=50):
    max_val = max(test_data.values())

    for label, value in test_data.items():
        #scales to fit max width of terminal
        num_blocks = int((value / max_val) * max_width)
        bar = '█' * num_blocks
        print(f"{label}: {bar} ({value})")


#this function runs the program till killed that asks the user for which variable they
#want and then displays said variable along with the timestamp
while True:
    comd = float(input("Home Energy Management System.\n1. kWh.\n1.5. Make graph of ___\n2. voltage.\n3. Current.\n4. Quit.\n"))
    if comd == 1:
        print(timestamp,":",kWh,".\n")
    elif comd == 1.5:
        create_graph(test_data)
    elif comd == 2:
        print(timestamp,":",voltage,".\n")
    elif comd == 3:
        print(timestamp,":",current,".\n")
    elif comd == 4:
        print("See you next time!")
        break
    else:
        print("Invalid response. Try again.")
         