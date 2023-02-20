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

img_path = input("Enter path to disk image file: ")

# create "Patched" directory if it doesn't exist
if not os.path.exists('Patched'):
    os.mkdir('Patched')

with open(img_path, 'r+b') as f:
    # loop over all occurrences of the USBC sector in the file
    while True:
        # find the next occurrence of the USBC sector
        usbc_offset = f.read().find(b'USBC')
        if usbc_offset == -1:
            # USBC sector not found, exit loop
            break

        # decode the USBC sector and determine the number of sectors it was intended to write
        f.seek(usbc_offset)
        data = bytearray(f.read(512))
        cmd_len = struct.unpack('>H', data[22:24])[0]

        # delete the USBC sector
        f.seek(usbc_offset)
        f.write(b'\x00' * 512)

        # shift all sectors in the block up by one LBA
        for i in range(2, cmd_len+1):
            sector_offset = usbc_offset + i*512
            f.seek(sector_offset)
            sector_data = bytearray(f.read(512))
            f.seek(sector_offset - 512)
            f.write(sector_data)

        # insert a zero-filled sector at the end of the block
        end_offset = usbc_offset + cmd_len * 512
        f.seek(end_offset)
        f.write(b'\x00' * 512)

    # save the patched disk image to the "Patched" directory
    f.seek(0)
    patched_img_path = os.path.join('Patched', os.path.basename(img_path))
    with open(patched_img_path, 'wb') as patched_f:
        patched_f.write(f.read())
