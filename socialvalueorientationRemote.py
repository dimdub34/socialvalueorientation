# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from twisted.spread import pb
from client.cltremote import IRemote
from client.cltgui.cltguidialogs import GuiRecapitulatif
import socialvalueorientationParams as pms
from socialvalueorientationGui import GuiDecision
import socialvalueorientationTexts as texts_SVO


logger = logging.getLogger("le2m")


class RemoteSVO(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period

    def remote_display_decision(self, matrice):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randint(1, len(matrice[0]))
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else:
            defered = defer.Deferred()
            ecran_decision = GuiDecision(
                defered, self._le2mclt.automatique,
                self._le2mclt.screen, matrice)
            ecran_decision.show()
            return defered

    def remote_display_summary(self, period_content):
        """
        Display the summary screen
        :param period_content: dictionary with the content of the current period
        :return: deferred
        """
        logger.info(u"{} Summary".format(self._le2mclt.uid))
        self.histo.append([period_content.get(k) for k in self.histo_vars])
        if self._le2mclt.simulation:
            return 1
        else:
            defered = defer.Deferred()
            ecran_recap = GuiRecapitulatif(
                defered, self._le2mclt.automatique, self._le2mclt.screen,
                self.currentperiod, self.histo,
                texts_SVO.get_text_summary(period_content))
            ecran_recap.show()
            return defered
