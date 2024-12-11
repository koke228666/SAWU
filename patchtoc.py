import struct, os

def patch_toc(folder, toc, pakscnt):
    with open(folder+r'\resource.bin', 'rb') as resource_file:
        resid = resource_file.read(4)
        resource_int32 = struct.unpack('<I', resid)[0]

    with open(toc, 'r+b') as toc:
        toc_content = toc.read()
        toc_bytes = bytearray(toc_content)
        search_index = toc_bytes.find(struct.pack('<I', resource_int32))
        toc.seek(search_index)
        with open(folder+r'\resource.bin', 'rb') as resource_file:
            resource_data = resource_file.read()
        toc.write(resource_data)
        toc.seek(0)
        toc.write(struct.pack('<I', int(pakscnt)))

if __name__ == '__main__':
    patch_toc(input('Enter folder name with AWMod: '), input('Enter path to Resource.toc: '), input('Enter paks count (use latest pak ID): '))