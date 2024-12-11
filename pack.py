import os
import struct
from typing import List, Tuple

def make_toc_patch(resource_path):
    with open(os.path.join(resource_path, 'resource.bin'), 'rb+') as resource_file:
        resource_file.read(4)
        filesinr = struct.unpack("<I", resource_file.read(4))[0]
        archive = int(input('Enter archive ID (31 for first mod): '))
        files = makepak(os.path.join(resource_path, 'res'), archive)
        for name, size, offset in files:
            #print(name)
            #print(size)
            #print(offset)
            resource_file.read(4)
            resource_file.read(4)
            resource_file.write(struct.pack("<I", archive))
            resource_file.write(struct.pack("<I", size))
            resource_file.write(struct.pack("<I", size))
            resource_file.write(struct.pack("<I", offset))
            resource_file.read(4)
            resource_file.read(4)
            resource_file.read(4)
            resource_file.read(4)
            resource_file.read(4)
            resource_file.read(4)
            resource_file.read(4)

def makepak(folder_path: str, archive) -> List[Tuple[str, int, int]]:
    with open(os.path.join(folder_path, '..', f'Resource{archive}.pak'), 'wb') as f:
        file_info = []
        files = os.listdir(folder_path)
        files.sort()
        current_offset = 0
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                name_without_ext = os.path.splitext(file_name)[0]
                file_size = os.path.getsize(file_path)
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    f.write(file_data)
                file_info.append((name_without_ext, file_size, current_offset))
                current_offset += file_size
        return file_info

make_toc_patch(input('Enter folder name with AWMod: '))