from SAWU import *
import tkinter as tk

"""
ОСТОРОЖНО!!! ГОВНОКОД!!!
"""
def preview_image(image):
    root = tk.Tk()
    root.title("Image viewer")
    image_tk = ImageTk.PhotoImage(image)
    label = tk.Label(root, image=image_tk)
    label.pack()
    root.mainloop()

def preview_file(file_data):
    file_content = read_resource(file_data['offset'], file_data['sizepkg'], file_data['archnum'], os.path.dirname(tocpath))
    if file_data['ftid'] == 1:
        try:
            print('previewing DDS...')
            preview_image(unpack_txt(read_resource(offset, length, paknum, os.path.dirname(tocpath))))
        except Exception as e:
            print(f'Error previewing DDS: {str(e)}')
    elif file_data['ftid'] == 3:
        print('WAV file detected. Playing...')
        preview_wave(file_content)
    else:
        print('Sorry. Only unpacking available for this file.')

def export_dot_res(f, resource_id, resource_path):
    f.seek(0)
    toc_content = f.read()
    for i in range(0, len(toc_content) - 4 + 1, 1):
        number = struct.unpack_from('<I', toc_content, i)[0]
        if number == resource_id:

            resource_data_offset = i
            f.seek(i)
            resourceid = struct.unpack("<I", f.read(4))[0] #resource id used in Scripts4.pak
            filesinr = struct.unpack("<I", f.read(4))[0] #files in resource
            with open(resource_path, 'wb') as resource_file:
                resource_file.write(struct.pack("<I", resourceid))
                resource_file.write(struct.pack("<I", filesinr))

                for i in range(filesinr): #file (not resource) block's size is 52 (4 bytes*13 attributes)
                    ftid = struct.unpack("<I", f.read(4))[0] #file type ID (check toc specs)
                    fnum = struct.unpack("<I", f.read(4))[0] #file num in resource
                    archnum = struct.unpack("<I", f.read(4))[0] #archive num
                    sizeunp = struct.unpack("<I", f.read(4))[0] #size to unpack
                    sizepkg = struct.unpack("<I", f.read(4))[0] #size packed
                    offset = struct.unpack("<I", f.read(4))[0] #offset
                    ftype = struct.unpack("<I", f.read(4))[0] #idk 0-2
                    attr1 = struct.unpack("<I", f.read(4))[0] #for dds: width, for wav: channels
                    attr2 = struct.unpack("<I", f.read(4))[0] #for dds: height, for wav: frequency
                    attr3 = struct.unpack("<I", f.read(4))[0] #for dds: real width(?), for wav: bits
                    attr4 = struct.unpack("<I", f.read(4))[0] #for dds: real height(?), for wav: ?
                    attr5 = struct.unpack("<I", f.read(4))[0] #0 on all other, 1 on dds
                    attr6 = struct.unpack("<I", f.read(4))[0] #for dds: nothing, for wav: ?
                    
                    #writing
                    resource_file.write(struct.pack("<I", ftid))
                    resource_file.write(struct.pack("<I", fnum))
                    resource_file.write(struct.pack("<I", archnum))
                    resource_file.write(struct.pack("<I", sizeunp))
                    resource_file.write(struct.pack("<I", sizepkg))
                    resource_file.write(struct.pack("<I", offset))
                    resource_file.write(struct.pack("<I", ftype))
                    resource_file.write(struct.pack("<I", attr1))
                    resource_file.write(struct.pack("<I", attr2))
                    resource_file.write(struct.pack("<I", attr3))
                    resource_file.write(struct.pack("<I", attr4))
                    resource_file.write(struct.pack("<I", attr5))
                    resource_file.write(struct.pack("<I", attr6))
            return 'FOUND'

tocpath = input('Enter path to Resource.toc (e.g. C:\AnotherWorld\Data\Resource.toc): ')
try:
    f = open(tocpath, 'rb')
except Exception as e:
    print(e.args)
    sys.exit(1)
print('File loaded.')


while True:
    f = open(tocpath, 'rb')
    resid = int(input('enter resid: '))
    resource_data = json.loads(read_partially(f, resid))
    filenum = 0
    if not os.path.exists(f'{resid}'):
        os.makedirs(f'{resid}')
    if not os.path.exists(f'{resid}//res'):
        os.makedirs(f'{resid}//res')
    for file in resource_data['files']:
        filetype = resource_data['files'][filenum]['ftid']
        offset = resource_data['files'][filenum]['offset']
        length = resource_data['files'][filenum]['sizepkg']
        paknum = resource_data['files'][filenum]['archnum']
        intfid = resource_data['files'][filenum]['fnum']
        try:
            #preview_file(file)
            save_file(file, f'{resid}//res//{intfid}.dds', os.path.dirname(tocpath), True)
        except:
            save_file(file, f'{resid}//res//{intfid}.dds', os.path.dirname(tocpath), False)
        filenum += 1
    export_dot_res(f, resid, os.path.join(str(resid), 'resource.bin'))
