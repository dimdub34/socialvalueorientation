# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""

import sys
import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import socialvalueorientationParams as pms
from socialvalueorientationTexts import trans_SVO
import socialvalueorientationTexts as texts_SVO
from client.cltgui.cltguidialogs import GuiHistorique
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox


logger = logging.getLogger("le2m")


class WMatrice(QtGui.QWidget):
    def __init__(self, parent, matrice):
        super(WMatrice, self).__init__()

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.widget = QtGui.QWidget()
        layout.addWidget(self.widget)
        # self.widget.setStyleSheet("background-color: white; "
        #                           "border: 1px solid #D8D8D8;")
        self.widget.setStyleSheet("border: 1px solid #D8D8D8;")

        gridlayout = QtGui.QGridLayout()
        self.widget.setLayout(gridlayout)

        top, bottom = matrice

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

        gridlayout.addWidget(QtGui.QLabel(trans_SVO(u"You")), 0, len(top) + 1)
        self.spinbox_you = QtGui.QSpinBox()
        self.spinbox_you.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        gridlayout.addWidget(self.spinbox_you, 0, len(top) + 2)

        gridlayout.addWidget(QtGui.QLabel(trans_SVO(u"Other")), 2, len(top) + 1)
        self.spinbox_other = QtGui.QSpinBox()
        self.spinbox_other.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        gridlayout.addWidget(self.spinbox_other, 2, len(top) + 2)

        self.adjustSize()


class GuiDecision(QtGui.QDialog):
    def __init__(self, defered, automatique, parent, matrice):
        super(GuiDecision, self).__init__(parent)

        # variables
        self._defered = defered
        self._automatique = automatique
        self.matrice = matrice

        layout = QtGui.QVBoxLayout(self)

        wexplanation = WExplication(
            text=texts_SVO.get_text_explanation(),
            size=(650, 250), parent=self)
        layout.addWidget(wexplanation)

        self.wmatrice = WMatrice(self, self.matrice)
        layout.addWidget(self.wmatrice)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self._accept)
        layout.addWidget(buttons)

        self.setWindowTitle(trans_SVO(u"Décision"))
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
            list(sorted(pms.TREATMENTS_NAMES.viewvalues())))
        self._combo_treatment.setCurrentIndex(pms.TREATMENT)
        form.addRow(QtGui.QLabel(u"Traitement"), self._combo_treatment)

        # nombre de périodes
        self._spin_periods = QtGui.QSpinBox()
        self._spin_periods.setMinimum(0)
        self._spin_periods.setMaximum(100)
        self._spin_periods.setSingleStep(1)
        self._spin_periods.setValue(pms.NOMBRE_PERIODES)
        self._spin_periods.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spin_periods.setMaximumWidth(50)
        form.addRow(QtGui.QLabel(u"Nombre de périodes"), self._spin_periods)

        # periode essai
        self._checkbox_essai = QtGui.QCheckBox()
        self._checkbox_essai.setChecked(pms.PERIODE_ESSAI)
        form.addRow(QtGui.QLabel(u"Période d'essai"), self._checkbox_essai)

        # taille groupes
        self._spin_groups = QtGui.QSpinBox()
        self._spin_groups.setMinimum(0)
        self._spin_groups.setMaximum(100)
        self._spin_groups.setSingleStep(1)
        self._spin_groups.setValue(pms.TAILLE_GROUPES)
        self._spin_groups.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self._spin_groups.setMaximumWidth(50)
        form.addRow(QtGui.QLabel(u"Taille des groupes"), self._spin_groups)

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
        pms.PERIODE_ESSAI = self._checkbox_essai.isChecked()
        pms.NOMBRE_PERIODES = self._spin_periods.value()
        pms.TAILLE_GROUPES = self._spin_groups.value()
        self.accept()


if __name__ == "__main__":
    app = QtGui.QApplication([])
    test_mat = GuiDecision(None, 0, None, pms.matrices_A[1])
    test_mat.show()
    sys.exit(app.exec_())