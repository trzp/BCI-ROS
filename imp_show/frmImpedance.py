# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmImpedanceDisplay.ui'
#
# Created: Sun Oct 28 20:07:55 2018
#      by: PyQt4 UI code generator 4.11
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmImpedanceDisplay(object):
    def setupUi(self, frmImpedanceDisplay):
        frmImpedanceDisplay.setObjectName(_fromUtf8("frmImpedanceDisplay"))
        frmImpedanceDisplay.resize(730, 340)
        frmImpedanceDisplay.setMinimumSize(QtCore.QSize(730, 340))
        frmImpedanceDisplay.setMaximumSize(QtCore.QSize(730, 340))
        frmImpedanceDisplay.setSizeGripEnabled(True)
        self.tableWidgetValues = QtGui.QTableWidget(frmImpedanceDisplay)
        self.tableWidgetValues.setGeometry(QtCore.QRect(9, 9, 711, 291))
        self.tableWidgetValues.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidgetValues.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.tableWidgetValues.setRowCount(7)
        self.tableWidgetValues.setColumnCount(10)
        self.tableWidgetValues.setObjectName(_fromUtf8("tableWidgetValues"))
        self.tableWidgetValues.setColumnCount(10)
        self.tableWidgetValues.setRowCount(7)
        self.tableWidgetValues.horizontalHeader().setVisible(False)
        self.tableWidgetValues.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetValues.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidgetValues.horizontalHeader().setHighlightSections(False)
        self.tableWidgetValues.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidgetValues.verticalHeader().setVisible(False)
        self.tableWidgetValues.verticalHeader().setDefaultSectionSize(40)
        self.tableWidgetValues.verticalHeader().setHighlightSections(False)
        self.widget = QtGui.QWidget(frmImpedanceDisplay)
        self.widget.setGeometry(QtCore.QRect(530, 310, 182, 22))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.spinBox = QtGui.QSpinBox(self.widget)
        self.spinBox.setMinimum(10)
        self.spinBox.setMaximum(20)
        self.spinBox.setSingleStep(5)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout.addWidget(self.spinBox)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)

        self.retranslateUi(frmImpedanceDisplay)
        QtCore.QMetaObject.connectSlotsByName(frmImpedanceDisplay)

    def retranslateUi(self, frmImpedanceDisplay):
        frmImpedanceDisplay.setWindowTitle(_translate("frmImpedanceDisplay", "Impedance", None))
        self.label_2.setText(_translate("frmImpedanceDisplay", "Impedance scale:0-", None))
        self.label_3.setText(_translate("frmImpedanceDisplay", "kom", None))

