import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def equalizeLookUpTable(X):
    histogram, bins = np.histogram(X, bins=256, range=(0, 256))
    cs = histogram.cumsum()
    cs_normalized = cs * 255 / cs[-1]
    lookup_table = np.round(cs_normalized).astype('uint8')
    
    return lookup_table


def match(X, Z):
    equalized_X = equalizeLookUpTable(X)
    equalized_Z = equalizeLookUpTable(Z)
    mapping = np.zeros(256, dtype=np.uint8)

    for i in range(256):
        j = 0
        while equalized_Z[j] < equalized_X[i]:
            j += 1
        mapping[i] = j

    matched_image = mapping[X]

    return matched_image


def load_image():
    global input_image
    file_path = filedialog.askopenfilename()
    if file_path:
        input_image = cv2.imread(file_path, 0)
        messagebox.showinfo("OnlineConverter", "success")
    else:
        messagebox.showinfo("OnlineConverter", "No image")

def equalize_image():
    global input_image
    if input_image is not None:
        equalized = equalizeLookUpTable(input_image)
        equalized= equalized[input_image]
        cv2.imwrite('equalized_image.jpg', equalized)
        messagebox.showinfo("OnlineConverter", "Histogram equalization completed and saved as equalized_image.jpg")
    else:
        messagebox.showerror("OnlineConverterError", "No image loaded.")

def match_histogram():
    global input_image
    if input_image is not None:
        reference_path = filedialog.askopenfilename()
        if reference_path:
            reference_image = cv2.imread(reference_path, 0)
            matched = match(input_image, reference_image)
            cv2.imwrite('matched_image.jpg', matched)
            messagebox.showinfo("Info", "Histogram matching completed and saved as matched_image.jpg")
        else:
            messagebox.showinfo("Info", "No reference image")
    else:
        messagebox.showerror("Error", "No image")


root = tk.Tk()
root.title("Image Processing GUI")


window_width = 400
window_height = 250
root.geometry(f"{window_width}x{window_height}")

input_image = None


button_frame = tk.Frame(root)
button_frame.pack(pady=20)

load_button = tk.Button(button_frame, text="Load Image", command=load_image)
equalize_button = tk.Button(button_frame, text="Equalize Histogram", command=equalize_image)
match_button = tk.Button(button_frame, text="Match Histogram", command=match_histogram)


load_button.pack(pady=15)
equalize_button.pack(pady=15)
match_button.pack(pady=15)

root.mainloop()