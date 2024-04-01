from pynput import keyboard, mouse
import time
import clipboard

# Initialize variables
pressed_keys = []
last_clipboard_content = clipboard.paste()
last_event_time = time.time()

def on_key_press(key):
    global last_event_time
    try:
        # Attempt to get the character associated with the key
        char = key.char
    except AttributeError:
        # If the key doesn't have a char attribute (e.g., special keys), use the key's name
        char = str(key).split('.')[-1]

    if char.lower() == 'space':
        char = ' '

    # Exclude Shift and Space keys
    if char.lower() not in ['shift_r', 'shift_l']:
        # Add the character to the list of pressed keys
        if char != "enter":
            pressed_keys.append(char)

    # Update the last event time
    last_event_time = time.time()

def on_mouse_click(x, y, button, pressed):
    global last_event_time
    if pressed:
        # Convert button value to button name
        button_name = "left" if button == mouse.Button.left else "right" if button == mouse.Button.right else "middle" if button == mouse.Button.middle else str(button)
        # Print mouse click event details including position
        print(f"Mouse {button_name} clicked at ({x}, {y})")
    # Update the last event time
    last_event_time = time.time()

def on_mouse_release(x, y, button):
    global last_event_time
    # Convert button value to button name
    button_name = "left" if button == mouse.Button.left else "right" if button == mouse.Button.right else "middle" if button == mouse.Button.middle else str(button)
    # Print mouse release event details without position
    print(f"Mouse {button_name} released")
    # Update the last event time
    last_event_time = time.time()

def check_clipboard():
    global last_clipboard_content
    current_clipboard_content = clipboard.paste()
    if current_clipboard_content != last_clipboard_content:
        print("Previous clipboard:", last_clipboard_content)
        print("Current clipboard:", current_clipboard_content)
        last_clipboard_content = current_clipboard_content
        
def print_events():
    global pressed_keys
    if pressed_keys:
        # Concatenate the pressed keys into a single string
        pressed_keys_str = ' '.join(pressed_keys)
        # Print the pressed keys string
        print("Pressed keys:", pressed_keys_str)
        # Reset the list of pressed keys
        pressed_keys = []

# Create keyboard listener
keyboard_listener = keyboard.Listener(on_press=on_key_press)

# Create mouse listener for click and release events
mouse_listener = mouse.Listener(on_click=on_mouse_click, on_release=on_mouse_release)

# Start keyboard listener
keyboard_listener.start()

# Start mouse listener
mouse_listener.start()

while True:
    # Check if the events have been idle for 5 seconds
    if time.time() - last_event_time >= 3.5:
        check_clipboard()
        print_events()
        # Reset the last event time to the current time
        last_event_time = time.time()
    # Sleep for a short interval to reduce CPU usage
    time.sleep(0.1)
