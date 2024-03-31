import evdev, sys, os, threading

# supported keys for bluetooth neckband
# KEY_VOLUMEUP  = 114
# KEY_VOLUMEDOWN = 115
# KEY_PAUSECD
# KEY_PLAYCD

def handleUpButton():
    os.system("pkill i3lock")

def handleLowButton():
    os.system("i3lock")

def handlePowerButton():
    print("power button pressed")

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
volDev = None # used for volume buttons
avDev = None # used for power button
target ="pTron BT"
for device in devices:
    if device.name.find(target) != -1:
        if device.name.find("AVRCP") != -1:
            avDev = device
        else:
            volDev = device
        print(f"Found {target} at {device.path}")

if volDev == None:
    print(f"volume controls for {target} not found")
    sys.exit(1)

if avDev == None:
    print(f"power controls for {target} not found")
    sys.exit(1)

def checkUpDown(device):
    lowCheck = False
    upCheck = False
    for event in device.read_loop():
        if event.code == 114:
            if not lowCheck:
                lowCheck = True
                handleLowButton()
            else:
                lowCheck = False
        elif event.code == 115:
            if not upCheck:
                upCheck = True
                handleUpButton()
            else:
                upCheck = False

def checkPower(device):
    powerCheck = False
    for event in device.read_loop():
        if not powerCheck:
            powerCheck = True
            handlePowerButton()
        else:
            powerCheck = False

t1 = threading.Thread(target=checkUpDown, args=(volDev, ))
t2 = threading.Thread(target=checkPower, args=(avDev, ))

t1.start()
t2.start()

t1.join()
t2.join()
