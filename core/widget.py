from PySide import QtGui, QtCore


class DoubleButtons(QtGui.QWidget):

    def __init__(self, trueBtnName, falseBtnName, trueCommand, falseCommand):
        super(DoubleButtons, self).__init__()

        self.mainLayout = QtGui.QHBoxLayout()

        self.trueBtn = QtGui.QPushButton(trueBtnName)
        self.falseBtn = QtGui.QPushButton(falseBtnName)

        self.trueCommand = trueCommand
        self.falseCommand = falseCommand

        self.mainLayout.addWidget(self.trueBtn)
        self.mainLayout.addWidget(self.falseBtn)

        self.trueBtn.clicked.connect(self.trueCommand)
        self.falseBtn.clicked.connect(self.falseCommand)

        self.setLayout(self.mainLayout)


class LineEdit(QtGui.QWidget):

    def __init__(self, label):
        super(LineEdit, self).__init__()

        self.mainLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(label)
        self.lineEdit = QtGui.QLineEdit()

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.lineEdit)

        self.setLayout(self.mainLayout)

    def getLineEditValue(self):
        return self.lineEdit.text()

class ComboBox(QtGui.QWidget):

    def __init__(self, label, items=[]):
        super(ComboBox, self).__init__()

        self.mainLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(label)
        self.comboBox = QtGui.QComboBox()

        self.items = items

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.comboBox)

        self.setLayout(self.mainLayout)

        self.updateItems()

    def updateItems(self):
        self.comboBox.clear()
        self.comboBox.addItems(self.items)

    def deleteItems(self, items):
        for item in items:
            if item in self.items:
                index = self.items.index(item)
                self.comboBox.removeItem(index)
                self.items.remove(item)


class ButtonLineEdit(QtGui.QWidget):

    def __init__(self, labelName, command):
        super(ButtonLineEdit, self).__init__()

        self.mainLayout = QtGui.QVBoxLayout()

        self.lineEdit = LineEdit(labelName)
        self.doubleButttons = DoubleButtons('Apply', 'Apply and Close',
                                            self.apply, self.applyAndClose)

        self.command = command

        self.mainLayout.addWidget(self.lineEdit)
        self.mainLayout.addWidget(self.doubleButttons)

        self.setLayout(self.mainLayout)

    def apply(self):
        self.command(self.lineEdit.getLineEditValue())

    def applyAndClose(self):
        self.apply()
        self.close()

class FloatSlider(QtGui.QWidget):

    def __init__(self, label):
        super(FloatSlider, self).__init__()

        self.mainLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel()
        self.label.setText(label)
        self.slider = QtGui.QSlider()

        self.mainLayout.addWidget(self.label)
        self.mainLayout.addWidget(self.slider)

        self.setLayout(self.mainLayout)
