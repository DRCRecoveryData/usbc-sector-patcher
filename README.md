## Acknowledgements

This script was inspired by the work of Nguyen Vu Ha CEO of DRC Recovery, who originally developed a similar patching method to recover data from disk images that contain USBC sectors. Their work was an invaluable resource in the development of this script.

# Fixing File System Corruption Caused by USBC Sectors using Python

![2023-02-20_201557](https://user-images.githubusercontent.com/85211068/220119775-e914c793-6818-4151-b22a-0f468950c7ed.png)

This Python script is designed to help fix file system corruption caused by USBC sectors in disk images. USBC sectors are USB/SCSI command blocks that should not end up on the disk, and can cause file system corruption by introducing sector shift. This script will help patch the USBC sectors and recover lost data.

## Prerequisites

Before using this script, you'll need to have the following:

- Python 3.x
- The `struct` module (included with Python)
- A disk image that contains USBC sectors.

If you don't have a disk image that contains USBC sectors, you can create one by making a bit-for-bit copy of a damaged storage device, using a tool like `dd` on Linux, or `Win32DiskImager` on Windows.

## How to Use the Script

1. Open a terminal window and navigate to the directory where the script is located.
2. Run the script by typing `python patch_usbc_sectors.py` in the terminal.
3. Enter the path to the disk image file when prompted.
4. Wait for the script to finish patching the USBC sectors.
5. The patched disk image will be saved in a new directory called "Patched" in the same location as the original disk image.

## How the Script Works

The script works by using Python's `struct` module to decode the USBC sector and determine the number of sectors it was intended to write. It then deletes the USBC sector, shifts all sectors in the block up by one LBA, and inserts a zero-filled sector at the end of the block. This patching process helps to recover lost data and fix file system corruption caused by USBC sectors.

## License

This program is released under the GNU General Public License, version 3 or any later version. See the [LICENSE](LICENSE) file for more details.

## Disclaimer

Please note that this script is not guaranteed to work in all cases, and is provided as-is with no warranty or guarantee. It is always recommended to create a backup of your data before attempting any data recovery or disk repair operations.
