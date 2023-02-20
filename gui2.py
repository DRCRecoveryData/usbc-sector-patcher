import os
import struct
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

class DiskPatcher(QMainWindow):
    def __init__(self):
        super().__init__()

        # set up default values
        self.img_path = ""
        self.verbose = ""

        # set up main window
        self.setWindowTitle("Disk Patcher")
        self.setGeometry(100, 100, 400, 400)

        # create widgets
        self.select_button = QPushButton("Select Image")
        self.select_button.clicked.connect(self.select_image)

        self.verbose_box = QPlainTextEdit()
        self.verbose_box.setReadOnly(True)

        # set up layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.select_button)
        main_layout.addWidget(self.verbose_box)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_image(self):
        # get image path
        self.img_path, _ = QFileDialog.getOpenFileName(self, "Select image", filter="Disk image (*.img)")
        if self.img_path:
            self.patch_image()

    def patch_image(self):
        # create "Patched" directory if it doesn't exist
        if not os.path.exists('Patched'):
            os.mkdir('Patched')

        with open(self.img_path, 'r+b') as f:
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

                # update the verbose box
                self.verbose += f"USBC sector at offset {usbc_offset} patched\n"
                self.verbose_box.setPlainText(self.verbose)

            # save the patched disk image to the "Patched" directory
            f.seek(0)
            patched_img_path = os.path.join('Patched', os.path.basename(self.img_path))
            with open(patched_img_path, 'wb') as patched_f:
                patched_f.write(f.read())

            # update the verbose box
            self.verbose += f"\nPatching complete. Image saved to {patched_img_path}\n"
            self.verbose_box.setPlainText(self.verbose)

if __name__ == '__main__':
    app = QApplication([])
    patcher = DiskPatcher()
    patcher.show()
    app.exec_()
