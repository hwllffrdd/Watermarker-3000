from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk, ImageDraw, ImageFont

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


def add_text_watermark():
    if image_file_path:
        base_image = Image.open(image_file_path).convert("RGBA")
        text = watermark_text_entry.get()
        font = ImageFont.truetype("arial.ttf", 40)
        transparency = transparency_scale.get()
        text_color = (255, 255, 255, int(255 * (transparency / 100)))
        base_width, base_height = base_image.size
        large_dim = int((base_width**2 + base_height**2)**0.5) * 2
        text_layer = Image.new('RGBA', (large_dim, large_dim), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_layer)
        bbox = text_draw.textbbox((0, 0), text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        spacing = 50

        # Draw the text repeatedly on the large canvas, rotate and crop
        for x in range(0, large_dim, text_width + spacing):
            for y in range(0, large_dim, text_height + spacing):
                text_draw.text((x, y), text, font=font, fill=text_color)
        rotated_text_layer = text_layer.rotate(45, expand=1)
        left = (rotated_text_layer.width - base_width) // 2
        top = (rotated_text_layer.height - base_height) // 2
        right = left + base_width
        bottom = top + base_height
        cropped_text_layer = rotated_text_layer.crop((left, top, right, bottom))

        # Combine and convert
        combined = Image.alpha_composite(base_image, cropped_text_layer)
        rgb_combined = combined.convert("RGB")
        rgb_combined.save('text_watermarked_image.jpg')

        showinfo(
            title='Processing Complete',
            message='The image has been watermarked with text and saved as text_watermarked_image.jpg'
        )


# UI setup
window = Tk()
window.config(padx=100, pady=50, bg="#D6D1C5")
window.resizable(False, False)
window.title("Watermarker 3000")

app_image = Image.open("paper.jpg")
paper_img = ImageTk.PhotoImage(app_image)

watermk_label = Label(window, text="Watermarker 3000", fg="#006989", bg="#D6D1C5", font=("Verdana", 40, "bold"))
watermk_label.grid(column=0, row=0, columnspan=2)

canvas = Canvas(window, width=300, height=300, bg="#D6D1C5", highlightthickness=0)
canvas.create_image(150, 150, image=paper_img)
canvas.grid(column=0, row=1, columnspan=2)

button_style = {
    'bg': '#005C78',
    'fg': '#E88D67',
    'font': ('Verdana', 12, 'bold'),
    'activebackground': '#e57c51',
    'activeforeground': 'white',
    'bd': 0,
    'padx': 20,
    'pady': 10
}

open_image = Button(
    text='Open image to be watermarked',
    command=lambda: select_file("image to be watermarked"),
    **button_style
)
open_image.grid(column=0, row=2, padx=10, pady=20)

open_watermark = Button(
    text='Open image with watermark',
    command=lambda: select_file("watermark"),
    **button_style
)
open_watermark.grid(column=1, row=2, padx=10, pady=20)

style = ttk.Style(window)
style.configure('TScale', background='#D6D1C5', foreground='#005C78', troughcolor='#E88D67', sliderthickness=25, bordercolor='#E88D67')

watermark_text_label = Label(window, text="Watermark Text: ", bg="#D6D1C5", fg="#005C78", font=("Verdana", 12, "bold"))
watermark_text_label.grid(column=0, row=3)
watermark_text_entry = Entry(window, width=30)
watermark_text_entry.grid(column=0, row=4)

transparency_label = Label(window, text="Watermark transparency:", bg="#D6D1C5", fg="#005C78", font=("Verdana", 12, "bold"))
transparency_label.grid(column=1, row=3)

transparency_scale = Scale(window, from_=0, to=100, orient=HORIZONTAL,
                           bg="#D6D1C5", fg="#005C78", troughcolor='#E88D67', highlightthickness=0)
transparency_scale.set(40)
transparency_scale.grid(column=1, row=4)

process_button = Button(
    text='Watermark with image',
    command=process_files,
    **button_style
)
process_button.grid(column=0, row=5, pady=20)

text_watermark_button = Button(
    text='Watermark with text',
    command=add_text_watermark,
    **button_style
)
text_watermark_button.grid(column=1, row=5, pady=20)

window.mainloop()
