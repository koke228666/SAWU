import os, sys, struct, time, io, json
import tkinter as tk
from PIL import Image, ImageTk
from SAWU import *
import simpleaudio as sa
import wave
#init folder for extracted resource data
if not os.path.exists("ResourceData"):
    print("ResourceData doesn't exist, creating...")
    os.makedirs("ResourceData")
    print('ResourceData created')



tocpath = input('Enter path to Resource.toc (e.g. C:\AnotherWorld\Data\Resource.toc): ')
try:
    f = open(tocpath, 'rb')
except Exception as e:
    print(e.args)
    sys.exit(1)
print('File loaded.')

while True:
    f = open(tocpath, 'rb')
    selection = input('1. Parse Resource.toc to human-readable format\n2. Parse Resource.toc to json (TAKES A LONG TIME)\n3. Save Resource Data block.\n4. Preview resource\n5. Exit\n\nPlease select one: ')
    if selection.isdigit():
        selection = int(selection)
    else:
        print('\nEnter a number')
        selection = input('1. Export Resource.toc to human-readable format\n2. Export Resource.toc to json (TAKES A LONG TIME)\n3. Save Resource Data block.\n4. Preview resource\n5. Exit\n\nPlease select one: ')

    if selection == 1:
        ExportToLog(f)
    elif selection == 2:
        ExportToJson(f)
    elif selection == 3:
        resourceid = int(input('Enter Resource ID for extract: '))
        if export_dot_res(f, resourceid) == 'FOUND':
            print(f'Successfully extracted to ResourceData\{resourceid}.res')
        else:
            print(f'Not found! Enter something like 4179940073. Can be found in {logpath} or in Scripts4.pak')
    elif selection == 4:
        # filetype = 'DDS(1)'
        # offset = 16505344
        # length = 11166
        # paknum = 5
        resourceid = input('Enter id of resource (you can get it in one of exports): ')
        if resourceid.isdigit():
            resourceid = int(resourceid)
            resource_data = json.loads(read_partially(f, resourceid))
            ftotal = int(resource_data['filescnt'])
            filenum = input(f'Enter id of file (0-{ftotal-1}): ')
            if filenum.isdigit():
                filenum = int(filenum)
                filetype = resource_data['files'][filenum]['ftid']
                offset = resource_data['files'][filenum]['offset']
                length = resource_data['files'][filenum]['sizepkg']
                paknum = resource_data['files'][filenum]['archnum']
                intfid = resource_data['files'][filenum]['fnum']
                print('\nPreviewing resource...')
                print(f'File type: {filetype}')
                print(f'Offset: {offset}')
                print(f'Length: {length}')
                print(f'Packed in: Resource{paknum}.pak')
                print(f'Internal file id: {intfid}')
                if filetype == 3:
                    wave_file = read_resource(offset, length, paknum, os.path.dirname(tocpath))
                    wave_file.seek(0)
                    wave_file.write(b'\x52\x49\x46\x46')
                    wave_file.seek(0)
                    wave_file = wave.open(wave_file)
                    wave_obj = sa.WaveObject.from_wave_read(wave_file)
                    play_obj = wave_obj.play()
                    play_obj.wait_done()
                    print('Previewing done.')
                elif filetype == 1:
                    try:
                        preview_image(unpack_txt(read_resource(offset, length, paknum, os.path.dirname(tocpath))))
                    except:
                        print('Unpacking DDS currently unsupported for this game.')
                    print('Previewing done.')
                else:
                    print('Unknown file.')
            else:
                print('\nEnter a number')
        else:
            print('\nEnter a number')
        
    else:
        sys.exit(0)

