import os, sys, struct, time, io, json
from .config import *
def ExportToLog(f):
    export = open('SAWU.txt', 'w')
    #read header of TOC
    packs = struct.unpack("<I",f.read(4))[0] #packs count
    resources = struct.unpack("<I",f.read(4))[0] #resources count
    #main log info
    export.write(f'--TOC reader config--\nShow file types with ids: {showftypes}\nReplace 4294967295 with 0: {fixcount}\n')
    export.write('--HEADER INFO BEGINS (counting from 1)--\n')
    export.write(f'Total packs: {packs}\nTotal resources: {resources}\n--MAIN TABLE BEGINS--\n')
    export.write('FTID FNUM ARCHNUM SIZEUNP SIZEPKG OFFSET FTYPE WDTH/CHS HGHT/FRQ WDTH/BIT HGHT/FRSTP ONE/ZRO UNK/SECP\n')
    for ii in range(resources):
        resourceid = struct.unpack("<I",f.read(4))[0] #resource id used in Scripts4.pak
        filesinr = struct.unpack("<I",f.read(4))[0] #files in resource
        export.write(f'--RESOURCE {ii} with ID {resourceid} and {filesinr} file(s) record(s) BEGINS--\n')
        for i in range(filesinr): #file (not resource) block's size is 52
            ftid = struct.unpack("<I",f.read(4))[0] #file type ID (check toc specs)
            fnum = struct.unpack("<I",f.read(4))[0] #file num in resource
            archnum = struct.unpack("<I",f.read(4))[0] #archive num
            sizeunp = struct.unpack("<I",f.read(4))[0] #size to unpack
            sizepkg = struct.unpack("<I",f.read(4))[0] #size packed
            offset = struct.unpack("<I",f.read(4))[0] #offset
            ftype = struct.unpack("<I",f.read(4))[0] #idk 0-2
            attr1 = struct.unpack("<I",f.read(4))[0] #for dds: width, for wav: channels
            attr2 = struct.unpack("<I",f.read(4))[0] #for dds: height, for wav: frequency
            attr3 = struct.unpack("<I",f.read(4))[0] #for dds: real width(?), for wav: bits
            attr4 = struct.unpack("<I",f.read(4))[0] #for dds: real height(?), for wav: ?
            attr5 = struct.unpack("<I",f.read(4))[0] #0 on all other, 1 on dds
            attr6 = struct.unpack("<I",f.read(4))[0] #for dds: nothing, for wav: ?
            #detect file type
            if ftid == 1:
                ftw = 'DDS'
            elif ftid == 3:
                ftw = 'WAV'
            elif ftid == 5:
                ftw = 'RGN'
            elif ftid == 6:
                ftw = 'PTH'
            elif ftid == 7:
                ftw = 'OGG'
            else:
                ftw = 'unknown'
            if showftypes == True:
                ftid = f'{ftw}({ftid})'
            else:
                ftid = f'{ftid}'
            if fnum == 4294967295:
                if fixcount:
                    fnum = 0
                    export.write(f'{ftid} {fnum} {archnum} {sizeunp} {sizepkg} {offset} {ftype} {attr1} {attr2} {attr3} {attr4} {attr5} {attr6} -- resource contains one file\n')
            else:
                export.write(f'{ftid} {fnum} {archnum} {sizeunp} {sizepkg} {offset} {ftype} {attr1} {attr2} {attr3} {attr4} {attr5} {attr6}\n')

