
#export DISPLAY=:0
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functions import *


class Form(QDialog, UFunc):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Annotator")
        self.edit = QPlainTextEdit('')
        self.info_box = QPlainTextEdit('')

        self.quit = QPushButton("QUIT")
        self.quit.clicked.connect(app.exit)

        self.bd_bt = QPushButton("BD")
        self.bd_bt.clicked.connect(self.bd)

        self.ch_bt = QPushButton("CH")
        self.ch_bt.clicked.connect(self.ch)

        self.pr_bt = QPushButton("PR")
        self.pr_bt.clicked.connect(self.pr)

        self.sp_bt = QPushButton("SP")
        self.sp_bt.clicked.connect(self.sp)

        self.ed_bt = QPushButton("ED")
        self.ed_bt.clicked.connect(self.ed)

        self.bp_bt = QPushButton("BP")
        self.bp_bt.clicked.connect(self.bp)

        self.clear_bt = QPushButton("CLEAR")
        self.clear_bt.clicked.connect(self.clear)
        
        self.save_bt = QPushButton("SAVE")
        self.save_bt.clicked.connect(self.save)

        self.load_bt = QPushButton("LOAD")
        self.load_bt.clicked.connect(self.load)

        self.edit.selectionChanged.connect(self.handleSelectionChanged)
        layout = QGridLayout()
        # layout.addWidget(self.info_box, 1,1,1,8)
        # layout.addWidget(self.edit, 1, 0, 1, 8)
        layout.addWidget(self.info_box, 1, 0, 1 ,2)
        layout.addWidget(self.edit, 1, 2, 1, 10)
        layout.addWidget(self.bd_bt, 2, 0)
        layout.addWidget(self.ch_bt, 2, 1)
        layout.addWidget(self.pr_bt, 2, 2)
        layout.addWidget(self.sp_bt, 2, 3)
        layout.addWidget(self.ed_bt, 2, 4)
        layout.addWidget(self.bp_bt, 2, 5)
        layout.addWidget(self.clear_bt, 2, 6)
        layout.addWidget(self.load_bt, 2, 7)
        layout.addWidget(self.save_bt, 2, 10)
        self.setLayout(layout)
        self.selection = [0, 0, 0]
        self.selection_list = []
        self.html = ""
        self.setupDataset() # load the dataset

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form=Form()
    form.show()
    sys.exit(app.exec_())