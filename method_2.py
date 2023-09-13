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
    img_path = input("Enter path to disk image file: ")

    # create "Patched" directory if it doesn't exist
    os.makedirs('Patched', exist_ok=True)

    with open(img_path, 'r+b') as f:
        data = f.read()
        usbc_offset = data.find(b'USBC')

        while usbc_offset != -1:
            cmd_len = struct.unpack_from('>H', data, usbc_offset + 22)[0]

            # delete the USBC sector
            data = data[:usbc_offset] + b'\x00' * 512 + data[usbc_offset + 512:]

            # shift all sectors in the block up by one LBA
            for i in range(2, cmd_len + 1):
                sector_offset = usbc_offset + i * 512
                data = data[:sector_offset - 512] + data[sector_offset:sector_offset + 512] + data[sector_offset - 512:]

            # insert a zero-filled sector at the end of the block
            end_offset = usbc_offset + cmd_len * 512
            data = data[:end_offset] + b'\x00' * 512 + data[end_offset:]

            usbc_offset = data.find(b'USBC', end_offset)

        # save the patched disk image to the "Patched" directory
        patched_img_path = os.path.join('Patched', os.path.basename(img_path))
        with open(patched_img_path, 'wb') as patched_f:
            patched_f.write(data)

if __name__ == "__main__":
    main()

