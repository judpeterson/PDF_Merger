import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton, QHBoxLayout, QCheckBox, QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QMovie, QPainter
from PyPDF2 import PdfFileReader, PdfFileWriter
import time

class App(QWidget):

    def __init__(self, boolean):
        super().__init__()
        self.title = 'PDF Merger'
        self.setWindowIcon(QIcon("C:\\Users\\cold\\Downloads\\pdf_icon.png"))
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 600
        self.fileNames = []
        self.showSuccess = boolean
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.movie = QMovie("C:\\Users\\cold\\Downloads\\cats.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        buttonGetFiles = QPushButton('Choose PDFs to Merge', self)
        buttonGetFiles.resize(200,32)
        buttonGetFiles.move(200, 300)        
        buttonGetFiles.clicked.connect(self.openFileDialog)

        if self.showSuccess:
            explText = QLabel(self)
            explText.setText("Success! File created.")
            explText.setGeometry(175, 100, 250, 32)
            explText.setStyleSheet('color: green; font: 18pt Arial')
        
        self.show()
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        fileNamesFromDialog, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileName()", "","PDF Files (*.pdf);;All Files (*)", options=options)
        if fileNamesFromDialog:
            for filename in fileNamesFromDialog:
                self.fileNames.append(filename)
        self.cams = filesChosen(self.fileNames)
        self.cams.show()
        self.close()

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)
            

class filesChosen(QWidget):

    def __init__(self, files):
        super().__init__()
        self.title = 'PDF Merger'
        self.setWindowIcon(QIcon("C:\\Users\\cold\\Downloads\\pdf_icon.png"))
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 600
        self.fileNames = files
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.movie = QMovie("C:\\Users\\cold\\Downloads\\cats.gif")
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        buttonGoBack = QPushButton('Back to File Selection', self)
        buttonGoBack.move(200, 550)
        buttonGoBack.resize(200, 32)
        buttonGoBack.clicked.connect(self.buttonGoBack_onClick)

        buttonMerge = QPushButton('Merge Files', self)
        buttonMerge.move(200, 500)
        buttonMerge.resize(200, 32)
        buttonMerge.clicked.connect(self.buttonMerge_onClick)
        
        explText = QLabel(self)
        explText.setText("Merge will happen in order listed here.")
        explText.setGeometry(200, 10, 200, 32)

        expl2Text = QLabel(self)
        expl2Text.setText("Rearrange by moving text to correct position with each file on a separate line.")
        expl2Text.setGeometry(100, 50, 400, 32)

        otherText = QLabel(self)
        otherText.setText("Files Chosen for Merging:")
        otherText.setGeometry(200, 90, 200, 32)

        self.filesText = QTextEdit(self)
        if self.fileNames:
            fileNameText = ''
            for filename in self.fileNames:
                fileNameText += filename + "<br>"
            self.filesText.setText(fileNameText)
        else:
            self.filesText.setText('No files chosen.')
        self.filesText.setGeometry(100,130,400,300)
        

        self.show()

    def buttonGoBack_onClick(self):
        self.cams = App(False)
        self.cams.show()
        self.close()

    def buttonMerge_onClick(self):
        filesTextValue = self.filesText.toPlainText()
        files = filesTextValue.splitlines()
        output_file = self.saveFileDialog()
        if output_file:
            self.merge_pdfs(files, output_file)
            self.cams = App(True)
            self.cams.show()
            self.close()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Save File As","","PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            return fileName
        else:
            return ''

    def paintEvent(self, event):
        currentFrame = self.movie.currentPixmap()
        frameRect = currentFrame.rect()
        frameRect.moveCenter(self.rect().center())
        if frameRect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

    def merge_pdfs(self, paths, output):
        pdf_writer = PdfFileWriter()

        for path in paths:
            if path:
                pdf_reader = PdfFileReader(path)
                for page in range(pdf_reader.getNumPages()):
                    # Add each page to the writer object
                    pdf_writer.addPage(pdf_reader.getPage(page))

        # Write out the merged PDF
        with open(output, 'wb') as out:
            pdf_writer.write(out)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(False)
    sys.exit(app.exec_())
