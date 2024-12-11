# ░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗  ███████╗░██████╗███╗░░░███╗░█████╗░██╗██╗░░░░░██╗
# ██╔══██╗██╔══██╗████╗░████║██║████╗░██║  ██╔════╝██╔════╝████╗░████║██╔══██╗██║██║░░░░░██║
# ███████║██████╔╝██╔████╔██║██║██╔██╗██║  █████╗░░╚█████╗░██╔████╔██║███████║██║██║░░░░░██║
# ██╔══██║██╔══██╗██║╚██╔╝██║██║██║╚████║  ██╔══╝░░░╚═══██╗██║╚██╔╝██║██╔══██║██║██║░░░░░██║
# ██║░░██║██║░░██║██║░╚═╝░██║██║██║░╚███║  ███████╗██████╔╝██║░╚═╝░██║██║░░██║██║███████╗██║
# ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝  ╚══════╝╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝╚══════╝╚═╝
# github : https://github.com/esi0077
# mail : armines765@gmail.com


import subprocess  # Used to run system-level commands and processes.
import os  # Provides functions to interact with the operating system, such as file and directory operations.
import cv2  # OpenCV library for computer vision tasks like image processing, face detection, etc.
import easyocr  # Optical Character Recognition (OCR) library for extracting text from images.
import customtkinter  # Custom Tkinter module to create advanced, styled GUI applications.
from tkinter import Text, Scrollbar, RIGHT, Y, END, messagebox, simpledialog  
# Tkinter components:
# - Text: For multi-line text widgets.
# - Scrollbar: Adds scrolling functionality.
# - RIGHT, Y, END: Constants for widget positioning and content control.
# - messagebox: To show dialog boxes (e.g., alerts, confirmations).
# - simpledialog: For user input dialogs (single-field).

from PIL import Image, ImageTk, ImageFont, ImageDraw  
# Python Imaging Library (Pillow) components:
# - Image: Handles image creation and processing.
# - ImageTk: Converts images for use with Tkinter GUI.
# - ImageFont: Defines and loads fonts for text rendering on images.
# - ImageDraw: Used to draw shapes and text on images.

import gtts
# Google Text-to-Speech library for converting text to spoken audio.

import mysql.connector  
# Allows interaction with a MySQL database for storing and retrieving data.

from hashlib import sha256  
# Hashing library for securely encoding data (passwords).

from tkinter import filedialog  
# Provides a dialog box to open/save files.

import numpy as np  
# Library for numerical computations; works with arrays and matrices.

import threading  
# For concurrent execution, allowing multiple tasks (threads) to run simultaneously.

import shutil  
# High-level file operations like copying and removing files or directories.

import uuid  
# Generates universally unique identifiers (UUIDs), often used for unique keys.


# runing bat file to install everything 
# os.system("requirements.bat")
# Database connection using mysql.connector
def connect_to_database():
    # trying to connect to the host by using ip address 
    # user : the database username that we have it can be root or whatever
    # password : using a password to connect to database (you can choose it when u making the user)
    # database : database name that we make (wrote in db.sql)
    # port : we use an open port to connect to target pc like 3306 here 
    # ports are important to connect and changing on which app you going to use it on 
    # some ports : 8080 , 30120 , ... (check firewall for it)
    try:
        mydb = mysql.connector.connect(
            host="10.2.3.97",  # database IP or localhost
            user="armin",  # database username
            password="1382",  # database password
            database="user_auth",  # database name
            port=3306  # database port
        )
        # for connecting to localhost then this code work
        # mydb = mysql.connector.connect(
        #     host="localhost",  # database IP or localhost
        #     user="root",  # database username
        #     password="",  # database password
        #     database="user_auth",  # database name
        #     port=3306  # database port
        # )
        return mydb
        # if there is an error with data base then its going to show you the error
        # messagebox is the alert pop up
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Error: {err}")
        return None


# Database connection
# if we have database or conection then you can do stuff
mydb = connect_to_database()
if mydb is not None:
    cursor = mydb.cursor()


