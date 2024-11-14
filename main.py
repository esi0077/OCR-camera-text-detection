
# ░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗  ███████╗░██████╗███╗░░░███╗░█████╗░██╗██╗░░░░░██╗
# ██╔══██╗██╔══██╗████╗░████║██║████╗░██║  ██╔════╝██╔════╝████╗░████║██╔══██╗██║██║░░░░░██║
# ███████║██████╔╝██╔████╔██║██║██╔██╗██║  █████╗░░╚█████╗░██╔████╔██║███████║██║██║░░░░░██║
# ██╔══██║██╔══██╗██║╚██╔╝██║██║██║╚████║  ██╔══╝░░░╚═══██╗██║╚██╔╝██║██╔══██║██║██║░░░░░██║
# ██║░░██║██║░░██║██║░╚═╝░██║██║██║░╚███║  ███████╗██████╔╝██║░╚═╝░██║██║░░██║██║███████╗██║
# ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝  ╚══════╝╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚═╝
# OCR for camera detection with login system

import subprocess
import os

# current_directory = os.path.dirname(os.path.abspath(__file__))
# batch_file_path = os.path.join(current_directory, "requirements.bat")
# try:
#     # Run the batch file
#     subprocess.run(batch_file_path, check=True, shell=True)
#     print("Batch file executed successfully.")
# except subprocess.CalledProcessError as e:
#     print(f"An error occurred while executing the batch file!")


# OpenCV is used for capturing video from the webcam and handling image processing
import cv2

# EasyOCR is a library that allows Optical Character Recognition (OCR) for text detection in images
import easyocr

# CustomTkinter is an extension of the Tkinter library, which is used for creating modern graphical user interfaces (GUIs)
import customtkinter

# Threading is used to run tasks (like capturing video and performing OCR) in parallel without freezing the UI
import threading

# Tkinter components for handling text boxes, scrollbars, and pop-up message boxes
from tkinter import Text, Scrollbar, RIGHT, Y, END, messagebox

# PIL (Python Imaging Library) is used to handle image processing and conversion of OpenCV images to display in Tkinter
from PIL import Image, ImageTk

# gTTS (Google Text-to-Speech) is used to convert detected text into audio files (speech)
from gtts import gTTS

# The 'os' library is used for interacting with the operating system, like playing audio files
import os

# MySQL connector is used to establish a connection to a MySQL database for user authentication
import mysql.connector

# The hashlib library provides the 'sha256' hashing algorithm to securely hash passwords before storing them in the database
from hashlib import sha256

from tkinter import messagebox




# Database connection using mysql connector 
mydb = mysql.connector.connect(
    host="10.2.3.236",  # database ip if you run it on your pc type : localhost
    user="armin", # user name of database you can create one or check users table on database
    password="1382", # password of your database
    database="user_auth", # database name you can simply create it like i did in db.sql
    port=3306 # your port that is open for everyone to connect 
)

#Allows Python code to execute PostgreSQL command in a database session
cursor = mydb.cursor() 

# Function to hash passwords using sha256 
# using hash to hide the password that no one can see your password.
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to register a new user
def sign_up(username, password): #function takes tow var that calls : username and password
    if not username or not password: # if field is empty then you get the error
        messagebox.showerror("Error", "Username and password cannot be empty.") # sending error
        return # closing signup function
    try: # try to do something if it dosent or it couldn't so it expected other function
        # hashing the password by using the function : hash_password()
        hashed_password = hash_password(password)
        # execute sql as it sends and insert to username and password 
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        
        mydb.commit()

        # massage that you are good to goo :)
        messagebox.showinfo("Success", "User registered successfully!")
        # if not then error
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
    cap = cv2.VideoCapture(0)
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

# Create app using CustomTkinter
# Create app using CustomTkinter
app = customtkinter.CTk()

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Get the window width and height
window_width = 1024  # or use the desired width
window_height = 768  # or use the desired height

# Calculate the position to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

# Set the window size and position
app.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
app.title("BlindVision")
app.iconbitmap("eye.ico")


# Login/Sign-Up Frame
login_frame = customtkinter.CTkFrame(app)
login_frame.pack(pady=20, padx=20)

# Username entry
username_label = customtkinter.CTkLabel(login_frame, text="Username")
username_label.pack(pady=5)
username_entry = customtkinter.CTkEntry(login_frame)
username_entry.pack(pady=5)

# Password entry
password_label = customtkinter.CTkLabel(login_frame, text="Password")
password_label.pack(pady=5)
password_entry = customtkinter.CTkEntry(login_frame, show="*")
password_entry.pack(pady=5)

# Login button
login_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.pack(pady=10)

# Sign-Up button
signup_button = customtkinter.CTkButton(login_frame, text="Sign Up", command=lambda: sign_up(username_entry.get(), password_entry.get()))
signup_button.pack(pady=10)

app.mainloop()
