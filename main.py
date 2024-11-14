import subprocess
import os
import cv2
import easyocr
import customtkinter
from tkinter import Text, Scrollbar, RIGHT, Y, END, messagebox, simpledialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
from gtts import gTTS
import mysql.connector
from hashlib import sha256
from tkinter import filedialog
import numpy as np
import threading
from PIL import Image, ImageTk



# Database connection using mysql connector 
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="10.2.3.236",  # database ip if you run it on your pc type : localhost
            user="armin",  # user name of database you can create one or check users table on database
            password="1382",  # password of your database
            database="user_auth",  # database name you can simply create it like i did in db.sql
            port=3306  # your port that is open for everyone to connect
        )
        return mydb
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None

# Database connection
mydb = connect_to_database()
if mydb is not None:
    cursor = mydb.cursor()

# Function to hash passwords using sha256 
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to register a new user
def sign_up(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        mydb.commit()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Function to authenticate user login
def login(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    hashed_password = hash_password(password)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Success", "Login successful!")
        open_main_application()  # Open the OCR application on successful login
    else:
        messagebox.showerror("Error", "Invalid username/password.")

# Function to open the main OCR application after login
def open_main_application():
    global app
    login_frame.pack_forget()  # Hide the login frame

    # Initialize EasyOCR reader for multiple languages
    reader = easyocr.Reader(['en', 'fr', 'es', 'no'], gpu=True)

    # Label to display the video feed
    label = customtkinter.CTkLabel(app, text="", height=380, anchor="center")
    label.pack(padx=0, pady=0)

    # Frame to contain the scrollable text box
    text_frame = customtkinter.CTkFrame(app)
    text_frame.pack(padx=20, pady=10)

    # Scrollbar for the text box
    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Text box to display the detected text
    text_box = Text(text_frame, wrap='word', yscrollcommand=scrollbar.set, height=10, width=80)
    text_box.pack(padx=5, pady=5)

    # Configure the scrollbar
    scrollbar.config(command=text_box.yview)

    # Initialize camera with reduced resolution
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set lower resolution width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set lower resolution height

    # Flag for controlling OCR frequency
    detect_text = False
    detected_text = ""  # Variable to store detected text for TTS
    detected_language = 'en'  # Default language for TTS

    # Function to continuously update the camera feed in the label
    def update_preview():
        ret, frame = cap.read()
        if ret:
            # Convert frame to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Show the live preview without OCR
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            # Perform text detection every few frames (controlled by detect_text flag)
            if detect_text:
                threading.Thread(target=perform_ocr, args=(rgb_frame,)).start()

        # Update preview every 10ms
        label.after(10, update_preview)

    # Function to perform OCR and update the UI with detected text
    def perform_ocr(rgb_frame):
        nonlocal detect_text, detected_text, detected_language
        detect_text = False  # Prevent re-triggering OCR while it's running

        # Perform text detection
        text_ = reader.readtext(rgb_frame)
        threshold = 0.1
        detected_text = ""  # Clear previously detected text

        for t in text_:
            bbox, text, score = t
            if score > threshold:
                detected_text += f"{text}\n"
                detected_language = detect_language(text)  # Detect the language of the text
                # Convert bbox points to integers and draw the boxes
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                cv2.rectangle(rgb_frame, top_left, bottom_right, (0, 255, 0), 2)

        # Clear the text box and insert the detected text
        text_box.delete(1.0, END)
        text_box.insert(END, detected_text)

        # Convert the frame with bounding boxes to ImageTk format
        img_with_boxes = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img_with_boxes)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    def detect_language(text):
        if any(char in text for char in "abcdefghijklmnopqrstuvwxyz"):
            return 'en'
        elif any(char in text for char in "áéíóúñ"):
            return 'es'
        elif any(char in text for char in "àâçéèêëîôû"):
            return 'fr'
        elif any(char in text for char in "æøå"):
            return 'no'
        return 'en'  

    # Function to capture a frame and trigger OCR
    def capture_and_analyze():
        nonlocal detect_text
        detect_text = True  # Trigger OCR on the next frame

    # Function to convert the detected text to speech and delete it
    def text_to_speech():
        nonlocal detected_text, detected_language
        if detected_text:
            tts = gTTS(text=detected_text, lang=detected_language, slow=False)
            audio_file = "detected_text.mp3"
            tts.save(audio_file)
            os.system(f"start {audio_file}")  # For Windows; use "afplay" for macOS or "xdg-open" for Linux

            # Clear the detected text after playing
            detected_text = ""
            text_box.delete(1.0, END)  # Clear the text box

    update_preview()

    # Analyze button
    capture_button = customtkinter.CTkButton(app, text="Analyze", command=capture_and_analyze)
    capture_button.pack(padx=20, pady=10)

    # Text-to-Speech button
    tts_button = customtkinter.CTkButton(app, text="Text-to-Speech", command=text_to_speech)
    tts_button.pack(padx=20, pady=10)

    # Training button to open the training pop-up
    train_button = customtkinter.CTkButton(app, text="Train AI", command=open_train_popup)
    train_button.pack(pady=10)

# Function to open a pop-up for importing a font or taking a picture for training
def open_train_popup():
    train_popup = customtkinter.CTkToplevel(app)
    train_popup.title("Train Model")

    # Add a descriptive text label at the top for user instructions
    instruction_label = customtkinter.CTkLabel(
        train_popup, text="Use this pop-up to add fonts for training.", text_color="gray"
    )
    instruction_label.pack(padx=10, pady=10)

    # Frame for import font option
    frame = customtkinter.CTkFrame(train_popup)
    frame.pack(padx=20, pady=20)

    # Label to display instructions for adding fonts
    font_instructions = customtkinter.CTkLabel(frame, text="You can add fonts here as needed.")
    font_instructions.pack(pady=(0, 10))

    # Button to import a font
    import_font_button = customtkinter.CTkButton(frame, text="Import Font", command=import_font)
    import_font_button.pack(padx=10, pady=10)


# Function to import a font for training
def import_font():
    font_file = filedialog.askopenfilename(filetypes=[("TrueType Font", "*.ttf")])
    if font_file:
        # Placeholder for actual font processing
        messagebox.showinfo("Font Import", f"Font imported successfully: {font_file}")
        # You would now need to integrate the font into your training dataset (using a library like PIL for generating synthetic images)





# Main login page setup
app = customtkinter.CTk()

# Login screen components
login_frame = customtkinter.CTkFrame(app)
login_frame.pack(padx=20, pady=20)

username_label = customtkinter.CTkLabel(login_frame, text="Username")
username_label.pack(pady=10)

username_entry = customtkinter.CTkEntry(login_frame)
username_entry.pack(pady=10)

password_label = customtkinter.CTkLabel(login_frame, text="Password")
password_label.pack(pady=10)

password_entry = customtkinter.CTkEntry(login_frame, show="*")
password_entry.pack(pady=10)

login_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.pack(pady=20)

signup_button = customtkinter.CTkButton(login_frame, text="Sign Up", command=lambda: sign_up(username_entry.get(), password_entry.get()))
signup_button.pack(pady=10)

# Main window setup
app.geometry("600x400")
app.title("Blindvison")
app.iconbitmap("eye.ico")

app.mainloop()
