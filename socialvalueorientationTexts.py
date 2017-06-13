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


def get_histo_vars():
    return ["SVO_period", "SVO_decision",
            "SVO_periodpayoff",
            "SVO_cumulativepayoff"]


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_SVO(u"Explanation text")


def get_text_label_decision():
    return trans_SVO(u"Decision label")


def get_text_summary(period_content):
    txt = trans_SVO(u"Summary text")
    return txt


