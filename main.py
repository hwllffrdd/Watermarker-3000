from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

# Global variables to store file paths
image_file_path = None
watermark_file_path = None


def select_file(file_type):
    global image_file_path, watermark_file_path

    filetypes = (
        ('JPEG files', '*.jpg'),
        ('PNG files', '*.png'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if filename:
        showinfo(
            title=f'Selected {file_type} File',
            message=filename
        )

        if file_type == "image to be watermarked":
            image_file_path = filename
        elif file_type == "watermark":
            watermark_file_path = filename


# Create the main window
window = Tk()
window.config(padx=100, pady=50, bg="#D6D1C5")
window.resizable(False, False)
window.title("Watermarker 3000")

# Load the initial image using Pillow
app_image = Image.open("paper.jpg")
paper_img = ImageTk.PhotoImage(app_image)

# Title label
watermk_label = Label(window, text="Watermarker 3000", fg="#006989", bg="#D6D1C5", font=("Verdana", 40, "bold"))
watermk_label.grid(column=0, row=0, columnspan=3)  # Span across 3 columns

# Canvas for image display
canvas = Canvas(window, width=300, height=300, bg="#D6D1C5", highlightthickness=0)
canvas.create_image(150, 150, image=paper_img)  # Center the image
canvas.grid(column=0, row=1, columnspan=3)  # Span across 3 columns

# Customize the button appearance
button_style = {
    'bg': '#E88D67',
    'fg': '#005C78',
    'font': ('Verdana', 12, 'bold'),
    'activebackground': '#e57c51',
    'activeforeground': 'white',
    'bd': 0,
    'padx': 20,
    'pady': 10
}

# Open image button
open_image = Button(
    text='Open image to be watermarked',
    command=lambda: select_file("image to be watermarked"),
    **button_style
)
open_image.grid(column=0, row=2, padx=10, pady=20)

# Open watermark button
open_watermark = Button(
    text='Open image with watermark',
    command=lambda: select_file("watermark"),
    **button_style
)
open_watermark.grid(column=2, row=2, padx=10, pady=20)

style = ttk.Style(window)
style.configure('TScale', background='#D6D1C5', foreground='#005C78', troughcolor='#E88D67', sliderthickness=25, bordercolor='#E88D67')

transparency_scale = ttk.Scale(window, from_=0, to=100, orient=HORIZONTAL, style='TScale')
transparency_scale.set(40)
transparency_scale.grid(column=1, row=3, pady=20)

def process_files():
    if image_file_path and watermark_file_path:
        base_image = Image.open(image_file_path).convert("RGBA")
        watermark_image = Image.open(watermark_file_path).convert("RGBA")
        base_width, base_height = base_image.size
        max_size = min(base_width, base_height)
        watermark = watermark_image.resize((max_size, max_size), Image.Resampling.LANCZOS)
        x = (base_width - max_size) // 2
        y = (base_height - max_size) // 2
        position = (x, y)
        combined = Image.new("RGBA", base_image.size)
        combined.paste(base_image, (0, 0))
        transparency = transparency_scale.get()
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: p * (transparency / 100))
        combined.paste(watermark, position, mask=alpha)
        rgb_combined = combined.convert("RGB")
        rgb_combined.save('watermarked_image.jpg')
        showinfo(
            title='Processing Complete',
            message='The image has been watermarked and saved as watermarked_image.jpg'
        )

process_button = Button(
    text='Watermark!',
    command=process_files,
    **button_style
)
process_button.grid(column=1, row=4, pady=20)

window.mainloop()
