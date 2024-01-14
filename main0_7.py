import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.simpledialog import Dialog
import random
import itertools
import threading
import time
import requests
import json 
import pygame
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


#pygame mixer
pygame.mixer.init()
time.sleep(1.5) #wait for the mixer to warm up b4 loading sound
startup_sound = pygame.mixer.Sound(resource_path("init.mp3"))
beep = pygame.mixer.Sound(resource_path("servo.mp3"))
login_sound = pygame.mixer.Sound(resource_path("initcomp.mp3"))
transmitting_sound = pygame.mixer.Sound(resource_path("connetc_loop.wav"))
nice = pygame.mixer.Sound(resource_path("nice.mp3"))
sent = pygame.mixer.Sound(resource_path("connect_established.wav"))
transmitting = pygame.mixer.Sound(resource_path("transmitting.mp3"))

ice = [
    pygame.mixer.Sound(resource_path("ice.mp3")),
    pygame.mixer.Sound(resource_path("ice2.mp3"))


]
song_played = False




def on_root_click(event):
    global song_played  
    if song_played:
        return

    width = root.winfo_width()
    height = root.winfo_height()

    if event.x >= width - 20 and event.y >= height - 20: 
        random.choice(ice).play()
        song_played = True 





def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

click_sounds = [
    pygame.mixer.Sound(resource_path("key1.mp3")),
    pygame.mixer.Sound(resource_path("key2.mp3")),
    pygame.mixer.Sound(resource_path("key3.mp3")),
    pygame.mixer.Sound(resource_path("key4.mp3")),
    pygame.mixer.Sound(resource_path("key5.mp3")),
    pygame.mixer.Sound(resource_path("key6.mp3")),
    pygame.mixer.Sound(resource_path("key7.mp3"))
]
def play_random_click_sound():
    random.choice(click_sounds).play()



dark_gray = '#404040'
light_text_color = 'white'  

entry_bg = 'gray'  
entry_fg = 'light_text_color' 



def is_digit(input):
    return (input.isdigit() and len(input) <= 2) or input == ""


class NumberPad(Dialog):
    def __init__(self, parent, title, var):
        self.var = var
        super().__init__(parent, title)


    def body(self, master):
        validate_cmd = master.register(is_digit)
        self.entry = ttk.Entry(master, textvariable=self.var, validate="key", validatecommand=(validate_cmd, '%P'))
        self.entry.grid(row=0, column=0, columnspan=3)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('Clear', 4, 0)
        ]
        self.bind("<Button-1>", lambda e: play_random_click_sound())


        for (text, row, col) in buttons:
            action = lambda val=text: self.add_digit(val) if val != 'Clear' else self.clear_entry()
            ttk.Button(master, text=text, command=action).grid(row=row, column=col)

        return self.entry

    def add_digit(self, digit):
        current_value = self.var.get()
        if len(current_value) < 2:  #2 digits
            self.var.set(current_value + digit)

    def clear_entry(self):
        self.var.set('')

    def apply(self):
        print("Applying value:", self.entry.get())#debug print.
        self.var.set(self.entry.get())


class TextInputDialog(Dialog):
    def __init__(self, parent, title, var):
        self.var = var
        super().__init__(parent, title)

    def body(self, master):
        self.entry = ttk.Entry(master, textvariable=self.var, width=50)
        self.entry.grid(row=0, column=0, padx=5, pady=5)
        self.entry.bind("<Key>", lambda e: play_random_click_sound())
        return self.entry

    def apply(self):
        self.var.set(self.entry.get())



#open num pad
def open_number_pad(var):
    NumberPad(root, "Enter Number", var)

def open_text_input(var):
    TextInputDialog(root, "Enter Other Remarks...", var)



def custom_loading_bar(label, sub_label, net_label, popup_active, duration=10):
    process_stages = [
        "Establishing Uplink...",
        "Successful Bounce Ping",
        "Verifying Connection Stability...",
        "Stability OK",
        "Sending Payload...",
        "Payload Broadcasted",
        "Conducting Post-Transmission Analysis...",
        "Receiving Acknowledgment Signal...",
        "Confirming Data Integrity...",
        "Transmission Complete!",
        "Transmission Complete!",
    ]
    stage_duration = duration / len(process_stages)


    def update_bar(stage=0, start_time=time.time()):
        if not popup_active[0]:  #popup check
            return  #quit updating if closed

        #widgets still exist?
        if not label.winfo_exists() or not sub_label.winfo_exists() or not net_label.winfo_exists():
            return

        elapsed_time = time.time() - start_time
        if elapsed_time < duration:
            i = int((elapsed_time % stage_duration) / 0.1)
            bar = ''.join("#" if j <= i % 20 else ' ' for j in range(20))
            label.config(text=f"- Transmitting - [{bar}]")

            if elapsed_time // stage_duration != stage:
                sub_label.config(text=process_stages[stage])
                stage += 1

            net_speed = f"{random.uniform(0.2, 5.3):.2f} Kilobit/s"
            net_label.config(text=net_speed)

            root.after(100, lambda: update_bar(stage, start_time))
        else:
            
            sub_label.config(text="Success!")
            label.config(text="")

    update_bar()



