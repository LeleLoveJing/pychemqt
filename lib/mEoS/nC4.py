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

from scipy import log, exp

from lib.meos import MEoS
from lib import unidades


class nC4(MEoS):
    """Multiparameter equation of state for n-butane"""
    name = "n-butane"
    CASNumber = "106-97-8"
    formula = "CH3-(CH2)2-CH3"
    synonym = "R-600"
    _refPropName = "BUTANE"
    _coolPropName = "n-Butane"
    rhoc = unidades.Density(228.)
    Tc = unidades.Temperature(425.125)
    Pc = unidades.Pressure(3796.0, "kPa")
    M = 58.1222  # g/mol
    Tt = unidades.Temperature(134.895)
    Tb = unidades.Temperature(272.660)
    f_acent = 0.201
    momentoDipolar = unidades.DipoleMoment(0.05, "Debye")
    id = 6
    _Tr = unidades.Temperature(406.785141)
    _rhor = unidades.Density(230.384826)
    _w = 0.194240287

    Fi1 = {"ao_log": [1, 3.24680487],
           "pow": [0, 1],
           "ao_pow": [12.54882924, -5.46976878],
           "ao_exp": [5.54913289, 11.4648996, 7.59987584, 9.66033239],
           "titao": [0.7748404445, 3.3406025522, 4.9705130961, 9.9755537783],
           "ao_hyp": [], "hyp": []}

    Fi2 = {"ao_log": [1, 3.33944],
           "pow": [0, 1],
           "ao_pow": [20.884143364, -91.638478026],
           "ao_exp": [], "titao": [],
           "ao_hyp": [9.44893, 6.89406, 24.4618, 14.7824],
           "hyp": [468.27/Tc, 183.636/Tc, 1914.1/Tc, 903.185/Tc]}

    Fi3 = {"ao_log": [1, 3.240207],
           "pow": [0, 1],
           "ao_pow": [-5.404217, 4.91136],
           "ao_exp": [5.513671, 7.388450, 10.250630, 11.061010],
           "titao": [327.55988/Tc, 1319.06935/Tc,
                     4138.63184/Tc, 1864.36783/Tc],
           "ao_hyp": [], "hyp": []}

    CP4 = {"ao": -1.3491511376e1,
           "an": [3.8802310194e5, -1.5444296890e5, 2.8455082239e3,
                  6.6142595353e-2, -2.4307965028e-5, 1.5044248429e-10],
           "pow": [-3, -2, -1.001, 1, 2, 3],
           "ao_exp": [-8.3933423467], "exp": [3000],
           "ao_hyp": [], "hyp": []}

    CP6 = {"ao": 0.801601/8.3143*58.124,
           "an": [0.655936e-3/8.3143*58.124, 0.12277e-4/8.3143*58.124,
                  -0.165626e-7/8.3143*58.124, 0.67736e-11/8.3143*58.124],
           "pow": [1, 2, 3, 4],
           "ao_exp": [], "exp": [],
           "ao_hyp": [], "hyp": []}

    buecker = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for butane of Buecker and "
                    "Wagner (2006)",
        "__doi__": {"autor": "Bücker, D., Wagner, W.",
                    "title": "Reference Equations of State for the "
                             "Thermodynamic Properties of Fluid Phase "
                             "n-Butane and Isobutane",
                    "ref": "J. Phys. Chem. Ref. Data 35(2) (2006) 929-1019",
                    "doi": "10.1063/1.1901687"},

        "R": 8.314472,
        "cp": Fi1,
        "ref": "OTO",

        "Tmin": Tt, "Tmax": 750., "Pmax": 200000.0, "rhomax": 13.86,
        "Pmin": 0.000653, "rhomin": 12.645,

        "nr1": [0.25536998241635e1, -0.44585951806696e1, 0.82425886369063,
                0.11215007011442, -0.35910933680333e-1, 0.16790508518103e-1,
                0.32734072508724e-1],
        "d1": [1, 1, 1, 2, 3, 4, 4],
        "t1": [0.50, 1.00, 1.50, 0.00, 0.50, 0.50, 0.75],
        "nr2": [0.95571232982005, -0.10003385753419e1, 0.85581548803855e-1,
                -0.025147918369616, -0.15202958578918e-2, 0.47060682326420e-2,
                -0.97845414174006e-1, -0.48317904158760e-1, 0.17841271865468,
                0.18173836739334e-1, -0.11399068074953, 0.19329896666669e-1,
                0.11575877401010e-2, 0.15253808698116e-3, -0.43688558458471e-1,
                -0.82403190629989e-2],
        "d2": [1, 1, 2, 7, 8, 8, 1, 2, 3, 3, 4, 5, 5, 10, 2, 6],
        "t2": [2.00, 2.50, 2.50, 1.50, 1.00, 1.50, 4.00, 7.00, 3.00, 7.00,
               3.00, 1.00, 6.00, 0.00, 6.00, 13.00],
        "c2": [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3],
        "gamma2": [1]*16,

        "nr3": [-0.28390056949441e-1, 0.14904666224681e-2],
        "d3": [1, 2],
        "t3": [2., 0.],
        "alfa3": [10, 10],
        "beta3": [150, 200],
        "gamma3": [1.16, 1.13],
        "epsilon3": [0.85, 1.]}

    MBWR = {
        "__type__": "MBWR",
        "__name__": "MBWR equation of state for butane of Younglove and Ely "
                    "(1987)",
        "__doi__": {"autor": "Younglove, B.A. and Ely, J.F.",
                    "title": "Thermophysical Properties of Fluids. II. "
                             "Methane, Ethane, Propane, Isobutane, and Normal "
                             "Butane",
                    "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                    "doi": "10.1063/1.555785"},

        "R": 8.31434,
        "cp": CP4,
        "ref": {"Tref": 298.15, "Pref": 101.325, "ho": 19275.7, "so": 309.909},

        "Tmin": 134.86, "Tmax": 500., "Pmax": 70000.0, "rhomax": 13.2,
        "Pmin": 6.736e-4, "rhomin": 12.65,

        "b": [None, 0.153740104603e-1, -0.160980034611, -0.979782459010e1,
              0.499660674504e3, -0.102115607687e7, 0.236032147756e-2,
              -0.137475757093e1, -0.907038733865e3, 0.385421748213e6,
              -0.349453710700e-4, 0.157361122714, 0.102301474068e3,
              0.182335737331e-1, -0.404114307787e1, 0.187979855783e1,
              0.362088795040, -0.738762248266e-2, -0.218618590563e1,
              0.118802729027, 0.706854198713e6, -0.219469885796e9,
              -0.182454361268e5, 0.206790377277e10, 0.111757550145e3,
              0.558779925986e5, -0.159579054026e2, -0.148034214622e7,
              -0.245206328201, 0.218305259309e3, -0.923990627338e-4,
              -0.205267776639e1, 0.387639044820e2]}

    GERG = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for butane of Kunz and "
                    "Wagner (2004).",
        "__doi__": {"autor": "Kunz, O., Wagner, W.",
                    "title": "The GERG-2008 Wide-Range Equation of State for "
                             "Natural Gases and Other Mixtures: An Expansion "
                             "of GERG-2004",
                    "ref": "J. Chem.Eng. Data 57(11) (2012) 3032-3091",
                    "doi": "10.1021/je300655b"},

        "R": 8.314472,
        "cp": Fi2,
        "ref": "OTO",

        "Tmin": Tt, "Tmax": 575., "Pmax": 69000.0, "rhomax": 13.2,
        "Pmin": 0.000653, "rhomin": 12.645,

        "nr1": [0.10626277411455e1, -0.28620951828350e1, 0.88738233403777,
                -0.12570581155345, 0.10286308708106, 0.25358040602654e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.32325200233982, -0.037950761057432, -0.32534802014452,
                -0.079050969051011, -0.020636720547775, 0.57053809334750e-2],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    miyamoto = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for butane of Miyamoto and "
                    "Watanabe (2001)",
        "__doi__": {"autor": "Miyamoto, H. and Watanabe, K.",
                    "title": "A Thermodynamic Property Model for Fluid-Phase "
                             "n-Butane",
                    "ref": "Int. J. Thermophys., 22(2) (2001) 459-475",
                    "doi": "10.1023/A:1010722814682"},
        "R": 8.314472,
        "cp": Fi3,
        "ref": "IIR",

        "Tmin": 134.87, "Tmax": 589., "Pmax": 69000.0, "rhomax": 13.15,
        "Pmin": 0.000688, "rhomin": 12.652,

        "nr1": [2.952054e-1, -1.32636, -2.031317e-3, 2.240301e-1,
                -3.635425e-2, 1.905841e-3, 7.409154e-5, -1.401175e-6],
        "d1": [1, 1, 2, 2, 3, 5, 8, 8],
        "t1": [-0.25, 1.5, -0.75, 0, 1.25, 1.5, 0.5, 2.5],

        "nr2": [-2.492172, 2.386920, 1.424009e-3, -9.393388e-3, 2.616590e-3,
                -1.977323e-1, -3.809534e-2, 1.523948e-3, -2.391345e-2,
                -9.535229e-3, 3.928384e-5],
        "d2": [3, 3, 8, 5, 6, 1, 5, 7, 2, 3, 15],
        "t2": [1.5, 1.75, -0.25, 3, 3, 4, 2, -1, 2, 19, 5],
        "c2": [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
        "gamma2": [1]*11}

    shortSpan = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for butane of Span "
                    "and Wagner (2003)",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of state for technical applications. "
                             "II. Results for nonpolar fluids.",
                    "ref": "Int. J. Thermophys. 24 (1) (2003) 41-109",
                    "doi": "10.1023/A:1022310214958"},

        "R": 8.31451,
        "cp": Fi2,
        "ref": "OTO",
        "M": 58.123, "rhoc": 227.84/58.123,

        "Tmin": 134.86, "Tmax": 750., "Pmax": 100000.0, "rhomax": 13.20,
        "Pmin": 0.00064578, "rhomin": 12.671,

        "nr1": [0.10626277e1, -0.28620952e1, 0.88738233, -0.12570581,
                0.10286309, 0.25358041e-3],
        "d1": [1, 1, 1, 2, 3, 7],
        "t1": [0.25, 1.125, 1.5, 1.375, 0.25, 0.875],

        "nr2": [0.323252, -0.37950761e-1, -0.32534802, -0.79050969e-1,
                -0.20636721e-1, 0.57053809e-2],
        "d2": [2, 5, 1, 4, 3, 4],
        "t2": [0.625, 1.75, 3.625, 3.625, 14.5, 12.],
        "c2": [1, 1, 2, 2, 3, 3],
        "gamma2": [1]*6}

    polt = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for butane of Polt (1992)",
        "__doi__": {"autor": "Polt, A., Platzer, B., and Maurer, G.",
                    "title": "Parameter der thermischen Zustandsgleichung von "
                             "Bender fuer 14 mehratomige reine Stoffe",
                    "ref": "Chem. Technik 22(1992)6 , 216/224",
                    "doi": ""},
        "R": 8.3143,
        "cp": CP6,
        "ref": "NBP",

        "Tmin": 140.0, "Tmax": 589., "Pmax": 30000.0, "rhomax": 12.81,
        "Pmin": 0.00161, "rhomin": 12.573,

        "nr1": [-0.504188295325, 0.541067401063, -0.760421383062e-1,
                0.846035653528, -0.191317317203e1, 0.521441860186,
                -0.783511318207, 0.689697797175e-1, 0.947825461055e-1,
                -0.141401831669, 0.382675021672, -0.423893176684e-1,
                0.677591792029e-1, 0.567943363340e-1, -0.131517698401,
                0.221136942526e-1],
        "d1": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 5],
        "t1": [3, 4, 5, 0, 1, 2, 3, 4, 0, 1, 2, 0, 1, 0, 1, 1],

        "nr2": [0.504188295325, -0.541067401063, 0.760421383062e-1,
                -0.619109535460e-1, 0.423035373804, -0.390505508895],
        "d2": [0, 0, 0, 2, 2, 2],
        "t2": [3, 4, 5, 3, 4, 5],
        "c2": [2]*6,
        "gamma2": [1.08974964]*6}

    sun = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for butane of Sun and Ely "
                    "(2004)",
        "__doi__": {"autor": "Sun, L. and Ely, J.F.",
                    "title": "Universal equation of state for engineering "
                             "application: Algorithm and  application to "
                             "non-polar and polar fluids",
                    "ref": "Fluid Phase Equilib., 222-223 (2004) 107-118",
                    "doi": "10.1016/j.fluid.2004.06.028"},

        "R": 8.314472,
        "cp": Fi1,
        "ref": "OTO",

        "Tmin": Tt, "Tmax": 620.0, "Pmax": 800000.0, "rhomax": 40.,
        "Pmin": 0.1, "rhomin": 40.,

        "nr1": [1.18936994, 1.05407451, -3.24964532, 8.25263908e-2,
                2.76467405e-4, -8.09869214e-2],
        "d1": [1, 1, 1, 3, 7, 2],
        "t1": [1.5, 0.25, 1.25, 0.25, 0.875, 1.375],

        "nr2": [-9.38097492e-2, 1.46213532e-1, 4.01168502e-1, -1.28716120e-2,
                -0.275191070, -1.62708971e-2, -7.04082962e-2, -2.32871995e-2],
        "d2": [1, 1, 2, 5, 1, 1, 4, 2],
        "t2": [0, 2.375, 2., 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*8}

    # eq = buecker, MBWR, GERG, miyamoto, shortSpan, polt, sun
    eq = buecker, GERG, miyamoto, shortSpan, polt, sun

    _dielectric = {"eq": 3, "Tref": 273.16, "rhoref": 1000.,
                   "a0": [0.0557549],  "expt0": [-1.], "expd0": [1.],
                   "a1": [20.611, 0.02], "expt1": [0, 1], "expd1": [1, 1],
                   "a2": [66.64, 24.44, -7461.2, -1983.6],
                   "expt2": [0, 1, 0, 1], "expd2": [2, 2, 3, 3]}
    _melting = {"eq": 1, "Tref": Tt, "Pref": 0.00066566,
                "Tmin": 134.895, "Tmax": 575.0,
                "a1": [-558558235.4, 558558236.4], "exp1": [0, 2.206],
                "a2": [], "exp2": [], "a3": [], "exp3": []}
    _surface = {"sigma": [0.05138], "exp": [1.209]}
    _vapor_Pressure = {
        "eq": 3,
        "n": [-0.71897e1, 0.26122e1, -0.21729e1, -0.27230e1],
        "t": [1, 1.5, 2., 4.5]}
    _liquid_Density = {
        "eq": 1,
        "n": [0.52341e1, -0.62011e1, 0.36063e1, 0.22137],
        "t": [0.44, 0.6, 0.76, 5.0]}
    _vapor_Density = {
        "eq": 2,
        "n": [-0.27390e1, -0.57347e1, -0.16408e2, -0.46986e2, -0.10090e3],
        "t": [0.39, 1.14, 3.0, 6.5, 14.0]}

    visco0 = {"__name__": "Herrmann (2018)",
              "__doi__": {
                  "autor": "Herrmann, S., Vogel, E.",
                  "title": "New Formulation for the Viscosity of n-Butane",
                  "ref": "J. Phys. Chem. Ref. Data 47(1) (2018) 013104",
                  "doi": "10.1063/1.5020802"},

              "eq": 1, "omega": 0,

              "special0": "_mu0",

              "Tref_virial": 425.125,
              # Special term of virial coefficient, with δ term and μPa·s
              "muref_virial": 4.89736312734e-1/228*M/1e3,
              "n_virial": [-1.9572881000e1, 1.98887362343e2, -8.3176420912e2,
                           1.83218450345e3, -2.26510439059e3, 1.51348864395e3,
                           -4.32819866497e2, 5.19698852489, -3.86579291550e-2],
              "t_virial": [0, -0.25, -0.5, -0.75, -1, -1.25, -1.5, -2.5, -5.5],

              "Tref_res": 425.125, "rhoref_res": 228,
              "nr": [2.3460864383872, 7.8632175809804e-1, 1.5823593499816e1,
                     -9.4670516989296, 1.0511496276340, -1.9355799491084e-2,
                     1.4895031937816e-4],
              "tr": [2, 5, 0, 0, 0, 4, 5],
              "dr": [2, 2, 2.5, 3, 5, 7.5, 10],

              "nr_gaus": [1.2790911462043, 2.5581822924086e-1],
              "br_gaus": [30, 5],
              "er_gaus": [220, 400],

              "special": "_mur"}

    def _mu0(self):
        """Special term for zero-density viscosity for Herrmann correlation"""
        tau = self.Tc/self.T

        # Eq 8
        no = [4.6147656002208, 4.574318591039e-1, 3.0851104723224e-2]
        suma = 0
        for i, n in enumerate(no):
            suma += n*log(tau)**i

        muo = 1.0546549635209e3/tau**0.5/exp(suma)
        return muo

    def _mur(self, rho, T, fase):
        """Special exponential term of residual viscosity for Herrmann
        correlation"""
        tau = self.Tc/T
        delta = rho/self.rhoc
        mur = tau**0.5/delta**(2/3)*1.2280342363570e-3*(delta**5.7*tau)**2
        return mur

    visco1 = {"__name__": "Vogel (1999)",
              "__doi__": {
                  "autor": "Vogel, E., Küchenmeister, C., Bich, E.",
                  "title": "Viscosity correlation for n-Butane in the Fluid "
                           "Region",
                  "ref": "High Temp. - High Pressures 31(2) (1999) 173-186",
                  "doi": "10.1068/htrt154"},

              "eq": 1, "omega": 1,

              "ek": 280.51, "sigma": 0.57335,
              "n_chapman": 0.021357,
              "collision": [0.17067154, -0.48879666, 0.039038856],

              "Tref_virial": 280.51,
              "n_virial": [-19.572881, 219.73999, -1015.3226, 2471.01251,
                           -3375.1717, 2491.6597, -787.26086, 14.085455,
                           -0.34664158],
              "t_virial": [0, -0.25, -0.5, -0.75, -1, -1.25, -1.5, -2.5, -5.5],

              "Tref_res": 425.125, "rhoref_res": 3.92*M,
              "nr": [-54.7737770846, 58.0898623034, 35.2658446259,
                     -39.6682203832, -1.83729542151, -0.833262985358,
                     1.93837020663],
              "tr": [0, 1, 0, 1, 0, 0, 1],
              "dr": [2, 2, 3, 3, 4, 5, 5],

              "CPf": 188.075903903,
              "CPg1": 2.30873963359,
              "CPgi": [0.88101765264], "CPti": [-0.5]}

    visco2 = {"eq": 2, "omega": 2,
              "__name__": "Younglove (1987)",
              "__doi__": {
                  "autor": "Younglove, B.A., Ely, J.F.",
                  "title": "Thermophysical Properties of Fluids. II. Methane, "
                           "Ethane, Propane, Isobutane, and Normal Butane",
                  "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                  "doi": "10.1063/1.555785"},

              "ek": 440., "sigma": 0.503103,
              "n_chapman": 0.20352457/M**0.5,

              "F": [0.1630521851e1, 0.0, 1.40, 425.16],
              "E": [-0.2724386845e2, 0.8012766611e3, 0.2503978646e2,
                    -0.1309704275e5, -0.8313305258e-1, 0.6636975027e2,
                    0.9849317662e4],
              "rhoc": 3.920}

    visco3 = {"__name__": u"Quiñones-Cisneros (2006)",
              "__doi__": {
                  "autor": "Quiñones-Cisneros, S.E., Deiters, U.K.",
                  "title": "Generalization of the Friction Theory for "
                           "Viscosity Modeling",
                  "ref": "J. Phys. Chem. B, 110(25) (2006) 12820-12834",
                  "doi": "10.1021/jp0618577"},

              "eq": 4, "omega": 0,

              "Toref": 425.125,
              "no": [18.3983, -57.1255, 49.3197],
              "to": [0, 0.25, 0.5],

              "a": [-1.34111e-5, -8.56588e-5, 0],
              "b": [1.49860e-4, -1.71134e-4, 0],
              "c": [3.53018e-7, -1.93040e-5, 0],
              "A": [-3.63389e-9, -7.73717e-10, 0],
              "B": [3.70980e-8, 2.07659e-9, 0],
              "C": [-1.12496e-7, 7.66906e-8, 0]}

    _viscosity = visco0, visco1, visco2, visco3

    thermo0 = {"__name__": "Perkins (2002)",
               "__doi__": {
                   "autor": "Perkins, R.A, Ramires, M.L.V., Nieto de Castro, "
                            "C.A., Cusco, L.",
                   "title": "Measurement and Correlation of the Thermal "
                            "Conductivity of Butane from 135 K to 600 K at "
                            "Pressures to 70 MPa",
                   "ref": "J. Chem. Eng. Data 47(5) (2002) 1263-1271",
                   "doi": "10.1021/je0101202"},

               "eq": 1,

               "Toref": 425.16, "koref": 1.,
               "no": [1.62676e-3, 9.75703e-4, 2.89887e-2],
               "to": [0, 1, 2],

               "Tref_res": 425.16, "rhoref_res": 3.92*M, "kref_res": 1.,
               "nr": [-3.04337e-2, 4.18357e-2, 1.65820e-1, -1.47163e-1,
                      -1.48144e-1, 1.33542e-1, 5.25500e-2, -4.85489e-2,
                      -6.29367e-3, 6.44307e-3],
               "tr": [0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
               "dr": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],

               "critical": 3,
               "gnu": 0.63, "gamma": 1.239, "R0": 1.03, "Xio": 0.194e-9,
               "gam0": 0.0496, "qd": 0.875350e-9, "Tcref": 637.68}

    thermo1 = {"__name__": "Younglove (1987)",
               "__doi__": {
                   "autor": "Younglove, B.A., Ely, J.F.",
                   "title": "Thermophysical Properties of Fluids. II. Methane,"
                            " Ethane, Propane, Isobutane, and Normal Butane ",
                   "ref": "J. Phys. Chem. Ref. Data 16(4) (1987) 577-798",
                   "doi": "10.1063/1.555785"},

               "eq": 2,

               "visco": visco1,
               "G": [0.1530992335e1, -0.2114511021],
               "E": [0.4024170074e-2, 0.1561435847e1, -0.6004381127e3,
                     -0.7547260841e-3, -0.2069676662e-1, 0.9382534978e2,
                     -0.1711371457, 0.3647724935e2],

               "critical": 2,
               "X": [0.000769608, 13.2533, 0.485554, 1.01021],
               "Z": 9.10218e-10}

    _thermal = thermo0, thermo1


class Test(TestCase):

    def test_buecker(self):
        # Selected point from Table 44, Pag 974, saturation state
        st = nC4(T=136, x=0.5)
        self.assertEqual(round(st.P.MPa, 8), 0.00000082)
        self.assertEqual(round(st.Liquido.rho, 4), 733.9269)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), -719.46)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), -3.020)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 1.442)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 1.974)
        self.assertEqual(round(st.Liquido.w, 2), 1819.41)
        self.assertEqual(round(st.Gas.rho, 6), 0.000042)
        self.assertEqual(round(st.Gas.h.kJkg, 2), -224.49)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), 0.619)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 0.967)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 1.110)
        self.assertEqual(round(st.Gas.w, 2), 149.44)

        st = nC4(T=220, x=0.5)
        self.assertEqual(round(st.P.MPa, 6), 0.007805)
        self.assertEqual(round(st.Liquido.rho, 3), 654.775)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), -549.07)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), -2.047)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 1.505)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 2.113)
        self.assertEqual(round(st.Liquido.w, 2), 1326.20)
        self.assertEqual(round(st.Gas.rho, 5), 0.24959)
        self.assertEqual(round(st.Gas.h.kJkg, 2), -120.52)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), -0.099)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 1.244)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 1.392)
        self.assertEqual(round(st.Gas.w, 2), 186.44)

        st = nC4(T=300, x=0.5)
        self.assertEqual(round(st.P.MPa, 5), 0.25760)
        self.assertEqual(round(st.Liquido.rho, 2), 570.68)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), -367.83)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), -1.349)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 1.729)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 2.451)
        self.assertEqual(round(st.Liquido.w, 2), 890.88)
        self.assertEqual(round(st.Gas.rho, 4), 6.5164)
        self.assertEqual(round(st.Gas.h.kJkg, 2), -8.24)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), -0.150)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 1.602)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 1.811)
        self.assertEqual(round(st.Gas.w, 2), 202.15)

        st = nC4(T=400, x=0.5)
        self.assertEqual(round(st.P.MPa, 4), 2.4954)
        self.assertEqual(round(st.Liquido.rho, 2), 408.48)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), -80.60)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), -0.542)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 2.173)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 3.838)
        self.assertEqual(round(st.Liquido.w, 2), 318.35)
        self.assertEqual(round(st.Gas.rho, 3), 73.077)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 113.39)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), -0.057)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 2.210)
        self.assertEqual(round(st.Gas.cp.kJkgK, 3), 3.623)
        self.assertEqual(round(st.Gas.w, 2), 154.77)

        st = nC4(T=425, x=0.5)
        self.assertEqual(round(st.P.MPa, 4), 3.7881)
        self.assertEqual(round(st.Liquido.rho, 2), 250.17)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 50.78)
        self.assertEqual(round(st.Liquido.s.kJkgK, 3), -0.235)
        self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 2.534)
        self.assertEqual(round(st.Liquido.cp.kJkgK, 2), 375.35)
        self.assertEqual(round(st.Liquido.w, 2), 114.85)
        self.assertEqual(round(st.Gas.rho, 2), 205.54)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 73.93)
        self.assertEqual(round(st.Gas.s.kJkgK, 3), -0.180)
        self.assertEqual(round(st.Gas.cv.kJkgK, 3), 2.589)
        self.assertEqual(round(st.Gas.cp.kJkgK, 2), 460.13)
        self.assertEqual(round(st.Gas.w, 2), 112.63)

        # Selected point from Table 45, Pag 980
        st = nC4(T=135, P=1e5)
        self.assertEqual(round(st.rho, 2), 734.90)
        self.assertEqual(round(st.u.kJkg, 2), -721.46)
        self.assertEqual(round(st.h.kJkg, 2), -721.32)
        self.assertEqual(round(st.s.kJkgK, 4), -3.0349)
        self.assertEqual(round(st.cv.kJkgK, 4), 1.4416)
        self.assertEqual(round(st.cp.kJkgK, 4), 1.9729)
        self.assertEqual(round(st.w, 2), 1826.47)

        st = nC4(T=320, P=5e5)
        self.assertEqual(round(st.rho, 2), 546.46)
        self.assertEqual(round(st.u.kJkg, 2), -318.37)
        self.assertEqual(round(st.h.kJkg, 2), -317.45)
        self.assertEqual(round(st.s.kJkgK, 4), -1.1876)
        self.assertEqual(round(st.cv.kJkgK, 4), 1.8027)
        self.assertEqual(round(st.cp.kJkgK, 4), 2.5760)
        self.assertEqual(round(st.w, 2), 784.25)

        st = nC4(T=360, P=1e6)
        self.assertEqual(round(st.rho, 3), 23.804)
        self.assertEqual(round(st.u.kJkg, 3), 39.201)
        self.assertEqual(round(st.h.kJkg, 3), 81.210)
        self.assertEqual(round(st.s.kJkgK, 6), -0.048237)
        self.assertEqual(round(st.cv.kJkgK, 4), 1.9129)
        self.assertEqual(round(st.cp.kJkgK, 4), 2.2666)
        self.assertEqual(round(st.w, 2), 197.12)

        st = nC4(T=575, P=2e6)
        self.assertEqual(round(st.rho, 3), 25.876)
        self.assertEqual(round(st.u.kJkg, 2), 535.89)
        self.assertEqual(round(st.h.kJkg, 2), 613.18)
        self.assertEqual(round(st.s.kJkgK, 4), 1.0083)
        self.assertEqual(round(st.cv.kJkgK, 4), 2.7050)
        self.assertEqual(round(st.cp.kJkgK, 4), 2.9097)
        self.assertEqual(round(st.w, 2), 279.37)

        st = nC4(T=330, P=5e6)
        self.assertEqual(round(st.rho, 2), 544.15)
        self.assertEqual(round(st.u.kJkg, 2), -298.77)
        self.assertEqual(round(st.h.kJkg, 2), -289.58)
        self.assertEqual(round(st.s.kJkgK, 4), -1.1272)
        self.assertEqual(round(st.cv.kJkgK, 4), 1.8433)
        self.assertEqual(round(st.cp.kJkgK, 4), 2.5833)
        self.assertEqual(round(st.w, 2), 793.83)

        st = nC4(T=140, P=1e7)
        self.assertEqual(round(st.rho, 2), 734.35)
        self.assertEqual(round(st.u.kJkg, 2), -713.92)
        self.assertEqual(round(st.h.kJkg, 2), -700.30)
        self.assertEqual(round(st.s.kJkgK, 4), -2.9800)
        self.assertEqual(round(st.cv.kJkgK, 4), 1.4519)
        self.assertEqual(round(st.cp.kJkgK, 4), 1.9720)
        self.assertEqual(round(st.w, 2), 1829.40)

        st = nC4(T=475, P=5e7)
        self.assertEqual(round(st.rho, 2), 501.63)
        self.assertEqual(round(st.u.kJkg, 3), 35.722)
        self.assertEqual(round(st.h.kJkg, 2), 135.40)
        self.assertEqual(round(st.s.kJkgK, 5), -0.28209)
        self.assertEqual(round(st.cv.kJkgK, 4), 2.4314)
        self.assertEqual(round(st.cp.kJkgK, 4), 2.9384)
        self.assertEqual(round(st.w, 2), 826.87)

    def test_shortSpan(self):
        # Table III, Pag 46
        st = nC4(T=700, rho=200, eq="shortSpan")
        self.assertEqual(round(st.cp0.kJkgK, 4), 3.2176)
        self.assertEqual(round(st.P.MPa, 3), 18.416)
        self.assertEqual(round(st.cp.kJkgK, 4), 3.5758)

        st2 = nC4(T=750, rho=100, eq="shortSpan")
        self.assertEqual(round(st2.h.kJkg-st.h.kJkg, 2), 213.78)
        self.assertEqual(round(st2.s.kJkgK-st.s.kJkgK, 5), 0.37465)

    def test_custom(self):
        """Test for other model not tested"""
        # Reference state for Miyamoto correlation
        st = nC4(T=273.15, x=0.0, eq="miyamoto")
        self.assertEqual(round(st.h.kJkg, 0), 200)
        self.assertEqual(round(st.s.kJkgK, 2), 1)

    def test_herrmann(self):
        # Table 6, Pag 18
        self.assertEqual(round(nC4(T=136, rho=735).mu.muPas, 3), 2310.306)
        self.assertEqual(round(nC4(T=300, rho=1).mu.muPas, 6), 7.440574)
        self.assertEqual(round(nC4(T=300, rho=6).mu.muPas, 6), 7.382406)
        self.assertEqual(round(nC4(T=300, rho=575).mu.muPas, 4), 162.2565)
        self.assertEqual(round(nC4(T=300, rho=640).mu.muPas, 4), 290.5562)
        self.assertEqual(round(nC4(T=400, rho=1).mu.muPas, 6), 9.860115)
        self.assertEqual(round(nC4(T=400, rho=70).mu.muPas, 5), 11.25890)
        self.assertEqual(round(nC4(T=400, rho=410).mu.muPas, 5), 56.96791)
        self.assertEqual(round(nC4(T=400, rho=570).mu.muPas, 4), 153.0508)
        self.assertEqual(round(nC4(T=425.125, rho=228).mu.muPas, 5), 24.84327)
        self.assertEqual(round(nC4(T=500, rho=1).mu.muPas, 5), 12.20820)
        self.assertEqual(round(nC4(T=500, rho=100).mu.muPas, 5), 15.51795)
        self.assertEqual(round(nC4(T=500, rho=500).mu.muPas, 5), 96.94796)
        self.assertEqual(round(nC4(T=650, rho=1).mu.muPas, 5), 15.62218)
        self.assertEqual(round(nC4(T=650, rho=100).mu.muPas, 5), 19.43536)
        self.assertEqual(round(nC4(T=650, rho=475).mu.muPas, 5), 86.78013)