# Function to hash passwords using sha256 + salt
def hash_password(password):
    salt = uuid.uuid4().hex # Generate a unique salt that no one can crack using uuid and hex 
                            # uuid make a uniqe id and we hex the id after it to make it harder to read
                            # and we call it salt id that use as key for hashed password
    hashed_password = sha256(salt.encode() + password.encode()).hexdigest() 
    # now we hash the password and adding it to password and using hexdigest to make it more readble 
    # normally sha256 output is binery so better to use hexdigest to make it human readble.
    return salt, hashed_password
    # returning salt and hash password so we can read it later.


# Function to register a new user
# Fetching data : username and password 
def sign_up(username, password):
    # if the fields of username and password are not full so the app will pop up the error 
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    # if the fields are ok then it will do the salting process 
    try:
    # and after hashing process it going to send it to database and insert it to rows that  
    # named : username , password , salt
        salt, hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (%s, %s, %s)", 
                       (username, hashed_password, salt))
        mydb.commit()
    # sending pop up that shows you are in order and you got username and password
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        # if username exists then you get an error
        messagebox.showerror("Error", "Username already exists.")



# Function to authenticate user login
# fetching data: username and password
def login(username, password):
    # same as sign up you can not have any empty fileds
    if not username or not password:
        messagebox.showerror("Error", "Username and password cannot be empty.")
        return
    try:
        # geting password and salt to table list (for the user input)
        cursor.execute("SELECT password, salt FROM users WHERE username=%s", (username,))
        result = cursor.fetchone()
        if result:
            # if we get the password from database and add salt to it we get a result 
            # and we try to make a hash on it 
            # if the hash and password are the same so you get Success and if not so error
            stored_password, salt = result
            hashed_password = sha256(salt.encode() + password.encode()).hexdigest()
            if hashed_password == stored_password:
                messagebox.showinfo("Success", "Login successful!")
                open_main_application()  # Open the OCR application on successful login
            else:
                messagebox.showerror("Error", "Invalid username/password.")
        else:
            messagebox.showerror("Error", "Invalid username/password.")
    except Exception as e:
        # if there is an error that we dont know what it is then this message pop up
        messagebox.showerror("Error", f"An error occurred: {e}")



