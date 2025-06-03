
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1000x550")
window.configure(bg = "#2A2F4F")


canvas = Canvas(
    window,
    bg = "#2A2F4F",
    height = 550,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    72.0,
    fill="#E5BEEC",
    outline="")

canvas.create_text(
    85.0,
    20.0,
    anchor="nw",
    text="Damage Controller",
    fill="#000000",
    font=("Inter Bold", 30 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    53.0,
    35.0,
    image=image_image_1
)

canvas.create_rectangle(
    54.0,
    114.0,
    324.0,
    184.0,
    fill="#917FB3",
    outline="")

canvas.create_rectangle(
    54.0,
    205.0,
    324.0,
    515.0,
    fill="#917FB3",
    outline="")

canvas.create_rectangle(
    675.0,
    205.0,
    945.0,
    515.0,
    fill="#917FB3",
    outline="")

canvas.create_rectangle(
    365.0,
    205.0,
    635.0,
    515.0,
    fill="#5F4AB7",
    outline="")

canvas.create_text(
    125.0,
    132.0,
    anchor="nw",
    text="Quantidade de Veículos Afetados",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
)

canvas.create_text(
    127.0,
    146.0,
    anchor="nw",
    text="1",
    fill="#FFFFFF",
    font=("Inter Bold", 24 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    92.0,
    152.0,
    image=image_image_2
)

canvas.create_rectangle(
    365.0,
    114.0,
    635.0,
    184.0,
    fill="#917FB3",
    outline="")

canvas.create_text(
    436.0,
    132.0,
    anchor="nw",
    text="Quantidade de Peças Afetadas",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
)

canvas.create_text(
    438.0,
    146.0,
    anchor="nw",
    text="1",
    fill="#FFFFFF",
    font=("Inter Bold", 24 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    404.0,
    150.0,
    image=image_image_3
)

canvas.create_rectangle(
    675.0,
    114.0,
    945.0,
    184.0,
    fill="#917FB3",
    outline="")

canvas.create_text(
    746.0,
    132.0,
    anchor="nw",
    text="Média de Defeitos por Peça Afetada",
    fill="#FFFFFF",
    font=("Inter Bold", 10 * -1)
)

canvas.create_text(
    748.0,
    146.0,
    anchor="nw",
    text="1",
    fill="#FFFFFF",
    font=("Inter Bold", 24 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    714.0,
    149.0,
    image=image_image_4
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=376.0,
    y=26.0,
    width=117.0,
    height=25.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=507.0,
    y=26.0,
    width=117.0,
    height=25.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=773.0,
    y=47.0,
    width=107.0,
    height=25.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=880.0,
    y=47.0,
    width=120.0,
    height=25.0
)
window.resizable(False, False)
window.mainloop()
