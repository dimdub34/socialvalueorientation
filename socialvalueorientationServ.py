# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import socialvalueorientationParams as pms
from socialvalueorientationGui import DConfigure
import random


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("socialvalueorientation")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Social Value Orientation", actions)

    def _configure(self):
        # self._le2mserv.gestionnaire_graphique.display_information(
        #     le2mtrans(u"There is no parameter to configure"))
        # return
        screen_conf = DConfigure(self._le2mserv.gestionnaire_graphique.screen)
        if screen_conf.exec_():
            to_display = [
                u"Traitement: {}".format(pms.TREATMENTS_NAMES[pms.TREATMENT]),
                u"Affichage: {}".format(pms.DISPLAY_NAMES[pms.DISPLAY])
            ]
            self._le2mserv.gestionnaire_graphique.infoserv(to_display)

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs == 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                le2mtrans(u"No clients connected!"))
            return

        if self._le2mserv.gestionnaire_joueurs.nombre_joueurs % \
                2 != 0:
            self._le2mserv.gestionnaire_graphique.display_error(
                u"Il faut un nombre de joueurs multiple de 2")
            return

        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") + u" socialvalueorientation?"):
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "socialvalueorientation", "PartieSVO",
            "RemoteSVO", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'socialvalueorientation')

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))

        # form groups
        self._le2mserv.gestionnaire_groupes.former_groupes(
            self._le2mserv.gestionnaire_joueurs.get_players(), 2)

        # Start part ===========================================================
        # init period
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, le2mtrans(u"Period") + u" {}".format(0)])
        self._le2mserv.gestionnaire_graphique.infoclt(
            [None, le2mtrans(u"Period") + u" {}".format(0)],
            fg="white", bg="gray")
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "newperiod", 0))

        # decision
        yield(self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Decision"), self._tous, "display_decision"))

        # tirage et enregistrement de la décision de l'autre pour la question
        # tirée
        self._le2mserv.gestionnaire_graphique.infoserv(u"Tirages")
        matrices = pms.matrices_A if pms.TREATMENT == pms.VERSION_A else \
            pms.matrices_B
        for g, m in self._le2mserv.gestionnaire_groupes.get_groupes(
                "socialvalueorientation").items():
            # m[0]
            tirage_m0 = random.randint(1, len(matrices))
            m[0].currentperiod.SVO_tirage = tirage_m0
            choix_m0 = getattr(m[0].currentperiod, "SVO_matrice_{}".format(tirage_m0))
            m[1].currentperiod.SVO_tirage_paire = tirage_m0
            m[1].currentperiod.SVO_choix_paire_tirage = choix_m0
            
            # m[1]
            tirage_m1 = random.randint(1, len(matrices))
            m[1].currentperiod.SVO_tirage = tirage_m1
            choix_m1 = getattr(m[1].currentperiod, "SVO_matrice_{}".format(tirage_m1))
            m[0].currentperiod.SVO_tirage_paire = tirage_m1
            m[0].currentperiod.SVO_choix_paire_tirage = choix_m1

            self._le2mserv.gestionnaire_graphique.infoserv(
                u"G{} - {} ({}), {} ({})".format(
                    g.split("_")[2], m[0].joueur, tirage_m0, m[1].joueur,
                    tirage_m1))

        # period payoffs
        self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
            "socialvalueorientation")

        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "socialvalueorientation"))
