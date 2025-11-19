import serial
from pynput import keyboard
import time

arduino = serial.Serial('/dev/tty.usbmodemB081849E54C82', 9600, timeout=1)

arduino = serial.Serial('/dev/tty.usbmodemB081849E54C82', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to initialize

print("Stepper Motor Control Ready!")
print("⬆️  = Move Up")
print("⬇️  = Move Down")
print("ESC = Exit")

def on_press(key):
    try:
        if key == keyboard.Key.up:
            arduino.write(b'u')
            print("↑ Sending UP command")
        elif key == keyboard.Key.down:
            arduino.write(b'd')
            print("↓ Sending DOWN command")
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n🛑 Exiting...")
        arduino.close()
        return False

# Start listening to keyboard
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()