# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import socialvalueorientationParams as pms


logger = logging.getLogger("le2m")


class PartieSVO(Partie):
    __tablename__ = "partie_socialvalueorientation"
    __mapper_args__ = {'polymorphic_identity': 'socialvalueorientation'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsSVO')

    def __init__(self, le2mserv, joueur):
        super(PartieSVO, self).__init__(
            nom="socialvalueorientation", nom_court="SVO",
            joueur=joueur, le2mserv=le2mserv)
        self.SVO_gain_ecus = 0
        self.SVO_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsSVO(period)
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        on envoie les matrices une par une
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        matrice = pms.matrices_A if pms.TREATMENT == pms.VERSION_A else pms.matrices_B
        debut = datetime.now()
        for m in range(1, len(matrice) + 1):
            dec = yield (self.remote.callRemote(
                "display_decision", matrice[m]))
            setattr(self.currentperiod, "SVO_matrice_{}".format(m), dec)
            self.joueur.info(u"mat. {}: {}".format(m, dec))
        self.currentperiod.SVO_decisiontime = (datetime.now() - debut).seconds
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        """
        Compute the payoff for the period
        :return:
        """
        logger.debug(u"{} Period Payoff".format(self.joueur))
        self.currentperiod.SVO_periodpayoff = 0

        # cumulative payoff since the first period
        if self.currentperiod.SVO_period < 2:
            self.currentperiod.SVO_cumulativepayoff = \
                self.currentperiod.SVO_periodpayoff
        else: 
            previousperiod = self.periods[self.currentperiod.SVO_period - 1]
            self.currentperiod.SVO_cumulativepayoff = \
                previousperiod.SVO_cumulativepayoff + \
                self.currentperiod.SVO_periodpayoff

        # we store the period in the self.periodes dictionnary
        self.periods[self.currentperiod.SVO_period] = self.currentperiod

        logger.debug(u"{} Period Payoff {}".format(
            self.joueur,
            self.currentperiod.SVO_periodpayoff))

    @defer.inlineCallbacks
    def display_summary(self, *args):
        """
        Send a dictionary with the period content values to the remote.
        The remote creates the text and the history
        :param args:
        :return:
        """
        logger.debug(u"{} Summary".format(self.joueur))
        yield(self.remote.callRemote(
            "display_summary", self.currentperiod.todict()))
        self.joueur.info("Ok")
        self.joueur.remove_waitmode()

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        """
        Compute the payoff for the part and set it on the remote.
        The remote stores it and creates the corresponding text for display
        (if asked)
        :return:
        """
        logger.debug(u"{} Part Payoff".format(self.joueur))

        self.SVO_gain_ecus = self.currentperiod.SVO_cumulativepayoff
        self.SVO_gain_euros = float(self.SVO_gain_ecus) * float(pms.TAUX_CONVERSION)
        yield (self.remote.callRemote(
            "set_payoffs", self.SVO_gain_euros, self.SVO_gain_ecus))

        logger.info(u'{} Payoff ecus {} Payoff euros {:.2f}'.format(
            self.joueur, self.SVO_gain_ecus, self.SVO_gain_euros))


class RepetitionsSVO(Base):
    __tablename__ = 'partie_socialvalueorientation_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_socialvalueorientation.partie_id"))

    SVO_period = Column(Integer)
    SVO_treatment = Column(Integer)
    SVO_matrice_1 = Column(Integer)
    SVO_matrice_2 = Column(Integer)
    SVO_matrice_3 = Column(Integer)
    SVO_matrice_4 = Column(Integer)
    SVO_matrice_5 = Column(Integer)
    SVO_matrice_6 = Column(Integer)
    SVO_matrice_7 = Column(Integer)
    SVO_matrice_8 = Column(Integer)
    SVO_matrice_9 = Column(Integer)
    SVO_matrice_10 = Column(Integer)
    SVO_matrice_11 = Column(Integer)
    SVO_matrice_12 = Column(Integer)
    SVO_matrice_13 = Column(Integer)
    SVO_matrice_14 = Column(Integer)
    SVO_matrice_15 = Column(Integer)
    SVO_decisiontime = Column(Integer)
    SVO_periodpayoff = Column(Float)
    SVO_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.SVO_treatment = pms.TREATMENT
        self.SVO_period = period
        self.SVO_decisiontime = 0
        self.SVO_periodpayoff = 0
        self.SVO_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns
                if "SVO" in c.name}
        if joueur:
            temp["joueur"] = joueur
        return temp

