import customtkinter as ctk
import pyautogui
import time
from pynput import keyboard

window = ctk.CTk()
window.geometry("300x300")
window.title("Mouse Finder")
window._set_appearance_mode("Dark")
window.resizable(width=False, height=False)

changing = False
pressed_keys = set()
pressed_keys2 = set()
hotkey = None

def hotkeyChange():
    global changing, pressed_keys, pressed_keys2
    changing = True
    pressed_keys.clear()
    pressed_keys2.clear()
    changeBtn.configure(text="Press keys", state="disabled")

changeBtn = ctk.CTkButton(window, text="Change Hotkey", command=hotkeyChange)
changeBtn.pack(pady=10)

lbl = ctk.CTkLabel(window, text="No Hotkey")
lbl.pack(pady=10)

def update_hotkey_display():
    global hotkey
    
    lbl.configure(text=" + ".join(pressed_keys2))

def on_press(key):
    global hotkey, changing, pressed_keys, pressed_keys2
    
    try:
        key_name = key.char if hasattr(key, 'char') else key.name
    except AttributeError:
        key_name = str(key)
    
    pressed_keys.add(key_name)
    print(pressed_keys)

    if changing:
        # Add the key to the set of currently pressed keys
        pressed_keys2.add(key_name)
        update_hotkey_display()

    # Detect if the current combination matches the set hotkey
    elif hotkey and all(k in pressed_keys for k in hotkey):
        print("Hotkey was pressed")
        
        x, y = pyautogui.position()
        
        window_position = "300" + "x" + "300" + "+" + str(x - 150) + "+" + str(y - 150)
        
        toplevel = ctk.CTkToplevel()
        toplevel.geometry(window_position)
        toplevel.title("Here It Is!")
        toplevel.wm_transient(window)

        lbl = ctk.CTkLabel(toplevel, text="Here It Is!")

def on_release(key):
    global hotkey, changing, pressed_keys, pressed_keys2

    try:
        key_name = key.char if hasattr(key, 'char') else key.name
    except AttributeError:
        key_name = str(key)
    
    # Remove the key from the set of currently pressed keys
    pressed_keys.discard(key_name)
    print(pressed_keys)
    
    if changing:

        if not pressed_keys:  # Finalize hotkey once all keys are released
            hotkey = list(pressed_keys2)
            print(hotkey)
            changeBtn.configure(state="normal", text="Change Hotkey")
            changing = False

# Bind key press and release events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

window.mainloop()
