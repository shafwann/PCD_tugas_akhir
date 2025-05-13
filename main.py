import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self):
        self.image_input = None
        self.image_gray = None
        self.image_tres = None
        
        # GUI Setup
        self.root = tk.Tk()
        self.root.title("Digital Image Transformation")
        
        # Create frames
        self.frame_left = tk.Frame(self.root)
        self.frame_left.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Buttons
        self.btn_load = tk.Button(self.frame_left, text="Load Image", command=self.load_image)
        self.btn_load.pack(pady=5)
        
        self.btn_save = tk.Button(self.frame_left, text="Save Image", command=self.save_image)
        self.btn_save.pack(pady=5)
        
        # Slider for threshold
        self.threshold = tk.Scale(self.frame_left, from_=0, to=255, orient=tk.HORIZONTAL, 
                                 command=self.update_threshold)
        self.threshold.set(127)
        self.threshold.pack(pady=5)
        
        # Image displays
        self.images_frame = tk.Frame(self.frame_right)
        self.images_frame.pack(pady=5)

        # Container untuk Original Image
        self.original_frame = tk.Frame(self.images_frame)
        self.original_frame.pack(side=tk.LEFT, padx=10)

        self.original_title = tk.Label(self.original_frame, text="Original Image", justify='center')
        self.original_title.pack(anchor='center')
        self.label_original = tk.Label(self.original_frame)
        self.label_original.pack()

        # Container untuk Grayscale Image
        self.grayscale_frame = tk.Frame(self.images_frame)
        self.grayscale_frame.pack(side=tk.LEFT, padx=10)

        self.grayscale_title = tk.Label(self.grayscale_frame, text="Grayscale Image", justify='center')
        self.grayscale_title.pack(anchor='center')
        self.label_grayscale = tk.Label(self.grayscale_frame)
        self.label_grayscale.pack()

        # Container untuk Thresholded Image
        self.threshold_frame = tk.Frame(self.frame_right)
        self.threshold_frame.pack(pady=5)

        self.threshold_title = tk.Label(self.threshold_frame, text="Thresholded Image", justify='center')
        self.threshold_title.pack(anchor='center')
        self.label_threshold = tk.Label(self.threshold_frame)
        self.label_threshold.pack() 
        
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_input = cv2.imread(file_path)
            self.show_image(self.image_input, self.label_original, "Original Image")
            
            # Convert to grayscale
            self.image_gray = cv2.cvtColor(self.image_input, cv2.COLOR_BGR2GRAY)
            self.show_image(self.image_gray, self.label_grayscale, "Grayscale Image", grayscale=True)
            
            # Apply initial threshold
            self.update_threshold()
    
    def update_threshold(self, val=None):
        if self.image_gray is not None:
            _, thresh = cv2.threshold(self.image_gray, self.threshold.get(), 255, cv2.THRESH_BINARY)
            self.image_tres = cv2.bitwise_not(thresh)  # Invert image
            self.show_image(self.image_tres, self.label_threshold, "Thresholded Image", grayscale=True)
    
    def save_image(self):
        if self.image_tres is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if file_path:
                cv2.imwrite(file_path, self.image_tres)
                tk.messagebox.showinfo("Information", "Image saved successfully!")
    
    def show_image(self, image, label, title="", grayscale=False):
        if grayscale:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) if len(image.shape) == 2 else image
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        
        label.configure(image=image)
        label.image = image
        label.configure(text=title)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    processor = ImageProcessor()
    processor.run()