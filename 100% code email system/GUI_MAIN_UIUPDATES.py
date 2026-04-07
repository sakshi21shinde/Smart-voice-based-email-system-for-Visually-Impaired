jimport tkinter as tk
from tkinter import messagebox as ms
from PIL import Image, ImageTk
import cv2

# Create the main window
root = tk.Tk()
root.title("Voice-Based Email System")
root.geometry("1600x900")
root.configure(bg="white")

# Load Video
video_path = "100% code/voicewave.mp4"
cap = cv2.VideoCapture(video_path)

# Create Canvas for Video
canvas = tk.Canvas(root, width=1600, height=900, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Update video frames
def update_video():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1600, 900))
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    root.after(25, update_video)

# Title animation
def animate_text():
    global text_x
    text_x += 2
    if text_x > 1300:
        text_x = 10
    title_label.place(x=text_x, y=10)
    root.after(50, animate_text)

# Hover effect helper
def on_hover(widget, enter_color, leave_color):
    widget.bind("<Enter>", lambda e: widget.config(bg=enter_color))
    widget.bind("<Leave>", lambda e: widget.config(bg=leave_color))

# Navigation functions
def Login():
    from subprocess import call
    call(["python", "face_login.py"])

def Register():
    from subprocess import call
    call(["python", "registration_new.py"])

# Top Frame for animated title
top_frame = tk.Frame(root, bg="#8B0000", height=70)
top_frame.place(x=0, y=0, relwidth=1)

text_x = 10
title_label = tk.Label(root, text="🎙️ Voice-Based Email System for Blind People",
                       font=("Segoe Script", 28, "bold"), fg="white", bg="#8B0000")
title_label.place(x=text_x, y=10)
animate_text()

# === Center Frame ===
center_frame = tk.Frame(root, bg="white", bd=3, relief="ridge")
center_frame.place(relx=0.5, rely=0.4, anchor="center", width=500, height=300)

# Welcome Text inside the frame
welcome_label = tk.Label(center_frame, text="Welcome to Voice Mail Portal",
                         font=("Helvetica", 18, "bold"), fg="#333", bg="white")
welcome_label.pack(pady=20)

# Buttons inside center frame
button_style = {
    "font": ("Helvetica", 14, "bold"),
    "bg": "white",
    "fg": "black",
    "bd": 0,
    "relief": "ridge",
    "activebackground": "#FFD700",
    "cursor": "hand2",
    "width": 15,
    "height": 2
}

login_button = tk.Button(center_frame, text="🔐 Login", command=Login, **button_style)
login_button.pack(pady=10)

register_button = tk.Button(center_frame, text="📝 Register", command=Register, **button_style)
register_button.pack(pady=10)

on_hover(login_button, "#FFCC00", "white")
on_hover(register_button, "#FFCC00", "white")

# Info frame at bottom-left
info_frame = tk.Frame(root, bg="white", bd=3, relief="ridge")
info_frame.place(relx=0.5, rely=0.7, anchor="center", width=700, height=150)

info_title = tk.Label(info_frame, text="📢 About the System",
                      font=("Arial", 16, "bold"), bg="white", fg="#333")
info_title.pack(pady=5)

info_text = tk.Label(info_frame,
    text="This voice-based email system is designed for visually impaired users.\n"
         "They can send, receive, and manage emails using just voice commands.\n"
         "Speech-to-text enables composing emails, while text-to-speech reads them aloud.",
    font=("Arial", 12), bg="white", fg="#444", justify="left", anchor="w")
info_text.pack(padx=10)

# Start video loop
update_video()

# Run main loop
root.mainloop()
