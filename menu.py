import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import threading
import cv2

from functions.virtual_mouse import virtual_mouse
from menu_fct import *


# Dictionary to track currently used cameras
cameras_in_use = {}

def start_virtual_mouse():
    root = tk.Toplevel()
    app_theme(root)
    root.withdraw()  
    
    num_cam = simpledialog.askinteger("Cam Info", "Enter the camera number")
    width_cam = simpledialog.askinteger("Width Cam", "Enter the camera width")
    height_cam = simpledialog.askinteger("Height Cam", "Enter the camera height")
    fps = messagebox.askquestion("FPS", "Show FPS ?")
    if fps == 'yes':
        fps = True
    else: 
        fps = False

    # Check if user has entered essential parameters
    if num_cam is not None and width_cam is not None and height_cam is not None:
        # Check if the camera is already in use
        if num_cam in cameras_in_use:
            messagebox.showinfo("Info", "The camera is already in use.")
            return

        # Mark the camera as in use
        cameras_in_use[num_cam] = True

        # Start the virtual_mouse function in a new thread
        threading.Thread(target=virtual_mouse, args=(num_cam, width_cam, height_cam, fps)).start()
    else:
        messagebox.showerror("Error", "Please enter all essential parameters.")
    
def info_cam():
    root = tk.Toplevel()
    app_theme(root)
    root.withdraw()  
    
    num_cam = simpledialog.askinteger("Cam", "Enter camera number")
    # Open video capture from camera
    cap = cv2.VideoCapture(num_cam)

    # Check if video capture is open
    if not cap.isOpened():
        messagebox.showerror("Error", "Unable to open video capture.")
    else:
        # Get width and height of video capture
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        messagebox.showinfo("Video information", f"Video width: {width}\nVideo height: {height}")

        # Release video capture
        cap.release()
    
root = tk.Tk()
root.title("Virtualis")

# Center the window and set its size
center_window(root, width=220, height=200)

# Set the background color to dark gray
root.configure(bg='#333333')

# Load the image with PIL and resize it
image = Image.open("ressources/virtual_mouse_logo.png")
image = image.resize((65, 65), Image.LANCZOS)
image = ImageTk.PhotoImage(image)

# Create a label with the image
image_label = tk.Label(root, image=image, bg='#333333')
image_label.pack()

# Create a style for the buttons
style = ttk.Style()
style.configure('TButton', font=('Inter', 14))

# Create two modern and design buttons using ttk
button1 = ttk.Button(root, text="Virtual Mouse", command=start_virtual_mouse, style='TButton')
button2 = ttk.Button(root, text="Cam Info", command=info_cam, style='TButton')

# Position the buttons in the middle of the window with a small padding
button1.pack(padx=20, pady=11)
button2.pack(padx=20, pady=11)

root.mainloop()