import os

# --------------------------------
# fucking shitty code starts here
# --------------------------------

def parse_pak_file(file_path):
    if file_path == '':
        print('nope')
        exit()
    #DDS_HEADER = b'DDS'
    WAV_HEADER = b'WAVE'
    
    file_name = os.path.basename(file_path)
    file_name = os.path.splitext(file_name)[0]

    if not os.path.exists(f'{file_name}'):
        os.makedirs(f'{file_name}')
    if not os.path.exists(f'{file_name}/WAV'):
        os.makedirs(f'{file_name}/WAV')
    #if not os.path.exists(f'{file_name}/DDS'):
    #    os.makedirs(f'{file_name}/DDS')

    with open(file_path, 'rb') as file:
        index = 0
        #DDSes = 0
        WAVes = 0
        current_chunk = b''
        
        # reading file by blocks
        while True:
            block = file.read(5242880)
            if not block:
                break

            current_chunk += block

            while True:
                #dds_index = current_chunk.find(DDS_HEADER)
                wav_index = current_chunk.find(WAV_HEADER)
                
                #if dds_index == -1 and wav_index == -1:
                if wav_index == -1:
                    break

                # if dds_index != -1 and (wav_index == -1 or dds_index < wav_index):
                    # print(f'Found DDS! index: {dds_index}')
                    # DDSes += 1
                    # with open(os.path.join(f'{file_name}/DDS', f'{DDSes}.dds'), 'wb') as dds_file:
                        # dds_file.write(current_chunk[:dds_index])
                    # current_chunk = current_chunk[dds_index + len(DDS_HEADER):]
                # elif wav_index != -1 and (dds_index == -1 or wav_index < dds_index):
                    # print(f'Found WAV file! index: {wav_index}')
                    # WAVes += 1
                    # with open(os.path.join(f'{file_name}/WAV', f'{WAVes}.wav'), 'wb') as wav_file:
                        # wav_file.write(b'\x52\x49\x46\x46') # original files won't have RIFF header
                        # wav_file.write(current_chunk[wav_index-4:])
                    # current_chunk = current_chunk[wav_index + len(WAV_HEADER):]
                if wav_index != -1:
                    print(f'Found WAV file! index: {wav_index}')
                    WAVes += 1
                    with open(os.path.join(f'{file_name}/WAV', f'{WAVes}.wav'), 'wb') as wav_file:
                        wav_file.write(b'\x52\x49\x46\x46') # original files won't have RIFF header
                        wav_file.write(current_chunk[wav_index-4:])
                    current_chunk = current_chunk[wav_index + len(WAV_HEADER):]

                index += len(block)  # next block

        if len(current_chunk) > 0:
            if current_chunk.startswith(WAV_HEADER):
                print(f'Found WAV file! index: {index}')
                WAVes += 1
                with open(os.path.join(f'{file_name}/WAV', f'{WAVes}.wav'), 'wb') as wav_file:
                    wav_file.write(b'\x52\x49\x46\x46')
                    wav_file.write(current_chunk-4)
            # elif current_chunk.startswith(DDS_HEADER):
            #     print(f'Found DDS! index: {index}')
            #     DDSes += 1
            #     with open(os.path.join(f'{file_name}/DDS', f'{DDSes}.dds'), 'wb') as dds_file:
            #         dds_file.write(current_chunk)

        print('---------------')
        #print(f'Found {WAVes} WAV(es) and {DDSes} DDS(es)')
        print(f'Found {WAVes} WAV(es)')
        print('---------------')
        input('Press enter to continue...')

parse_pak_file(input('Enter .pak name: '))