# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import sys
import logging
import random
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import socialvalueorientationParams as pms
from socialvalueorientationTexts import trans_SVO
import socialvalueorientationTexts as texts_SVO
from client.cltgui.cltguiwidgets import WExplication


logger = logging.getLogger("le2m")


class WMatrice(QtGui.QWidget):
    def __init__(self, parent, matrice, automatique):
        super(WMatrice, self).__init__(parent)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.widget = QtGui.QWidget()
        layout.addWidget(self.widget)
        self.widget.setStyleSheet("border: 1px solid #D8D8D8;")

        gridlayout = QtGui.QGridLayout()
        self.widget.setLayout(gridlayout)

        self.matrice = matrice
        top, bottom = self.matrice

        label_you = QtGui.QLabel(trans_SVO(u"You receive"))
        gridlayout.addWidget(label_you, 0, 0)
        label_other = QtGui.QLabel(trans_SVO(u"The other receives"))
        gridlayout.addWidget(label_other, 2, 0)

        self.radios_group = QtGui.QButtonGroup()
        for i in range(len(top)):
            gridlayout.addWidget(QtGui.QLabel(str(top[i])), 0, i+1)
            radio = QtGui.QRadioButton()
            self.radios_group.addButton(radio, i)
            gridlayout.addWidget(radio, 1, i+1)
            gridlayout.addWidget(QtGui.QLabel(str(bottom[i])), 2, i + 1)
        self.radios_group.buttonClicked.connect(self.set_values)

        gridlayout.addWidget(QtGui.QLabel(trans_SVO(u"You")), 0, len(top) + 1)
        self.spinbox_you = QtGui.QSpinBox()
        self.spinbox_you.setMinimum(0)
        self.spinbox_you.setMaximum(999)
        self.spinbox_you.setSingleStep(1)
        self.spinbox_you.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self.spinbox_you.setStyleSheet("font-weight: bold; color: black;")
        self.spinbox_you.setEnabled(False)
        gridlayout.addWidget(self.spinbox_you, 0, len(top) + 2)

        gridlayout.addWidget(QtGui.QLabel(trans_SVO(u"Other")), 2, len(top) + 1)
        self.spinbox_other = QtGui.QSpinBox()
        self.spinbox_other.setMinimum(0)
        self.spinbox_other.setMaximum(999)
        self.spinbox_other.setSingleStep(1)
        self.spinbox_other.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self.spinbox_other.setStyleSheet("font-weight: bold; color: black;")
        self.spinbox_other.setEnabled(False)
        gridlayout.addWidget(self.spinbox_other, 2, len(top) + 2)

        self.adjustSize()

        if automatique:
            self.radios_group.button(random.randint(0, len(top)-1)).setChecked(True)
            self.spinbox_you.setValue(top[self.radios_group.checkedId()])
            self.spinbox_other.setValue(bottom[self.radios_group.checkedId()])

    @QtCore.pyqtSlot()
    def set_values(self):
        self.spinbox_you.setValue(self.matrice[0][self.radios_group.checkedId()])
        self.spinbox_other.setValue(self.matrice[1][self.radios_group.checkedId()])


