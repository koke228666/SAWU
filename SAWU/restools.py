import os, sys, struct, time, io, json, wave, pickle
import simpleaudio as sa
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

def preview_wave(f):
    wave_file = f
    wave_file.seek(0)
    wave_file.write(b'\x52\x49\x46\x46')
    wave_file.seek(0)
    wave_file = wave.open(wave_file)
    wave_obj = sa.WaveObject.from_wave_read(wave_file)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def save_file(fdata, fpath, toc_dir, compressed):
    if fdata['ftid'] == 1:
        filetype = fpath+'.dds'
    elif fdata['ftid'] == 3:
        filetype = fpath+'.wav'
    else:
        fpath = fpath+'.bin'
    if fdata['ftid'] == 1:
        if compressed:
            unpack_txt(read_resource(fdata['offset'], fdata['sizepkg'], fdata['archnum'], toc_dir)).save(fpath)
        else:
            Image.open(read_resource(fdata['offset'], fdata['sizepkg'], fdata['archnum'], toc_dir)).save(fpath)
    elif fdata['ftid'] == 3:
        with open(fpath, 'wb') as f:
            wave_file = read_resource(fdata['offset'], fdata['sizepkg'], fdata['archnum'], toc_dir)
            wave_file.seek(0)
            wave_file.write(b'\x52\x49\x46\x46')
            wave_file.seek(0)
            f.write(wave_file.getbuffer().tobytes())
    else:
        with open(fpath, 'wb') as f:
            f.write(read_resource(fdata['offset'], fdata['sizepkg'], fdata['archnum'], toc_dir).getbuffer().tobytes())