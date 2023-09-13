# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import struct

def main():
    print("Be careful! Make a copy of the disk image first!")
    print("This program will modify the original file if a USBC sector is found.")
    
    img_path = input("Enter path to disk image file: ")

    # create "Patched" directory if it doesn't exist
    os.makedirs('Patched', exist_ok=True)

    with open(img_path, 'r+b') as f:
        data = f.read()
        while True:
            usbc_offset = data.find(b'USBC')
            if usbc_offset == -1:
                # USBC sector not found, exit loop
                print("No more USBC sectors found, exiting")
                break
            
            print("USBC found at offset:", usbc_offset)

            # decode the USBC sector to determine the number of sectors it was intended to write
            sector_data = data[usbc_offset:usbc_offset + 512]
            cmd_len = struct.unpack('>H', sector_data[22:24])[0]

            # shift all sectors in the block up by one LBA
            for i in range(cmd_len):
                # read the sector after USBC
                data_to_shift = data[usbc_offset + (i + 1) * 512:usbc_offset + (i + 2) * 512]

                # overwrite the current sector with the data read
                data = data[:usbc_offset + i * 512] + data_to_shift + data[usbc_offset + i * 512 + len(data_to_shift):]

            # Zero out the last sector
            end_offset = usbc_offset + cmd_len * 512
            data = data[:end_offset] + b'\x00' * 512 + data[end_offset + 512:]

        # save the patched disk image to the "Patched" directory
        patched_img_path = os.path.join('Patched', os.path.basename(img_path))
        with open(patched_img_path, 'wb') as patched_f:
            patched_f.write(data)

if __name__ == "__main__":
    main()


