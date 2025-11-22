import asyncio
import sys
from bleak import BleakClient, BleakScanner
from pynput import keyboard

# BLE UUIDs (must match Arduino)
SERVICE_UUID = "19B10000-E8F2-537E-4F6C-D104768A1214"
COMMAND_CHAR_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

client = None
active_motors = []
command_queue = None

async def connect_to_robot():
    global client
    
    print("🔍 Scanning for Arduino...")
    devices = await BleakScanner.discover()
    
    robot_address = None
    for device in devices:
        print(f"  Found: {device.name}")
        if device.name == "Arduino":  # Looking for "Arduino"
            robot_address = device.address
            print(f"\n✅ Found Arduino at: {robot_address}")
            break
    
    if not robot_address:
        print("❌ Arduino not found!")
        return None
    
    try:
        client = BleakClient(robot_address)
        await client.connect()
        print("🔵 Connected to Arduino!")
        return client
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

async def send_command(command):
    """Send command to Arduino via Bluetooth"""
    global client
    
    if not client or not client.is_connected:
        print("❌ Not connected!")
        return False
    
    try:
        print(f"📤 Sending: {command}")
        await client.write_gatt_char(COMMAND_CHAR_UUID, command.encode())
        await asyncio.sleep(0.05)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def command_processor():
    """Process commands from queue"""
    while True:
        try:
            command = await asyncio.wait_for(command_queue.get(), timeout=0.1)
            await send_command(command)
        except asyncio.TimeoutError:
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(0.1)

def on_press(key):
    """Handle key press"""
    global active_motors, command_queue
    
    try:
        if hasattr(key, 'char') and key.char:
            command = None
            motor = None
            
            # Motor 1 (Forward/Backward)
            if key.char == 'w':
                command = '1u'
                motor = 1
                print("⬆️  Forward")
            elif key.char == 's':
                command = '1d'
                motor = 1
                print("⬇️  Backward")
            
            # Motor 2 (Left/Right)
            elif key.char == 'a':
                command = '2u'
                motor = 2
                print("⬅️  Left")
            elif key.char == 'd':
                command = '2d'
                motor = 2
                print("➡️  Right")
            
            # Motor 3 (Rotate)
            elif key.char == 'q':
                command = '3u'
                motor = 3
                print("🔄 Motor 3 Up")
            elif key.char == 'e':
                command = '3d'
                motor = 3
                print("🔄 Motor 3 Down")
            
            # Motor 4 (Hand)
            elif key.char == 'r':
                command = '4u'
                motor = 4
                print("✋ Hand Open")
            elif key.char == 'f':
                command = '4d'
                motor = 4
                print("✊ Hand Close")
            
            if command and motor:
                if len(active_motors) < 2 or motor in active_motors:
                    if motor not in active_motors:
                        active_motors.append(motor)
                    
                    if command_queue:
                        try:
                            command_queue.put_nowait(command)
                        except:
                            pass
                else:
                    print(f"⚠️  Max 2 motors! Active: {active_motors}")
                    
    except Exception as e:
        pass

def on_release(key):
    """Handle key release"""
    global active_motors
    
    try:
        if hasattr(key, 'char') and key.char:
            if key.char in ['w', 's']:
                active_motors = [m for m in active_motors if m != 1]
            elif key.char in ['a', 'd']:
                active_motors = [m for m in active_motors if m != 2]
            elif key.char in ['q', 'e']:
                active_motors = [m for m in active_motors if m != 3]
            elif key.char in ['r', 'f']:
                active_motors = [m for m in active_motors if m != 4]
        
        if key == keyboard.Key.esc:
            print("\n🛑 Exiting...")
            return False
    except:
        pass

async def main():
    global client, command_queue
    
    command_queue = asyncio.Queue()
    
    client = await connect_to_robot()
    
    if not client:
        return
    
    print("\n" + "="*50)
    print("🦾 ARDUINO ROBOT ARM CONTROL")
    print("="*50)
    print("\n📍 MOVEMENT (Body Motors):")
    print("  W = Forward        S = Backward")
    print("  A = Left           D = Right")
    print("  Q = Rotate Up      E = Rotate Down")
    print("\n✋ HAND CONTROL (Motor 4):")
    print("  R = Open           F = Close")
    print("\n🎮 OTHER:")
    print("  ESC = Exit")
    print("\n⚠️  Max 2 motors simultaneous (power limit)")
    print("="*50 + "\n")
    
    processor_task = asyncio.create_task(command_processor())
    
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    
    print("🎮 Ready! Press keys...\n")
    
    try:
        while listener.is_alive():
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        processor_task.cancel()
        if client:
            await client.disconnect()
        print("\n✅ Disconnected")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Interrupted")
        sys.exit(0)