class WSlide(QtGui.QWidget):
    def __init__(self, parent, matrice, automatique):
        super(WSlide, self).__init__(parent)

        self.matrice = matrice
        top, bottom = self.matrice
        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        wlcd = QtGui.QWidget()
        wlcd.setStyleSheet("background-color: white;")
        formlayout = QtGui.QFormLayout()
        self.lcd_you = QtGui.QLCDNumber()
        self.lcd_you.setFrameShape(QtGui.QLCDNumber.NoFrame)
        self.lcd_you.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_you.setStyleSheet("color: blue;")
        self.lcd_you.setFixedHeight(20)
        self.lcd_you.setFixedWidth(60)
        formlayout.addRow(QtGui.QLabel(trans_SVO(u"You")), self.lcd_you)
        self.lcd_other = QtGui.QLCDNumber()
        self.lcd_other.setFrameShape(QtGui.QLCDNumber.NoFrame)
        self.lcd_other.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.lcd_other.setStyleSheet("color: blue;")
        self.lcd_other.setFixedHeight(20)
        self.lcd_other.setFixedWidth(60)
        formlayout.addRow(QtGui.QLabel(trans_SVO(u"Other")), self.lcd_other)
        wlcd.setLayout(formlayout)

        hlayout = QtGui.QHBoxLayout()
        hlayout.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        hlayout.addWidget(wlcd)
        hlayout.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        layout.addLayout(hlayout)

        layout.addSpacerItem(QtGui.QSpacerItem(5, 40, QtGui.QSizePolicy.Minimum,
                              QtGui.QSizePolicy.Fixed))

        # Sliders
        gridlayout = QtGui.QGridLayout()
        gridlayout.setHorizontalSpacing(30)
        layout.addLayout(gridlayout)
        label_you = QtGui.QLabel(trans_SVO(u"You receive"))
        gridlayout.addWidget(label_you, 0, 0)
        label_other = QtGui.QLabel(trans_SVO(u"The other receives"))
        gridlayout.addWidget(label_other, 2, 0)
        for i in range(len(top)):
            gridlayout.addWidget(QtGui.QLabel(str(top[i])), 0, i+1)
            gridlayout.addWidget(QtGui.QLabel(str(bottom[i])), 2, i + 1)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setStyleSheet("QSlider{background: transparent}")
        self.slider.setMinimum(0)
        self.slider.setMaximum(len(top)-1)
        self.slider.setValue(0)
        self.slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.display)
        gridlayout.addWidget(self.slider, 1, 1, 1, len(top))
        self.display()

        self.adjustSize()

        if automatique:
            self.slider.setValue(random.randint(0, len(top)-1))

    def display(self):
        self.lcd_you.display(self.matrice[0][self.slider.value()])
        self.lcd_other.display(self.matrice[1][self.slider.value()])


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, num_question, matrice):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self.matrice = matrice

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=texts_SVO.get_text_explanation(),
            size=(650, 150), parent=self)
        layout.addWidget(wexplanation)

        if pms.DISPLAY == pms.DISPLAY_SLIDER:
            self.wslider = WSlide(self, self.matrice, self._automatique)
            layout.addWidget(self.wslider)
        elif pms.DISPLAY == pms.DISPLAY_RADIO:
            self.wmatrice = WMatrice(self, self.matrice, self._automatique)
            layout.addWidget(self.wmatrice)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_SVO(u"Question {}".format(num_question)))
        self.adjustSize()
        self.setFixedSize(self.size())

        if self._automatique:
            self._timer_automatique = QtCore.QTimer()
            self._timer_automatique.timeout.connect(
                buttons.button(QtGui.QDialogButtonBox.Ok).click)
            self._timer_automatique.start(7000)
                
    def reject(self):
        pass
    
    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        try:

            if pms.DISPLAY == pms.DISPLAY_SLIDER:
                decision = self.wslider.slider.value()

            elif pms.DISPLAY == pms.DISPLAY_RADIO:
                decision = self.wmatrice.radios_group.checkedId()
                if decision == -1:
                    raise ValueError(trans_SVO(u"Please select a distribution"))
                you = self.wmatrice.spinbox_you.value()
                if you != self.matrice[0][decision]:
                    raise ValueError(trans_SVO(u"The value you wrote for 'you' "
                                               u"doesn't correspond to the "
                                               u"distribution you choose."))
                other = self.wmatrice.spinbox_other.value()
                if other != self.matrice[1][decision]:
                    raise ValueError(trans_SVO(u"The value you wrote for 'other' "
                                               u"doesn't correspond to the "
                                               u"distribution you choose."))
        except ValueError as e:
            QtGui.QMessageBox.warning(self, trans_SVO(u"Be careful"), e.message)
            return

        if not self._automatique:
            confirmation = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your choice?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirmation != QtGui.QMessageBox.Yes: 
                return
        logger.info(u"Send back {}".format(decision))
        self.accept()
        self._defered.callback(decision)


class DConfigure(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        form = QtGui.QFormLayout()
        layout.addLayout(form)

        # treatment
        self._combo_treatment = QtGui.QComboBox()
        self._combo_treatment.addItems(
            [v for k, v in sorted(pms.TREATMENTS_NAMES.items())])
        self._combo_treatment.setCurrentIndex(pms.TREATMENT)
        form.addRow(QtGui.QLabel(u"Traitement"), self._combo_treatment)

        # display
        self._combo_display = QtGui.QComboBox()
        self._combo_display.addItems(
            [v for k, v in sorted(pms.DISPLAY_NAMES.items())])
        self._combo_display.setCurrentIndex(pms.DISPLAY)
        form.addRow(QtGui.QLabel(u"Affichage"), self._combo_display)

        button = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        button.accepted.connect(self._accept)
        button.rejected.connect(self.reject)
        layout.addWidget(button)

        self.setWindowTitle(u"Configurer")
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        pms.TREATMENT = self._combo_treatment.currentIndex()
        pms.DISPLAY = self._combo_display.currentIndex()
        self.accept()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    # test_mat = WSlide(None, pms.matrices_A[2])
    test_mat = GuiDecision(None, 1, None, pms.matrices_A[2])
    test_mat.show()
    sys.exit(app.exec_())