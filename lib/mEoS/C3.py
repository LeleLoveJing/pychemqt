#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2017, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


from unittest import TestCase

from scipy import exp

from lib.meos import MEoS
from lib import unidades


class C3(MEoS):
    """Multiparameter equation of state for propane"""
    name = "propane"
    CASNumber = "74-98-6"
    formula = "CH3CH2CH3"
    synonym = "R-290"
    _refPropName = "PROPANE"
    _coolPropName = "n-Propane"
    rhoc = unidades.Density(220.4781)
    Tc = unidades.Temperature(369.89)
    Pc = unidades.Pressure(4251.2, "kPa")
    M = 44.09562  # g/mol
    Tt = unidades.Temperature(85.525)
    Tb = unidades.Temperature(231.036)
    f_acent = 0.1521
    momentoDipolar = unidades.DipoleMoment(0.084, "Debye")
    id = 4
    _Tr = unidades.Temperature(354.964211)
    _rhor = unidades.Density(221.906745)
    _w = 0.149041513

    Fi1 = {"ao_log": [1, 3],
           "pow": [0, 1],
           "ao_pow": [-4.970583, 4.29352],
           "ao_exp": [3.043, 5.874, 9.337, 7.922],
           "titao": [393/Tc, 1237/Tc, 1984/Tc, 4351/Tc],
           "ao_hyp": [], "hyp": []}

    Fi2 = {"ao_log": [1, 3.02939],
           "pow": [0, 1],
           "ao_pow": [31.602908195, -84.463284382],
           "ao_exp": [], "titao": [],
           "ao_hyp": [6.60569, 3.197, 19.1921, -8.37267],
           "hyp": [479.856/Tc, 200.893/Tc, 955.312/Tc, 1027.29/Tc]}

    CP1 = {"ao": 4.02939,
           "an": [], "pow": [],
           "ao_exp": [], "exp": [],
           "ao_hyp": [6.60569, 3.197, 19.1921, -8.37267],
           "hyp": [479.856, 200.893, 955.312, 1027.29]}

    Fi3 = {"ao_log": [1, 3.02256195],
           "pow": [0, 1],
           "ao_pow": [10.14394256, -4.79513693],
           "ao_exp": [2.90591124, 4.68495401, 10.2971154, 8.08977905],
           "titao": [1.0515052038, 3.0961635368, 5.0845797877, 11.4329447982],
           "ao_hyp": [], "hyp": []}

    Fi4 = {"ao_log": [1, 3.021394],
           "pow": [0, 1],
           "ao_pow": [-4.992402, 4.291476],
           "ao_exp": [2.889980, 4.474243, 8.139803, 10.48251],
           "titao": [1.048309, 3.053170, 11.42280, 5.042815],
           "ao_hyp": [], "hyp": []}

    CP5 = {"ao": -5.4041204338,
           "an": [3.1252450099e6, -1.1415253638e5, 1.4971650720e3,
                  3.9215452897e-2, -2.1738913926e-5, 4.8274541303e-9],
           "pow": [-3, -2, -1.001, 1, 2, 3],
           "ao_exp": [3.1907016349], "exp": [1500],
           "ao_hyp": [], "hyp": []}

    lemmon = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Lemmon et al. "
                    "(2009)",
        "__doi__": {"autor": "Lemmon, E.W., McLinden, M.O., Wagner, W.",
                    "title": "Thermodynamic Properties of Propane.  III.  A "
                             "Reference Equation of State for Temperatures "
                             "from the Melting Line to 650 K and Pressures up "
                             "to 1000 MPa",
                    "ref": "J. Chem. Eng. Datai, 54(12) (2009) 3141-3180",
                    "doi": "10.1021/je900217v"},

        "R": 8.314472,
        "cp": Fi1,
        "ref": {"Tref": 273.15, "Pref": 1, "ho": 26148.48, "so": 157.9105},

        "Tmin": Tt, "Tmax": 650.0, "Pmax": 1000000.0, "rhomax": 20.6,
        "Pmin": 0.00000017, "rhomin": 16.63,

        "nr1":  [0.42910051e-1, 0.17313671e1, -0.24516524e1, 0.34157466,
                 -0.46047898],
        "d1": [4, 1, 1, 2, 2],
        "t1": [1, 0.33, 0.8, 0.43, 0.9],

        "nr2": [-0.66847295, 0.20889705, 0.19421381, -0.22917851, -0.60405866,
                0.66680654e-1],
        "d2": [1, 3, 6, 6, 2, 3],
        "t2": [2.46, 2.09, 0.88, 1.09, 3.25, 4.62],
        "c2": [1, 1, 1, 1, 2, 2],
        "gamma2": [1]*6,

        "nr3": [0.17534618e-1, 0.33874242, 0.22228777, -0.23219062,
                -0.92206940e-1, -0.47575718, -0.17486824e-1],
        "d3": [1, 1, 1, 2, 2, 4, 1],
        "t3": [0.76, 2.50, 2.75, 3.05, 2.55, 8.40, 6.75],
        "alfa3": [0.963, 1.977, 1.917, 2.307, 2.546, 3.28, 14.6],
        "beta3": [2.33, 3.47, 3.15, 3.19, 0.92, 18.8, 547.8],
        "gamma3": [0.684, 0.829, 1.419, 0.817, 1.500, 1.426, 1.093],
        "epsilon3": [1.283, 0.6936, 0.788, 0.473, 0.8577, 0.271, 0.948]}

    buecker = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Bücker and "
                    "Wagner (2006)",
        "__doi__": {"autor": "Bücker, D., Wagner, W.",
                    "title": "Reference Equations of State for the "
                             "Thermodynamic Properties of Fluid Phase "
                             "n-Butane and Isobutane",
                    "ref": "J. Phys. Chem. Ref. Data 35(2) (2006) 929-1019",
                    "doi": "10.1063/1.1901687"},

        "R": 8.314472,
        "cp": Fi3,
        "ref": "OTO",

        "Tmin": Tt, "Tmax": 500.0, "Pmax": 100000.0, "rhomax": 17.41,
        "Pmin": 0.00000017, "rhomin": 16.62,

        "nr1": [.21933784906951e1, -.38432884604893e1, .56820219711755,
                .11235233289697, -.13246623110619e-1, .14587076590314e-1,
                .19654925217128e-1],
        "d1": [1, 1, 1, 2, 3, 4, 4],
        "t1": [0.50, 1.00, 1.50, 0.00, 0.50, 0.50, 0.75],

        "nr2": [.73811022854042, -.85976999811290, .14331675665712,
                -.23280677426427e-1, -.98713669399783e-4, .45708225999895e-2,
                -.27766802597861e-1, -.10523131087952, .97082793466314e-1,
                .20710537703751e-1, -.54720320371501e-1, .64918009057295e-3,
                .74471355056336e-2, -.27504616979066e-3, -.77693374632348e-2,
                -.17367624932157e-2],
        "d2": [1, 1, 2, 7, 8, 8, 1, 2, 3, 3, 4, 5, 5, 10, 2, 6],
        "t2": [2.00, 2.50, 2.50, 1.50, 1.00, 1.50, 4.00, 7.00, 3.00, 7.00,
               3.00, 1.00, 6.00, 0.00, 6.00, 13.00],
        "c2": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3],
        "gamma2": [1]*16,

        "nr3": [-.38248057095416e-1, -.68797254435490e-2],
        "d3": [1, 2],
        "t3": [2., 0.],
        "alfa3": [10, 10],
        "beta3": [150, 200],
        "gamma3": [1.16, 1.13],
        "epsilon3": [0.85, 1.]}

    MBWR = {
        "__type__": "MBWR",
        "__name__": "MBWR equation of state for propane of Younglove and Ely "
                    "(1987)",
        "__doi__": {"autor": "Younglove, B.A. and Ely, J.F.",
                    "title": "Thermophysical Properties of Fluids. II. "
                             "Methane, Ethane, Propane, Isobutane, and Normal "
                             "Butane",
                    "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                    "doi": "10.1063/1.555785"},

        "R": 8.31434,
        "cp": CP5,
        "ref": {"Tref": 298.15, "Pref": 101.325, "ho": 14740.2, "so": 270.203},

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 100000.0, "rhomax": 17.36,
        "Pmin": 1.685e-7, "rhomin": 16.617,

        "b": [None, -0.2804337729e-2, 0.1180666107e1, -0.3756325860e2,
              0.5624374521e4, -0.9354759605e6, -0.4557405505e-3, 1.530044332,
              -0.1078107476e4, 0.2218072099e6, 0.6629473971e-4, -0.06199354447,
              0.6754207966e2, 0.6472837570e-2, -0.6804325262, -0.9726162355e2,
              0.05097956459, -0.1004655900e-2, 0.4363693352, -0.01249351947,
              0.2644755879e6, -0.7944237270e8, -0.7299920845e4, 0.5381095003e9,
              0.3450217377e2, 0.9936666689e4, -0.2166699036e1, -0.1612103424e6,
              -0.3633126990e-2, 0.1108612343e2, -0.1330932838e-3,
              -0.3157701101e-1, 0.1423083811e1]}

    GERG = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Kunz and "
                    "Wagner (2004).",
        "__doi__": {"autor": "Kunz, O., Wagner, W.",
                    "title": "The GERG-2008 Wide-Range Equation of State for "
                             "Natural Gases and Other Mixtures: An Expansion "
                             "of GERG-2004",
                    "ref": "J. Chem.Eng. Data 57(11) (2012) 3032-3091",
                    "doi":  "10.1021/je300655b"},

        "R": 8.314472,
        "cp": Fi2,
        "ref": "OTO",

        "Tmin": 85.48, "Tmax": 500.0, "Pmax": 100000.0, "rhomax": 17.41,
        "Pmin": 73.476, "rhomin": 29.249,

        "nr1": [1.0403973107358, -2.8318404081403, 0.84393809606294,
                -0.076559591850023, 0.094697373057280, 0.24796475497006e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.2774376042287, -0.043846000648377, -0.2699106478435,
                -0.069313413089860, -0.029632145981653, 0.014040126751380],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    miyamoto = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Miyamoto and "
                    "Watanabe (2001)",
        "__doi__": {"autor": "Miyamoto, H. and Watanabe, K.",
                    "title": "A Thermodynamic Property Model for Fluid-Phase "
                             "Propane",
                    "ref": "Int. J. Thermophys., 21(5) (2000) 1045-1072",
                    "doi":  "10.1023/A:1026441903474"},

        "R": 8.314472,
        "cp": Fi4,
        "ref": "IIR",

        "Tmin": Tt, "Tmax": 623.0, "Pmax": 103000.0, "rhomax": 17.41,
        "Pmin": 0.00000017, "rhomin": 16.64,

        "nr1":  [2.698378e-1, -1.339252, -2.273858e-2, 2.414973e-1,
                 -3.321461e-2, 2.203323e-3, 5.935588e-5, -1.137457e-6],
        "d1": [1, 1, 2, 2, 3, 5, 8, 8],
        "t1": [-0.25, 1.5, -0.75, 0, 1.25, 1.5, 0.5, 2.5],

        "nr2": [-2.379299, 2.337373, 1.242344e-3, -7.352787e-3, 1.965751e-3,
                -1.402666e-1, -2.093360e-2, -2.475221e-4, -1.482723e-2,
                -1.303038e-2, 3.634670e-5],
        "d2": [3, 3, 8, 5, 6, 1, 5, 7, 2, 3, 15],
        "t2": [1.5, 1.75, -0.25, 3, 3, 4, 2, -1, 2, 19, 5],
        "c2": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
        "gamma2": [1]*11}

    shortSpan = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for propane of Span "
                    "and Wagner (2003)",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of state for technical applications. "
                             "II. Results for nonpolar fluids.",
                    "ref": "Int. J. Thermophys. 24 (1) (2003) 41-109",
                    "doi": "10.1023/A:1022310214958"},

        "R": 8.31451,
        "cp": CP1,
        "ref": "OTO",
        "M": 44.097, "Tc": 369.825, "rhoc": 220.48/44.097,

        "Tmin": Tt, "Tmax": 750.0, "Pmax": 100000.0, "rhomax": 17.36,
        "Pmin": 0.00000015304, "rhomin": 16.706,

        "nr1":  [0.10403973e1, -0.28318404e1, 0.8439381, -0.76559592e-1,
                 0.94697373e-1, 0.24796475e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.2774376, -0.43846001e-1, -0.26991065, -0.69313413e-1,
                -0.29632146e-1, 0.14040127e-1],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    sun = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for propane of Sun and Ely "
                    "(2004)",
        "__doi__": {"autor": "Sun, L. and Ely, J.F.",
                    "title": "Universal equation of state for engineering "
                             "application: Algorithm and  application to "
                             "non-polar and polar fluids",
                    "ref": "Fluid Phase Equilib., 222-223 (2004) 107-118",
                    "doi": "10.1016/j.fluid.2004.06.028"},

        "R": 8.314472,
        "cp": Fi1,
        "ref": {"Tref": 273.15, "Pref": 1, "ho": 26148.48, "so": 157.9105},

        "Tmin": Tt, "Tmax": 620.0, "Pmax": 800000.0, "rhomax": 40.,
        "Pmin": 0.1, "rhomin": 40.,

        "nr1": [9.70439249e-1, 9.73671323e-1, -2.96661981, 7.84340496e-2,
                2.78440866e-4, -6.77622221e-2],
        "d1": [1, 1, 1, 3, 7, 2],
        "t1": [1.5, 0.25, 1.25, 0.25, 0.875, 1.375],

        "nr2": [-8.56371936e-2, 1.77467443e-1, 3.91636018e-1, -8.03312946e-3,
                -0.260385851, -1.91104746e-2, -6.31331470e-2, -2.27769095e-2],
        "d2": [1, 1, 2, 5, 1, 1, 4, 2],
        "t2": [0, 2.375, 2., 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*8}

    eq = lemmon, buecker, GERG, miyamoto, shortSpan, sun
    # eq = lemmon, MBWR, buecker, GERG, miyamoto, shortSpan, sun

    _surface = {"sigma": [0.05334, -0.01748], "exp": [1.235, 4.404]}
    _dielectric = {"eq": 4, "Tref": 273.16, "rhoref": 1000.,
                   "a0": [0.1573071],  "expt0": [-1.], "expd0": [1.],
                   "a1": [15.85, 0.036], "expt1": [0, 1], "expd1": [1, 1],
                   "a2": [172.75, 505.67, -388.21, -2078.8],
                   "expt2": [0, 1, 0, 1], "expd2": [2, 2, 2.35, 2.35]}
    _melting = {"eq": 1, "Tref": Tt, "Pref": 0.00000017,
                "Tmin": Tt, "Tmax": 2000.0,
                "a1": [-4230000000000, 4230000000001], "exp1": [0, 1.283],
                "a2": [], "exp2": [], "a3": [], "exp3": []}

    _vapor_Pressure = {
        "eq": 3,
        "n": [-6.7722, 1.6938, -1.3341, -3.1876, 0.94937],
        "t": [1, 1.5, 2.2, 4.8, 6.2]}
    _liquid_Density = {
        "eq": 1,
        "n": [1.82205, 0.65802, 0.21109, 0.083973],
        "t": [0.345, 0.74, 2.6, 7.2]}
    _vapor_Density = {
        "eq": 2,
        "n": [-2.4887, -5.1069, -12.174, -30.495, -52.192, -134.89],
        "t": [0.3785, 1.07, 2.7, 5.5, 10., 20.]}

    visco0 = {"__name__": "Vogel (2016)",
              "__doi__": {
                  "autor": "Vogel, E., Herrmann, S.",
                  "title": "New Formulation for the Viscosity of Propane",
                  "ref": "J. Phys. Chem. Ref. Data 45(4) (2016) 043103",
                  "doi": "10.1063/1.4966928"},

              "eq": 1, "omega": 0,

              "Toref": 369.89,
              "no": [9.9301297115406, 7.2658798096248e-1,
                     -7.4692506744427e-1, 1.0156334572774e-1],
              "to": [1, 2, 3, 4],

              "Tref_res": 369.89, "rhoref_res": 220.478,
              "nr": [1.2514603628320e1, 1.5922183980545, -1.7976570855233e-2,
                     9.9769818327437e-2, 1.0361434810683e-5,
                     -1.4863884140117e-9, 4.8405686431740e-10,
                     -1.3029665878806e1, 1.8734125698089, 2.3303894474483,
                     3.4631192496757],
              "dr": [1, 2, 4, 7, 14, 19, 20, 1, 1, 4, 5],
              "tr": [0, 0, 3, 0, 2, 6, 6, 1, 2, 1, 0],
              "gr": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
              "cr": [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],

              "nr_gaus": [3.2587396573174, 2.1724931048783e-1],
              "br_gaus": [20, 100],
              "er_gaus": [250, 100]}

    visco1 = {"__name__": "Vogel (1998)",
              "__doi__": {
                  "autor": "Vogel, E., Küchenmeister, C., Bich, E., Laesecke, "
                           "A.",
                  "title": "Reference Correlation of the Viscosity of Propane",
                  "ref": "J. Phys. Chem. Ref. Data 27(5) (1998) 947-970",
                  "doi": "10.1063/1.556025"},

              "eq": 1, "omega": 1,

              "M": 44.0956, "ek": 263.88, "sigma": 0.49748,
              "n_chapman": 0.021357,
              "collision": [0.25104574, -0.47271238, 0, 0.060836515],

              "Tref_virial": 263.88,
              "n_virial": [-19.572881, 219.73999, -1015.3226, 2471.01251,
                           -3375.1717, 2491.6597, -787.26086, 14.085455,
                           -0.34664158],
              "t_virial": [0, -0.25, -0.5, -0.75, -1, -1.25, -1.5, -2.5, -5.5],

              "Tref_res": 369.825, "rhoref_res": 5*44.0956,
              "nr": [35.9873030195, -180.512188564, 87.7124888223,
                     -105.773052525, 205.319740877, -129.210932610,
                     58.9491587759, -129.7400331, 76.6280419971,
                     -9.59407868475, 21.0726986598, -14.3971968187],
              "dr": [2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5],
              "tr": [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2],
              "gr": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              "cr": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

              "CPf": 1616.88405374,
              "CPg1": 2.50053938863,
              "CPgi": [0.860516059264], "CPti": [-0.5]}

    visco2 = {"eq": 2, "omega": 2,
              "__name__": "Younglove (1987)",
              "__doi__": {
                  "autor": "Younglove, B.A., Ely, J.F.",
                  "title": "Thermophysical Properties of Fluids. II. Methane, "
                           "Ethane, Propane, Isobutane, and Normal Butane",
                  "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                  "doi": "10.1063/1.555785"},

              "ek": 358.9, "sigma": 0.47,
              "n_chapman": 0.177273976/M**0.5,

              "F": [0, 0, 1.12, 359.],
              "E": [-14.113294896, 968.22940153, 13.686545032, -12511.628378,
                    0.0168910864, 43.527109444, 7659.45434720],
              "rhoc": 5.0}

    visco3 = {"__name__": u"Quiñones-Cisneros (2006)",
              "__doi__": {
                  "autor": "Quiñones-Cisneros, S.E., Deiters, U.K.",
                  "title": "Generalization of the Friction Theory for "
                           "Viscosity Modeling",
                  "ref": "J. Phys. Chem. B, 110(25) (2006) 12820-12834",
                  "doi": "10.1021/jp0618577"},

              "eq": 4, "omega": 0,

              "Toref": 369.825,
              "no": [12.3057, -42.5793, 40.3486],
              "to": [0, 0.25, 0.5],

              "a": [-9.34268e-6, -4.93309e-5, 0],
              "b": [9.60710e-5, -8.18031e-5, 0],
              "c": [7.68800e-5, -4.18871e-5, 0],
              "A": [-8.49309e-9, -4.91415e-10, 0],
              "B": [2.08795e-8, 9.21785e-10, 0],
              "C": [-4.05944e-7, 1.31731e-7, 0]}

    _viscosity = visco0, visco1, visco2, visco3

    thermo0 = {"__name__": "Marsh (2002)",
               "__doi__": {
                   "autor": "Marsh, K.N., Perkins, R.A., Ramires, M.L.V.",
                   "title": "Measurement and Correlation of the Thermal "
                            "Conductivity of Propane from 86 to 600 K at "
                            "Pressures to 70 MPa",
                   "ref": "J. Chem. Eng. Data 47(4) (2002) 932-940",
                   "doi": "10.1021/je010001m"},

               "eq": 1,

               "Toref": 369.85, "koref": 1.,
               "no": [-1.24778e-3, 8.16371e-3, 1.99374e-2],
               "to": [0, 1, 2],

               "Tref_res": 369.85, "rhoref_res": 220.3, "kref_res": 1.,
               "nr": [-3.695e-2, 4.82798e-2, 1.48658e-1, -1.35636e-1,
                      -1.19986e-1, 1.17588e-1, 4.12431e-2, -4.36911e-2,
                      -4.86905e-3, 6.16079e-3],
               "tr": [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
               "dr": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],

               "critical": 3,
               "gnu": 0.63, "gamma": 1.239, "R0": 1.03, "Xio": 0.194e-9,
               "gam0": 0.0496, "qd": 0.716635e-9, "Tcref": 554.73}

    thermo1 = {"__name__": "Younglove (1987)",
               "__doi__": {
                   "autor": "Younglove, B.A., Ely, J.F.",
                   "title": "Thermophysical Properties of Fluids. II. Methane,"
                            " Ethane, Propane, Isobutane, and Normal Butane",
                   "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                   "doi": "10.1063/1.555785"},

               "eq": 2, "omega": 2,

               "visco": visco1,
               "G": [0.1422605e1, -0.179749],
               "E": [0.3113890422e-2, -0.225755973, 0.5674370999e2,
                     -0.7840963643e-4, 0.2291785465e-1, -0.2527939890e1,
                     -0.6265334654e-1, 0.2518064809e1],

               "critical": 2,
               "X": [3.98, 5.45, 0.468067, 1.08],
               "Z": 8.117e-10}

    _thermal = thermo0, thermo1


class Test(TestCase):

    def test_lemmon(self):
        # Table 5, pag 3174
        st = C3(T=200, rhom=14)
        self.assertEqual(round(st.P.MPa, 7), 2.3795138)
        self.assertEqual(round(st.cvM.JmolK, 6), 61.078424)
        self.assertEqual(round(st.cpM.JmolK, 6), 93.475362)
        self.assertEqual(round(st.w, 4), 1381.9552)

        st = C3(T=300, rhom=12)
        self.assertEqual(round(st.P.MPa, 6), 19.053797)
        self.assertEqual(round(st.cvM.JmolK, 6), 73.972542)
        self.assertEqual(round(st.cpM.JmolK, 5), 108.61529)
        self.assertEqual(round(st.w, 5), 958.40520)

        st = C3(T=300, rhom=0.4)
        self.assertEqual(round(st.P.MPa, 8), 0.84694991)
        self.assertEqual(round(st.cvM.JmolK, 6), 69.021875)
        self.assertEqual(round(st.cpM.JmolK, 6), 85.753997)
        self.assertEqual(round(st.w, 5), 221.88959)

        st = C3(T=400, rhom=5)
        self.assertEqual(round(st.P.MPa, 7), 6.6462840)
        self.assertEqual(round(st.cvM.JmolK, 6), 97.017439)
        self.assertEqual(round(st.cpM.JmolK, 5), 271.07044)
        self.assertEqual(round(st.w, 5), 194.65847)

        st = C3(T=369.9, rhom=5)
        self.assertEqual(round(st.P.MPa, 7), 4.2519399)
        self.assertEqual(round(st.cvM.JmolK, 5), 117.71621)
        self.assertEqual(round(st.cpM.JmolK, 2), 753625.00)
        self.assertEqual(round(st.w, 5), 130.89800)

        # Selected point from Table A1, Pag 3175, saturation state
        st = C3(T=-50+273.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 6), 0.070569)
        self.assertEqual(round(st.Liquido.rho, 2), 589.90)
        self.assertEqual(round(st.Liquido.h.kJkg, 3), 82.753)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 0.5298)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 1.428)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 2.212)
        self.assertEqual(round(st.Liquido.w, 1), 1212.5)
        self.assertEqual(round(st.Gas.rho, 4), 1.7270)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 516.48)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), 2.473)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 1.182)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 1.397)
        self.assertEqual(round(st.Gas.w, 1), 216.5)

        st = C3(T=50+273.15, x=0.5)
        self.assertEqual(round(st.P.MPa, 4), 1.7133)
        self.assertEqual(round(st.Liquido.rho, 2), 448.87)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 336.80)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), 1.450)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 1.780)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 3.089)
        self.assertEqual(round(st.Liquido.w, 1), 546.8)
        self.assertEqual(round(st.Gas.rho, 3), 38.630)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 621.66)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), 2.332)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 1.753)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 2.499)
        self.assertEqual(round(st.Gas.w, 1), 202.2)

    def test_shortSpan(self):
        # Table III, Pag 46
        st = C3(T=700, rho=200, eq="shortSpan")
        self.assertEqual(round(st.cp0.kJkgK, 3), 3.235)
        self.assertEqual(round(st.P.MPa, 3), 27.175)
        self.assertEqual(round(st.cp.kJkgK, 4), 3.5658)

        st2 = C3(T=750, rho=100, eq="shortSpan")
        self.assertEqual(round(st2.h.kJkg-st.h.kJkg, 2), 212.66)
        self.assertEqual(round(st2.s.kJkgK-st.s.kJkgK, 5), 0.41879)

    def test_custom(self):
        """Test for other model not tested"""
        # Reference state for Miyamoto correlation
        st = C3(T=273.15, x=0.0, eq="miyamoto")
        self.assertEqual(round(st.h.kJkg, 0), 200)
        self.assertEqual(round(st.s.kJkgK, 2), 1)

    def test_Vogel(self):
        # Table 6, Pag 16
        self.assertEqual(round(C3(T=90, rho=730).mu.muPas, 3), 8010.968)
        self.assertEqual(round(C3(T=300, rho=1).mu.muPas, 6), 8.174374)
        self.assertEqual(round(C3(T=300, rho=20).mu.muPas, 6), 8.230795)
        self.assertEqual(round(C3(T=300, rho=490).mu.muPas, 5), 95.63100)
        self.assertEqual(round(C3(T=300, rho=600).mu.muPas, 4), 223.6002)
        self.assertEqual(round(
            C3(T=369.89, rho=220.478).mu.muPas, 5), 25.70313)
        self.assertEqual(round(C3(T=375, rho=1).mu.muPas, 5), 10.15009)
        self.assertEqual(round(C3(T=375, rho=100).mu.muPas, 5), 13.07220)
        self.assertEqual(round(C3(T=375, rho=550).mu.muPas, 4), 146.8987)
        self.assertEqual(round(C3(T=500, rho=1).mu.muPas, 5), 13.26285)
        self.assertEqual(round(C3(T=500, rho=100).mu.muPas, 5), 16.85501)
        self.assertEqual(round(C3(T=500, rho=450).mu.muPas, 5), 77.67365)
        self.assertEqual(round(C3(T=650, rho=1).mu.muPas, 5), 16.63508)
        self.assertEqual(round(C3(T=650, rho=100).mu.muPas, 5), 20.72894)
        self.assertEqual(round(C3(T=650, rho=400).mu.muPas, 5), 62.40780)

    def test_Vogel2(self):
        # TODO: Input density calcualte from MBWR equation, do when fix
        # The method give good values, but the density input values are
        # unreproducibles while MBWR don't work

        # Table 4, pag 961
        # self.assertEqual(round(C3(T=90, P=1e4, visco=1).mu.muPas, 1), 7388.0)
        pass