def center_window(win, parent, width=300, height=100):
    """Center 'win' over 'parent' with the given 'width' and 'height'."""
    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    x = parent_x + (parent_width // 2 - width // 2)
    y = parent_y + (parent_height // 2 - height // 2)

    win.geometry(f"{width}x{height}+{x}+{y}")




def send_discord_message(webhook_url, message):
    data = {
        "content": message,
        "username": "Mission Update Relay"
    }

    result = requests.post(webhook_url, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("Error sending message to Discord:", err)
    else:
        print("Message successfully sent to Discord")



def show_transmit_popup():
    transmitting.play(0) 
    popup_active = [True]
    popup = tk.Toplevel(root)
    popup.title("Transmitting Data")
    center_window(popup, root)
    popup.configure(bg='black')
    popup.transient(root)
    popup.grab_set()
    popup.attributes("-topmost", True)

    transmitting_sound.play(-1)


    #main label for custom loading bar
    loading_label = tk.Label(popup, text="", bg='black', fg='green', font=("Consolas", 10))
    loading_label.pack(pady=10)

    # subtext label
    subtext_label = tk.Label(popup, text="", bg='black', fg='green', font=("Consolas", 8))
    subtext_label.pack()

    # network speed label
    net_speed_label = tk.Label(popup, text="", bg='black', fg='green', font=("Consolas", 8))
    net_speed_label.pack(pady=5)

    custom_loading_bar(loading_label, subtext_label, net_speed_label, popup_active, duration=10)

    def close_popup_and_send_message():
        webhook_url = ""
        popup.destroy()
        message_to_send = message_preview.get("1.0", tk.END).strip()
        send_discord_message(webhook_url, message_to_send)
        print("Message sent to Discord:", message_to_send)
        transmitting_sound.stop()
        login_sound.play(0)
        print("Sound Stopped")


    root.after(10000, close_popup_and_send_message)

    return popup



def update_preview(*args):
    print("Update_Preview called")
    bees_number = bees_number_var.get() if main_event_var.get() == "X bees located." else ""
    message = f"[{message_type_var.get()}] DAY {day_var.get()}: {main_event_var.get().replace('X', bees_number)} {additional_info_var.get()}"
    message_preview.configure(state='normal')
    message_preview.delete("1.0", tk.END)
    message_preview.insert(tk.END, message)
    message_preview.configure(state='disabled')
    
    message_type_var.trace_add("write", field_update_handler)
    day_var.trace_add("write", field_update_handler)
    main_event_var.trace_add("write", field_update_handler)
    bees_number_var.trace_add("write", update_preview)
    additional_info_var.trace_add("write", field_update_handler)


def update_bottom_label(is_complete):
    global should_flash
    if is_complete:
        bottom_label.config(text="Awaiting to Transmit Message", fg=retro_color)
        if not should_flash:
            start_flashing()
    else:
        if should_flash:
            stop_flashing()
        bottom_label.config(text="⚠ Command Failed: Fill Required Fields to Transmit ⚠", fg='red')

def send_message():
    if not all([message_type_var.get(), day_var.get(), main_event_var.get()]):
        update_bottom_label(False)
        return

    show_transmit_popup()

    constructed_message = message_preview.get("1.0", tk.END).strip()

    update_bottom_label(True)



# check if fields are filled and control flashing
def check_fields_and_flash():
    global should_flash
    if all([message_type_var.get(), day_var.get(), main_event_var.get()]):
        if not should_flash:
            start_flashing()
    else:
        if should_flash:
            stop_flashing()


def start_flashing():
    global should_flash
    should_flash = True
    flash_label(bottom_label)

def stop_flashing():
    global should_flash
    should_flash = False
    bottom_label.config(foreground='black')

should_flash = False

def flash_label(label):
    global should_flash
    if should_flash:
        current_color = label.cget("foreground")
        next_color = retro_color if current_color == 'black' else 'black'
        label.config(foreground=next_color)
        root.after(500, flash_label, label) 

def field_update_handler(*args):
    is_fields_complete = all([message_type_var.get(), day_var.get(), main_event_var.get()])
    update_bottom_label(is_fields_complete)

def draw_uplink_bars(num_bars):
    uplink_canvas.delete("all")  
    for i in range(5): 
        color = 'green' if i < num_bars else 'grey'
        uplink_canvas.create_rectangle(i * (bar_width + bar_spacing), 0, 
                                       i * (bar_width + bar_spacing) + bar_width, bar_height,
                                       fill=color, outline=color)

def update_uplink_status():
    num_bars = random.randint(1, 5)
    draw_uplink_bars(num_bars)
    
    root.after(6000, update_uplink_status)

def interpolate_color(start_color, end_color, factor: float):
    """Interpolate between two colors."""
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    new_r = start_r + (end_r - start_r) * factor
    new_g = start_g + (end_g - start_g) * factor
    new_b = start_b + (end_b - start_b) * factor
    return int(new_r), int(new_g), int(new_b)

def fade_scanlines(canvas, start_color, end_color, step=10):
    if step > 0:
        factor = (10 - step) / 10
        
        new_color = interpolate_color(start_color, end_color, factor)
        hex_color = f'#{new_color[0]:02x}{new_color[1]:02x}{new_color[2]:02x}'
        
        canvas.itemconfig('scanline', fill=hex_color)
        canvas.after(100, lambda: fade_scanlines(canvas, start_color, end_color, step - 1))
    else:
        canvas.place_forget()
        startup_sound.play()


#currently unused
def bring_canvas_to_top():
    canvas.lift()

def create_ascii_button(parent, text, command, relx=0.5, rely=0.5):  
    top_line = "-----\n"
    sides = "|     |\n"
    bottom_line = "_____"


    ascii_label = tk.Label(parent, text=top_line + sides + bottom_line, font=retro_font, fg=retro_color, bg='black')
    ascii_label.pack(pady=(0, 5))  

    button = tk.Button(parent, text=text, command=command, font=retro_font, fg=retro_color, bg='black', activebackground='black', activeforeground=retro_color, borderwidth=0, highlightthickness=0)
    button.place(in_=ascii_label, relx=relx, rely=rely, anchor="center")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)




root = tk.Tk()
root.title("Mission Update Relay | 0.7")
root.iconbitmap(resource_path('icon.ico'))
root.configure(bg='black')
window_width = 850
window_height = 150
root.geometry(f'{window_width}x{window_height}')
root.resizable(False, False)
root.attributes('-topmost', True)
root.grid_rowconfigure(0, weight=1)  
root.grid_rowconfigure(1, weight=0)  
root.grid_columnconfigure(0, weight=1)
root.bind("<Button-1>", lambda e: play_random_click_sound())
root.bind("<Key>", lambda e: play_random_click_sound())


retro_font = tkFont.Font(family="Consolas", size=10)
retro_color = 'green'
style = ttk.Style()
style.theme_use('clam')



entry_bg = dark_gray 
entry_fg = light_text_color 

style = ttk.Style()
style.configure('TFrame', background='dark_gray')
style.configure('TLabel', background='black', foreground=retro_color, font=retro_font)
style.configure('TEntry', foreground=entry_fg, background=entry_bg, fieldbackground=entry_bg, insertbackground=entry_fg)
style.map('TEntry', fieldbackground=[('readonly', entry_bg)], foreground=[('readonly', entry_fg)], background=[('readonly', entry_bg)])
style.configure('TCombobox', background='blue', foreground='white')
style.map('TCombobox', fieldbackground=[('readonly', dark_gray)], selectbackground=[('readonly', dark_gray)], background=[('readonly', dark_gray)])
style.configure('TButton', background='black', foreground=retro_color, font=retro_font)
style.map('TButton', background=[('active', '!disabled', 'black'), ('pressed', 'black')], foreground=[('active', '!disabled', retro_color), ('pressed', retro_color)])


main_frame = ttk.Frame(root)
main_frame.grid(sticky='nsew')
for i in range(6):
    main_frame.grid_columnconfigure(i, weight=1)



message_type_var = tk.StringVar()
day_var = tk.StringVar()
main_event_var = tk.StringVar()
additional_info_var = tk.StringVar()
bees_number_var = tk.StringVar()




sentence_creator_frame = ttk.Frame(main_frame)
sentence_creator_frame.grid(row=0, column=0, columnspan=6, sticky='ew', padx=5, pady=5)

ttk.Label(sentence_creator_frame, text="Protocol:").pack(side='left')
ttk.Combobox(sentence_creator_frame, textvariable=message_type_var, values=["LOG", "LIVE-BROADCAST", "RESET", "CRITICAL"], state="readonly").pack(side='left')

ttk.Label(sentence_creator_frame, text="Log Day:").pack(side='left')
day_entry = ttk.Entry(sentence_creator_frame, textvariable=day_var, state="readonly")
day_entry.bind("<Button-1>", lambda e: open_number_pad(day_var))
day_entry.pack(side='left')

ttk.Label(sentence_creator_frame, text="Primary Operation:").pack(side='left')
main_event_combo = ttk.Combobox(sentence_creator_frame, textvariable=main_event_var, values=["No bees located.", "X bees located.", "Casualties Reported.", "All Personnel MIA.", "New personnel hired.", "Quota Accomplished.", "Unsuccessful Mission.","Successful Mission.","Mutiny Reported."], state="readonly")
main_event_combo.bind("<<ComboboxSelected>>", lambda e: open_number_pad(bees_number_var) if main_event_var.get() == "X bees located." else None)
main_event_combo.pack(side='left')


ttk.Label(sentence_creator_frame, text="Custom Notes:").pack(side='left')
additional_info_entry = ttk.Entry(sentence_creator_frame, textvariable=additional_info_var, state="readonly")
additional_info_entry.bind("<Button-1>", lambda e: open_text_input(additional_info_var))
additional_info_entry.pack(side='left')



message_preview_frame = ttk.Frame(main_frame)
message_preview_frame.grid(row=3, column=0, columnspan=6, sticky='nsew', padx=5, pady=5)



message_preview = tk.Text(message_preview_frame, height=2, width=80, state="disabled")
message_preview.configure(bg=dark_gray, fg=light_text_color)
message_preview.pack()

create_ascii_button(message_preview_frame, ">Transmit Data<", send_message)

bottom_text = "Awaiting to Transmit Data"
bottom_label = tk.Label(root, text=bottom_text, font=retro_font, fg=retro_color, bg='black')
bottom_label.grid(row=1, column=0, sticky="ew", pady=10) 


uplink_x, uplink_y = 10, window_height - 30 
bar_width, bar_height = 10, 20  
bar_spacing = 5 


uplink_canvas = tk.Canvas(root, bg='black', highlightthickness=0, width=100, height=30) 
uplink_canvas.place(x=uplink_x, y=uplink_y)

draw_uplink_bars(5) 


uplink_label = tk.Label(root, text="Uplink Status", fg="green", bg="black", font=("Consolas", 10))
uplink_label.place(x=uplink_x - 10, y=uplink_y - -10)  


update_uplink_status()


message_type_var.trace_add("write", update_preview)
day_var.trace_add("write", update_preview)
main_event_var.trace_add("write", update_preview)
bees_number_var.trace_add("write", update_preview)
additional_info_var.trace_add("write", update_preview)

root.bind("<Button-1>", on_root_click)



canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
line_spacing = 2  
line_color = "#555555"  


start_rgb = canvas.winfo_rgb(line_color) 
end_rgb = canvas.winfo_rgb(root['bg']) 

init_message = "Initializing Lethal Co. Mission Update Relay..."


init_message_id = canvas.create_text(window_width // 2, window_height // 2, text=init_message, fill="orange", font=("Consolas", 12, "bold"), tags="init_message")

for i in range(0, window_height, line_spacing):
    canvas.create_line(0, i, window_width, i, fill=line_color, tags='scanline')

startup_sound_length = 3000
sent.play()

root.after(startup_sound_length, lambda: fade_scanlines(canvas, start_rgb, end_rgb))


frames_and_widgets = [main_frame, sentence_creator_frame, message_preview_frame, bottom_label, uplink_canvas]


def bind_widgets(parent):
    for widget in parent.winfo_children():
        if widget not in [day_entry, additional_info_entry]:  
            if isinstance(widget, (tk.Button, ttk.Button, ttk.Entry, ttk.Combobox, tk.Text, ttk.Label)):
                widget.bind("<Button-1>", lambda e: play_random_click_sound())
            if isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
                bind_widgets(widget) 



bind_widgets(root)


root.mainloop()
