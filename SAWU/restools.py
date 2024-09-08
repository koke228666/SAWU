import os, sys, struct, time, io, json
import tkinter as tk
from PIL import Image, ImageTk

def read_resource(offset, length, packnum, packpath):
    packpath = os.path.join(packpath, f'Resource{packnum}.pak')
    pack = open(packpath, 'rb')
    pack.seek(offset)
    data = io.BytesIO(pack.read(length))
    return data

def unpack_txt(data):
    temp = io.BytesIO()
    end_f = data.seek(0, 2)
    data.seek(0)
    breaks = data.read(1)
    image_format='RGBA'

    while data.tell() != end_f:
        byte = data.read(1)
        if byte == breaks:
            byte_repeat = data.read(1)
            if byte_repeat == breaks:
                temp.write(byte_repeat)
            else:
                byte_1 = data.read(1)[0]
                repeat = byte_1 & 0x7F if byte_1 > 0x80 else (byte_1 << 8) + data.read(1)[0]
                temp.write(byte_repeat * repeat)
        else:
            temp.write(byte)
    try:
        image = Image.open(temp)
    except:
        temp.seek(12)
        h, w = struct.unpack("<II", temp.read(8))
        temp.seek(128)
        image = Image.frombuffer(image_format, (w, h), temp.read(w * h * 4), 'raw', 'BGRA', 0, 1)

    return image

def preview_image(image):
    root = tk.Tk()
    root.title("Image viewer")

    image_tk = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=image_tk)
    label.pack()

    root.mainloop()

