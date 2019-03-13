from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon

from PyQt5 import uic

from app.Template import Template
from app.Validator import Validator

from app.Model import Model

class Ui (QMainWindow):

    parent = False
    def __init__(self, app):
        super(Ui, self).__init__()

        self.parent = app
        self.ui = uic.loadUi('MainWindow.ui', self)

        self.ui.openFile.clicked.connect( self.onOpenFile )
        self.ui.exec.clicked.connect( self.Exec )
        self.show()
        #self.initUI()

    menuActions = {}
    menuSubActions = {}

    def onOpenFile(self):
        QMessageBox.information(self, "Файл", "Выберите сначала ref файл, а затем data")
        self.fileRef = QFileDialog.getOpenFileName(self, "Выберите ref файл")[0]
        self.fileData = QFileDialog.getOpenFileName(self, "Выберите data файл")[0]

        QMessageBox.information(self, "Успешно", "Теперь можно настраивать ограничения")


    def Exec(self):
        model = Model( N=50 )

        model.setDeleteNum(self.ui.deleteLine.text())
        model.setSpeedLimit(self.ui.speedLine.text())

        ret = False
        try:
            ret = model.fromTwoFiles( self.fileData, self.fileRef)
        except Exception as e:
            print(e)

        if ( ret ):
            QMessageBox.information(self, "Успешно", "Операция успешно завершилась")

    def initUI(self):
        self.statusBar().showMessage("Ready...")

        self.resize(640, 480)
        self.center()
        self.setWindowIcon(QIcon('web.jpg'))

        self.addMenuMain("Файл")
        self.AddMenuSub("Файл", "Открыть файл", "open.png", self.FileDialog)
        self.AddMenuSub("Файл", "Выход", "exit.png", "close")

        self.addMenuMain("Шаблон")
        self.AddMenuSub("Шаблон", "Создать шаблон", "open.png", self.FileDialog)
        self.AddMenuSub("Шаблон", "Загрузить шаблон", "exit.png", "close")

        self.addMenuMain("Настройки")

        self.setWindowTitle("Главное Окно")

        self.template = Template(self)

        self.textEdit = QTextEdit()
        self.textEdit.setFontPointSize(16)
        self.setCentralWidget(self.textEdit)

        self.show()

    def getTextEdit(self) -> QTextEdit:
        return self.textEdit

    def AddMenuSep(self, name):
        self.menuActions[name].addSeparator()

    def addMenuMain(self, name : str):
        self.menuActions[name] = self.menuBar().addMenu(name)

    def AddMenuSub(self, mainPoint : str, name : str, icon : str, connect):
        self.menuSubActions[name] = QAction(QIcon(icon), name, self)

        if ( type(connect) == type("str") and connect == 'close'):
            self.menuSubActions[name].triggered.connect(self.close)
        else:
            self.menuSubActions[name].triggered.connect(connect)

        self.menuActions[mainPoint].addAction(self.menuSubActions[name])

    def FileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())