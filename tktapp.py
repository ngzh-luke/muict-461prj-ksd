import customtkinter as ctk
import time


def on_key_event(event):
    global keystroke_timings, current_key, current_time

    key_name = event.char
    event_type = "released" if event.state == 0 else "pressed"

    if event_type == "pressed":
        current_key = key_name
        current_time = time.time()
        keystroke_timings.append(current_time)
        print(f"[Tkinter] Key {key_name} {event_type} at {current_time:.2f}")
        key_event_label.configure(
            text=f"[Tkinter] Key {key_name} {event_type} at {current_time:.2f}")
    else:
        if key_name == current_key:
            prev_time = keystroke_timings[-2]
            current_time = time.time()
            duration = current_time - prev_time
            keystroke_timings.append(duration)
            print(
                f"[Tkinter] Key {key_name} {event_type} at {current_time:.2f}, duration: {duration:.2f}s ({duration * 1000:.0f}ms)")
            key_event_label.configure(
                text=f"[Tkinter] Key {key_name} {event_type} at {current_time:.2f}, duration: {duration:.2f}s ({duration * 1000:.0f}ms)")
            current_key = None


def verify_login():
    global keystroke_timings
    entered_password = password_entry.get()
    if entered_password == "0":
        if analyze_keystroke_dynamics(keystroke_timings):
            login_label.configure(text="Login Successful!")
        else:
            login_label.configure(text="Keystroke dynamics did not match.")
    else:
        login_label.configure(text="Incorrect password.")
    keystroke_timings = []


def analyze_keystroke_dynamics(timings):
    # You can implement your own keystroke dynamics analysis algorithm here
    # For simplicity, let's assume the timings should be within a certain range
    min_time = 0.05
    max_time = 0.3
    # Check every other timing (key press to release)
    for timing in timings[1::2]:
        if timing < min_time or timing > max_time:
            return False
    return True


root = ctk.CTk()
root.geometry("400x300")
root.title("Login App: KSD&Password")

password_label = ctk.CTkLabel(root, text="Enter Password:")
password_label.pack(pady=10)

password_entry = ctk.CTkEntry(root, show="*")
password_entry.pack(pady=10)
password_entry.bind("<KeyPress>", on_key_event)
password_entry.bind("<KeyRelease>", on_key_event)

login_button = ctk.CTkButton(root, text="Login", command=verify_login)
login_button.pack(pady=10)

key_event_label = ctk.CTkLabel(root, text="")
key_event_label.pack(pady=10)

login_label = ctk.CTkLabel(root, text="")
login_label.pack(pady=10)

keystroke_timings = []
current_key = None
current_time = 0

root.mainloop()
