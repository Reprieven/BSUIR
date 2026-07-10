import cv2
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, ttk

class StereoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Стереоскопический генератор")
        
        self.left_image = None
        self.right_image = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.btn_left = tk.Button(self.root, text="Загрузить левое изображение", command=self.load_left_image)
        self.btn_left.pack(pady=5)
        
        self.btn_right = tk.Button(self.root, text="Загрузить правое изображение", command=self.load_right_image)
        self.btn_right.pack(pady=5)

        self.method_var = tk.StringVar(value="anaglyph")
        methods = [("Анаглиф (красно-синий)", "anaglyph"),
                  ("Разделение (вертикальное)", "side_by_side"),
                  ("Стереопара (параллельная)", "parallel")]
        
        for text, mode in methods:
            tk.Radiobutton(self.root, text=text, variable=self.method_var, value=mode).pack()

        self.scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Смещение")
        self.scale.set(50)
        self.scale.pack()
        self.btn_process = tk.Button(self.root, text="Сгенерировать стереоизображение", command=self.process_image)
        self.btn_process.pack(pady=10)
    def load_left_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if path:
            self.left_image = cv2.imread(path)
            self.btn_left.config(text=f"Левое: {path.split('/')[-1]}")

    def load_right_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if path:
            self.right_image = cv2.imread(path)
            self.btn_right.config(text=f"Правое: {path.split('/')[-1]}")

    def process_image(self):
        if self.left_image is None or self.right_image is None:
            return
            
        method = self.method_var.get()
        if method == "anaglyph":
            result = self.create_anaglyph()
        elif method == "side_by_side":
            result = self.create_side_by_side()
        elif method == "parallel":
            result = self.create_parallel()

        cv2.imwrite("result.jpg", result)
        self.show_image(result)

    def create_anaglyph(self):
        h, w = min(self.left_image.shape[0], self.right_image.shape[0]), \
               min(self.left_image.shape[1], self.right_image.shape[1])
        left = cv2.resize(self.left_image, (w, h))
        right = cv2.resize(self.right_image, (w, h))
        anaglyph = left.copy()
        anaglyph[:, :, 0] = right[:, :, 0] 
        anaglyph[:, :, 2] = left[:, :, 2]   
        return anaglyph

    def create_side_by_side(self):
        h, w = min(self.left_image.shape[0], self.right_image.shape[0]), \
               min(self.left_image.shape[1], self.right_image.shape[1])
        left = cv2.resize(self.left_image, (w, h))
        right = cv2.resize(self.right_image, (w, h))
        sbs = np.vstack((left, right))
        return sbs

    def create_parallel(self):
        h, w = min(self.left_image.shape[0], self.right_image.shape[0]), \
               min(self.left_image.shape[1], self.right_image.shape[1])
        left = cv2.resize(self.left_image, (w, h))
        right = cv2.resize(self.right_image, (w, h))
        parallel = np.hstack((left, right))
        return parallel

    def show_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        pil_image.thumbnail((400, 400))
        tk_image = tk.PhotoImage(image=pil_image)
        
        self.result_label.config(image=tk_image, text="")
        self.result_label.image = tk_image

if __name__ == "__main__":
    root = tk.Tk()
    app = StereoApp(root)
    root.mainloop()