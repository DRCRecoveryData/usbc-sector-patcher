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

print("Be careful! Make a copy of the disk image first!")
print("This program will modify the original file if a USBC sector is found.")

img_path = input("Enter path to disk image file: ")

# create "Patched" directory if it doesn't exist
if not os.path.exists('Patched'):
    os.mkdir('Patched')

with open(img_path, 'r+b') as f:
    while True:
        f.seek(0)  # reset the file pointer to the beginning
        data = f.read()
        usbc_offset = data.find(b'USBC')
        
        if usbc_offset == -1:
            # USBC sector not found, exit loop
            print("No more USBC sectors found, exiting")
            break
        else:
            print("USBC found at offset:", usbc_offset)

            # decode the USBC sector to determine the number of sectors it was intended to write
            f.seek(usbc_offset)
            sector_data = bytearray(f.read(512))
            cmd_len = struct.unpack('>H', sector_data[22:24])[0]

            # shift all sectors in the block up by one LBA
            for i in range(cmd_len):
                # read the sector after USBC
                f.seek(usbc_offset + (i + 1) * 512)
                data_to_shift = f.read(512)
                
                # overwrite the current sector with the data read
                f.seek(usbc_offset + i * 512)
                f.write(data_to_shift)

            # Zero out the last sector
            end_offset = usbc_offset + cmd_len * 512
            f.seek(end_offset)
            f.write(b'\x00' * 512)

    # save the patched disk image to the "Patched" directory
    f.seek(0)
    patched_img_path = os.path.join('Patched', os.path.basename(img_path))
    with open(patched_img_path, 'wb') as patched_f:
        patched_f.write(f.read())

