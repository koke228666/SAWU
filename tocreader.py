import struct

#file path
tocpath = 'Resource.toc'

with open(tocpath, 'rb') as file:
    #reading first 8 bytes
    data = file.read(8)
    if len(data) < 8:
        raise ValueError("bruuuuh")
    
    #extracting Resource*.pak and packed files count
    pcnt = int.from_bytes(data[0:4], byteorder='little')
    flcnt = int.from_bytes(data[4:8], byteorder='little')
    
    print(f'Packs count: {pcnt}')
    print(f'Files in packs count: {flcnt}')