# Function to open the main OCR application after login
def open_main_application():
    global app # using to show python the general app
    login_frame.pack_forget()  # Hide the login frame by using tk function

    # Initialize EasyOCR reader for multiple languages
    # all langueges on easyocr has been aded to this list so we cant add more then this 
    # Note : you can if you want to use another lib or your own language system
    reader = easyocr.Reader(['en', 'fr', 'es', 'no', 'de', 'it'], gpu=True) # I am are using gpu for faster check but you can use cpu if you got a good one

    # Label to display the video feed (use height like html to change the size)
    label = customtkinter.CTkLabel(app, text="", height=380, anchor="center")
    label.pack(padx=0, pady=0)

    # Frame to contain the scrollable text box (white box under video)
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
    detect_text = False # it makes the app not scaning every secound so its not going to be laggy
    detected_text = ""  # Variable to store detected text for TTS {text to speach}
    detected_language = 'en'  # Default language for TTS

    # Function to continuously update the camera feed in the label
    def update_preview():
        # Capture a frame from the camera
        ret, frame = cap.read()
    
    # Check if the frame was successfully captured
        if ret:
        # Convert the captured frame from BGR (OpenCV format) to RGB (PIL format)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame into a format that can be displayed in a Tkinter label
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with the new image
            label.imgtk = imgtk
            label.configure(image=imgtk)

        # Perform text detection (OCR) every few frames, controlled by 'detect_text' flag
            if detect_text:
                # Start a new thread to perform OCR on the current frame (this prevents blocking the main UI thread)
                threading.Thread(target=perform_ocr, args=(rgb_frame,)).start()

    # Schedule the 'update_preview' function to be called again in 10ms (creating a continuous loop)
        label.after(10, update_preview)


    # Function to perform OCR and update the UI with detected text
    def perform_ocr(rgb_frame):
        nonlocal detect_text, detected_text, detected_language
        detect_text = False  # Prevent re-triggering OCR while it's running (this ensures OCR is not called repeatedly)

        # Perform text detection using the OCR reader object
        text_ = reader.readtext(rgb_frame)  # The reader detects any text present in the input RGB frame

        threshold = 0.1  # Set a threshold to filter low-confidence text detections
        detected_text = ""  # Clear previously detected text to store new results

        for t in text_:
            bbox, text, score = t  # Unpack the bounding box (bbox), detected text, and confidence score for each detected text block
            if score > threshold:  # Only process text if the detection confidence score is above the threshold
                detected_text += f"{text}\n"  # Append the detected text to the string with a newline

                detected_language = detect_language(text)  # Detect the language of the detected text

                # Convert the coordinates of the bounding box from floats to integers
                top_left = tuple(map(int, bbox[0]))  # Get the top-left corner of the bounding box
                bottom_right = tuple(map(int, bbox[2]))  # Get the bottom-right corner of the bounding box
                
                # Draw a green rectangle around the detected text on the original frame
                cv2.rectangle(rgb_frame, top_left, bottom_right, (0, 255, 0), 2)  # Draw a rectangle with a green border and thickness of 2

        # Clear the previous text in the text box (likely a GUI element) to display the new detected text
        text_box.delete(1.0, END)  # Delete all text in the text box
        text_box.insert(END, detected_text)  # Insert the new detected text at the end of the text box

        # Convert the frame with the bounding boxes drawn to an image format suitable for GUI display (using tkinter)
        img_with_boxes = Image.fromarray(rgb_frame)  # Convert the frame with rectangles (bounding boxes) into an Image object

        # Create an ImageTk object to display the image in a Tkinter label
        imgtk = ImageTk.PhotoImage(image=img_with_boxes)  # Convert the Image object into a Tkinter-compatible photo image

        label.imgtk = imgtk  # Store the image in the label to prevent garbage collection
        label.configure(image=imgtk)  # Update the label with the new image (show the frame with bounding boxes)

    # my method to detect languages if txt included this words then it going to type it in that language 
    # def detect_language(text):
    #     if any(char in text for char in "abcdefghijklmnopqrstuvwxyz"):
    #         return 'en'
    #     elif any(char in text for char in "áéíóúñ"):
    #         return 'es'
    #     elif any(char in text for char in "àâçéèêëîôû"):
    #         return 'fr'
    #     elif any(char in text for char in "æøå"):
    #         return 'no'
    #     return 'en'  

    # new method to detect language in text format for gtts 
    # testing langdetect liberary 
    from langdetect import detect

    def detect_language(text):
        allowed_languages = {'en', 'es', 'fr', 'no'}
        try:
            detected_language = detect(text)
            return detected_language if detected_language in allowed_languages else 'en'
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'en'  # Default to English in case of error
           



    # Function to capture a frame and trigger OCR
    def capture_and_analyze():
        nonlocal detect_text
        detect_text = True  # Trigger OCR on the next frame

    from gtts import gTTS  # Ensure you import gTTS correctly

    def text_to_speech():
        nonlocal detected_text, detected_language
        if detected_text:
            tts = gTTS(text=detected_text, lang=detected_language, slow=False)
            audio_file = "detected_text.mp3"
            tts.save(audio_file)
            os.system(f"start {audio_file}")  # On Windows, this will open the audio file.

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




# Function to import font files
def import_font():
    font_path = filedialog.askopenfilename(filetypes=[("TrueType Fonts", "*.ttf")])
    if font_path:
        shutil.copy(font_path, './training_data/fonts/')
        messagebox.showinfo("Font Imported", "Font imported successfully!")


# GUI setup
app = customtkinter.CTk()
app.title("OCR Application")
app.geometry("800x600")

# Login Frame
login_frame = customtkinter.CTkFrame(app)
login_frame.pack(pady=20)

# Username and password fields
username_label = customtkinter.CTkLabel(login_frame, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5)

username_entry = customtkinter.CTkEntry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = customtkinter.CTkLabel(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5)

password_entry = customtkinter.CTkEntry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Buttons for Sign Up and Login
login_button = customtkinter.CTkButton(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.grid(row=2, column=1, padx=10, pady=10)

signup_button = customtkinter.CTkButton(login_frame, text="Sign Up", command=lambda: sign_up(username_entry.get(), password_entry.get()))
signup_button.grid(row=3, column=1, padx=10, pady=10)


app.geometry("600x400")
app.title("Blindvison")
app.iconbitmap("eye.ico")

app.mainloop()
