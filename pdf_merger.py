import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QCheckBox, QLabel, QTextEdit
from PyQt5.QtGui import QIcon
from PyPDF2 import PdfFileReader, PdfFileWriter

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PDF Merger'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
        self.fileNames = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonGetFiles = QPushButton('Choose PDFs to Merge', self)
        buttonGetFiles.resize(200,32)
        buttonGetFiles.move(540, 500)        
        buttonGetFiles.clicked.connect(self.openFileDialog)
        
        self.show()
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        fileNamesFromDialog, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","PDF Files (*.pdf)", options=options)
        if fileNamesFromDialog:
            for filename in fileNamesFromDialog:
                print(filename)
                self.fileNames.append(filename)
        self.cams = filesChosen(self.fileNames)
        self.cams.show()
        self.close()
            

class filesChosen(QWidget):

    def __init__(self, files):
        super().__init__()
        self.title = 'PDF Merger'
        self.left = 100
        self.top = 100
        self.width = 1280
        self.height = 960
        self.fileNames = files
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonGoBack = QPushButton('Back to File Selection', self)
        buttonGoBack.move(540, 900)
        buttonGoBack.resize(200, 32)
        buttonGoBack.clicked.connect(self.buttonGoBack_onClick)

        buttonMerge = QPushButton('Merge Files', self)
        buttonMerge.move(540, 800)
        buttonMerge.resize(200, 32)
        buttonMerge.clicked.connect(self.buttonMerge_onClick)

        otherText = QLabel(self)
        otherText.setText("Files Chosen for Merging:")
        otherText.setGeometry(440, 300, 200, 32)
        filesText = QTextEdit(self)
        if self.fileNames:
            fileNameText = ''
            for filename in self.fileNames:
                fileNameText += filename + "<br>"
                print(filename)
            filesText.setText(fileNameText)
        else:
            filesText.setText('No files chosen.')
        filesText.setReadOnly(True)
        filesText.setGeometry(440,330,400,300)
        

        self.show()

    def buttonGoBack_onClick(self):
        self.cams=App()
        self.cams.show()
        self.close()

    def buttonMerge_onClick(self):
        self.merge_pdfs(self.fileNames, "output.pdf")

    
    def merge_pdfs(self, paths, output):
        pdf_writer = PdfFileWriter()

        for path in paths:
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                # Add each page to the writer object
                pdf_writer.addPage(pdf_reader.getPage(page))

        # Write out the merged PDF
        with open(output, 'wb') as out:
            pdf_writer.write(out)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())