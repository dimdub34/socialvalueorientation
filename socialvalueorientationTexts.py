# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import socialvalueorientationParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "socialvalueorientation",
                             "locale")
    trans_SVO = gettext.translation(
      "socialvalueorientation", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_SVO = lambda x: x  # if there is an error, no translation


def get_text_explanation():
    return u"Vous devez décider de la répartition d'une somme d’argent entre " \
           u"vous et une personne de la salle. Vous ne pouvez pas identifier " \
           u"l'autre personne et elle ne peut pas vous identifier. Il n’y a pas " \
           u"de bonne ou de mauvaise réponse, et les données seront traitées " \
           u"de manière anonyme. Pour chacune des 15 questions, " \
           u"indiquez la répartition que vous préférez en " \
           u"cliquant sur le bouton correspondant. "
