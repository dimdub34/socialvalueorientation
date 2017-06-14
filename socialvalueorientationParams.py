# -*- coding: utf-8 -*-
"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu at the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

# variables --------------------------------------------------------------------
VERSION_A = 0
VERSION_B = 1
TREATMENTS_NAMES = {VERSION_A: "Version A", VERSION_B: "Version B"}

# parameters -------------------------------------------------------------------
TREATMENT = VERSION_A
TAUX_CONVERSION = 1
MONNAIE = u"None"


matrices_A = {
    1: ([85, 85, 85, 85, 85, 85, 85, 85, 85], [85, 76, 68, 59, 50, 41, 33, 24, 15]),
    2: ([85, 87, 89, 91, 93, 94, 96, 98, 100], [15, 19, 24, 28, 33, 37, 41, 46, 50]),
    3: ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 98, 96, 94, 93, 91, 89, 87, 85]),
    4: ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 89, 79, 68, 58, 47, 36, 26, 15]),
    5: ([100, 94, 88, 81, 75, 69, 63, 56, 50], [50, 56, 63, 69, 75, 81, 88, 94, 100]),
    6: ([100, 98, 96, 94, 93, 91, 89, 87, 85], [50, 54, 59, 63, 68, 72, 76, 81, 85]),
    7: ([100, 96, 93, 89, 85, 81, 78, 74, 70], [50, 56, 63, 69, 75, 81, 88, 94, 100]),
    8: ([90, 91, 93, 94, 95, 96, 98, 99, 100], [100, 99, 98, 96, 95, 94, 93, 91, 90]),
    9: ([100, 94, 88, 81, 75, 69, 63, 56, 50], [70, 74, 78, 81, 85, 89, 93, 96, 100]),
    10: ([100, 99, 98, 96, 95, 94, 93, 91, 90], [70, 74, 78, 81, 85, 89, 93, 96, 100]),
    11: ([70, 74, 78, 81, 85, 89, 93, 96, 100], [100, 96, 93, 89, 85, 81, 78, 74, 70]),
    12: ([50, 56, 63, 69, 75, 81, 88, 94, 100], [100, 99, 98, 96, 95, 94, 93, 91, 90]),
    13: ([50, 56, 63, 69, 75, 81, 88, 94, 100], [100, 94, 88, 81, 75, 69, 63, 56, 50]),
    14: ([100, 96, 93, 89, 85, 81, 78, 74, 70], [90, 91, 93, 94, 95, 96, 98, 99, 100]),
    15: ([90, 91, 93, 94, 95, 96, 98, 99, 100], [100, 94, 88, 81, 75, 69, 63, 56, 50])
}

matrices_B = {
    1: ([100, 98, 96, 94, 93, 91, 89, 87, 85], [50, 54, 59, 63, 68, 72, 76, 81, 85]),
    2: ([100, 94, 88, 81, 75, 69, 63, 56, 50], [50, 56, 63, 69, 75, 81, 88, 94, 100]),
    3: ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 89, 79, 68, 58, 47, 36, 26, 15]),
    4: ([50, 54, 59, 63, 68, 72, 76, 81, 85], [100, 98, 96, 94, 93, 91, 89, 87, 85]),
    5: ([85, 87, 89, 91, 93, 94, 96, 98, 100], [15, 19, 24, 28, 33, 37, 41, 46, 50]),
    6: ([85, 85, 85, 85, 85, 85, 85, 85, 85], [85, 76, 68, 59, 50, 41, 33, 24, 15]),
    7: ([90, 91, 93, 94, 95, 96, 98, 99, 100], [100, 94, 88, 81, 75, 69, 63, 56, 50]),
    8: ([100, 96, 93, 89, 85, 81, 78, 74, 70], [90, 91, 93, 94, 95, 96, 98, 99, 100]),
    9: ([50, 56, 63, 69, 75, 81, 88, 94, 100], [100, 94, 88, 81, 75, 69, 63, 56, 50]),
    10: ([50, 56, 63, 69, 75, 81, 88, 94, 100], [100, 99, 98, 96, 95, 94, 93, 91, 90]),
    11: ([70, 74, 78, 81, 85, 89, 93, 96, 100], [100, 96, 93, 89, 85, 81, 78, 74, 70]),
    12: ([100, 99, 98, 96, 95, 94, 93, 91, 90], [70, 74, 78, 81, 85, 89, 93, 96, 100]),
    13: ([100, 94, 88, 81, 75, 69, 63, 56, 50], [70, 74, 78, 81, 85, 89, 93, 96, 100]),
    14: ([90, 91, 93, 94, 95, 96, 98, 99, 100], [100, 99, 98, 96, 95, 94, 93, 91, 90]),
    15: ([100, 96, 93, 89, 85, 81, 78, 74, 70], [50, 56, 63, 69, 75, 81, 88, 94, 100])
}