def ExportToJson(f):
    #creates json file with size about 300MB!!!
    #read header of TOC
    packs = struct.unpack("<I",f.read(4))[0] #packs count
    resources = struct.unpack("<I",f.read(4))[0] #resources count
    toc_data = {
        "packs": packs,
        "resources": []
    }
    for ii in range(resources):
        resourceid = struct.unpack("<I",f.read(4))[0] #resource id used in Scripts4.pak
        filesinr = struct.unpack("<I",f.read(4))[0] #files in resource
        resource_data = {
            "resource_id": resourceid,
            "filescnt": filesinr,
            "files": []
        }
        for i in range(filesinr): #file (not resource) block's size is 52
            ftid = struct.unpack("<I",f.read(4))[0] #file type ID (check toc specs)
            fnum = struct.unpack("<I",f.read(4))[0] #file num in resource
            archnum = struct.unpack("<I",f.read(4))[0] #archive num
            sizeunp = struct.unpack("<I",f.read(4))[0] #size to unpack
            sizepkg = struct.unpack("<I",f.read(4))[0] #size packed
            offset = struct.unpack("<I",f.read(4))[0] #offset
            ftype = struct.unpack("<I",f.read(4))[0] #idk 0-2
            attr1 = struct.unpack("<I",f.read(4))[0] #for dds: width, for wav: channels
            attr2 = struct.unpack("<I",f.read(4))[0] #for dds: height, for wav: frequency
            attr3 = struct.unpack("<I",f.read(4))[0] #for dds: real width(?), for wav: bits
            attr4 = struct.unpack("<I",f.read(4))[0] #for dds: real height(?), for wav: ?
            attr5 = struct.unpack("<I",f.read(4))[0] #0 on all other, 1 on dds
            attr6 = struct.unpack("<I",f.read(4))[0] #for dds: nothing, for wav: ?
            #detect file type
            if ftid == 1:
                ftw = 'DDS'
            elif ftid == 3:
                ftw = 'WAV'
            elif ftid == 5:
                ftw = 'RGN'
            elif ftid == 6:
                ftw = 'PTH'
            elif ftid == 7:
                ftw = 'OGG'
            else:
                ftw = 'unknown'
            if showftypes == True:
                ftid = f'{ftw}({ftid})'
            else:
                ftid = f'{ftid}'
            if fnum == 4294967295 and fixcount:
                fnum = 0
            file_data = {
                "ftid": ftid,
                "fnum": fnum,
                "archnum": archnum,
               "sizeunp": sizeunp,
                "sizepkg": sizepkg,
                "offset": offset,
                "ftype": ftype,
                "attr1": attr1,
                "attr2": attr2,
                "attr3": attr3,
                "attr4": attr4,
                "attr5": attr5,
                "attr6": attr6
                }
            resource_data["files"].append(file_data)
            toc_data["resources"].append(resource_data)
    with open('SAWU.json', 'w') as jsonf:
        json.dump(toc_data, jsonf, indent=4)

def export_dot_res(f, resource_id):
    toc_content = f.read()

    for i in range(0, len(toc_content) - 4 + 1, 1):
        number = struct.unpack_from('<I', toc_content, i)[0]

        if number == resource_id:
            resource_data_offset = i
            f.seek(i)
            resourceid = struct.unpack("<I", f.read(4))[0] #resource id used in Scripts4.pak
            filesinr = struct.unpack("<I", f.read(4))[0] #files in resource
            resource_path = os.path.join('ResourceData', f'{resourceid}.res') #create file to write
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

def read_partially(f, resource_id):
    f.seek(0)
    toc_content = f.read()
    for i in range(0, len(toc_content) - 4 + 1, 1):
        number = struct.unpack_from('<I', toc_content, i)[0]
        if number == resource_id:
            f.seek(i)
            resourceid = struct.unpack("<I", f.read(4))[0]  # resource id used in Scripts4.pak
            filesinr = struct.unpack("<I", f.read(4))[0]  # files in resource
            resource_data = {
                "resource_id": resourceid,
                "filescnt": filesinr,
                "files": []
            }
            for j in range(filesinr): #file (not resource) block's size is 52 (4 bytes * 13 attributes)
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
                if fnum == 4294967295:
                    fnum = 0
                file_data = {
                    "ftid": ftid,
                    "fnum": fnum,
                    "archnum": archnum,
                    "sizepkg": sizepkg,
                    "offset": offset,
                }
                resource_data["files"].append(file_data)
            return json.dumps(resource_data)