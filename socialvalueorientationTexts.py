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
    return trans_SVO(u"In this task you have been randomly paired with another "
                     u"person, whom we will refer to as the other. This other "
                     u"person is someone you do not know and will remain "
                     u"mutually anonymous. All of your choices are completely "
                     u"confidential. You will be making a series of "
                     u"decisions about allocating resources between you and "
                     u"this other person. For each of the following questions, "
                     u"please indicate the distribution you prefer most by "
                     u"marking the respective position along the midline. "
                     u"You can only make one mark for each question. Your "
                     u"decisions will yield money for both yourself and the "
                     u"other person. In the example below, a person has chosen "
                     u"to distribute money so that he/she receives 50 dollars, "
                     u"while the anonymous other person receives 40 dollars. "
                     u"There are no right or wrong answers, this is all about "
                     u"personal preferences. After you have made your decision, "
                     u"write the resulting distribution of money on the "
                     u"spaces on the right. As you can see, your choices will "
                     u"influence both the amount of money you receive as well "
                     u"as the amount of money the other receives")


