#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from math import exp, log
import sqlite3
from ConfigParser import ConfigParser
from functools import partial

from PyQt4 import QtCore, QtGui
from scipy.constants import lb
from scipy.special import erf

from tools import UI_databank
from tools.UI_psychrometry import PsychroInput
from lib.corriente import Corriente, Mezcla, Solid
from lib.psycrometry import PsychroState, PsyState
from lib import unidades, config
from lib.utilities import representacion
from lib.thread import Evaluate
from UI import texteditor
from UI.delegate import CellEditor
from UI.widgets import Tabla, Entrada_con_unidades, Status
    

###Estándares de filtros, unidades en mm
Tyler=[0.033, 0.043, 0.053, 0.061, 0.074, 0.088, 0.104, 0.121, 0.147, 0.173, 0.208, 0.246, 0.295, 0.351, 0.417, 0.495, 0.589, 0.701, 0.833, 0.991, 1.168, 1.397, 1.651, 1.981, 2.362, 2.794, 3.327, 3.962, 4.699, 5.613, 6.680, 7.925]
#ASTM E 11-70
ASTM=[0.02, 0.025, 0.032, 0.038, 0.045, 0.053, 0.063, 0.075, 0.09, 0.106, 0.125, 0.150, 0.180, 0.212, 0.250, 0.300, 0.355, 0.425, 0.5, 0.6, 0.71, 0.85, 1., 1.18, 1.4, 1.7, 2., 2.36, 2.8, 3.35, 4., 4.75, 5.6, 6.3, 6.7, 8., 9.5, 11.2, 12.5, 13.2, 16.0, 19., 22.4, 25., 26.5, 31.5, 37.5, 45., 50., 53., 63., 75., 90., 100., 106., 125]
#DIN 4188
DIN=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.04, 0.045, 0.05, 0.056, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.5, 0.56, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 2.8, 3.15, 3.55, 4., 4.5, 5., 5.6]
#AFNOR NFX11-501
AFNOR=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.04, 0.045, 0.05, 0.056, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.16, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.45, 0.5, 0.56, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 3.15, 3.55, 4., 4.5, 5., 5.6]
#ISO 565
ISO=[0.02, 0.022, 0.025, 0.028, 0.032, 0.036, 0.045, 0.05, 0.063, 0.071, 0.08, 0.09, 0.1, 0.125, 0.14, 0.18, 0.2, 0.224, 0.25, 0.28, 0.315, 0.355, 0.4, 0.45, 0.63, 0.71, 0.8, 0.9, 1.0, 1.18, 1.25, 1.4, 1.6, 1.8, 2., 2.24, 2.5, 2.8, 3.15, 3.55, 4., 4.5, 5., 5.6]
#BS 410
BS=[0.045, 0.053, 0.063, 0.075, 0.09, 0.106, 0.125, 0.15, 0.18, 0.212, 0.25, 0.3, 0.355, 0.425, 0.5, 0.6, 0.71, 0.85, 1.0, 1.18, 1.4, 1.7, 2.0, 2.36, 2.8, 3.35, 4.0, 4.75, 5.6]



class Dialog_Distribucion(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog_Distribucion, self).__init__(parent)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Generate solid distribution"))
        self.matriz=[]
        
        layout = QtGui.QGridLayout(self)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Model")),0,0,1,1)
        self.modelo=QtGui.QComboBox()
        layout.addWidget(self.modelo, 0, 1, 1, 1)
        self.stacked = QtGui.QStackedWidget()
        self.modelo.currentIndexChanged.connect(self.stacked.setCurrentIndex)
        layout.addWidget(self.stacked, 1, 0, 1, 2)
        
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Standards:")),2,0,1,1)
        self.standard=QtGui.QComboBox()
        self.standard.addItem("Tyler")
        self.standard.addItem("ASTM")
        self.standard.addItem("DIN")
        self.standard.addItem("BS")
        self.standard.addItem("AFNOR")
        self.standard.addItem("ISO")
        self.standard.addItem(QtGui.QApplication.translate("pychemqt", "Custom"))
        self.standard.currentIndexChanged.connect(self.standardCambiado)
        layout.addWidget(self.standard, 2, 1, 1, 1)
        
        self.diametros = QtGui.QLineEdit()
        layout.addWidget(self.diametros, 3, 1, 1, 2)
        
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),4,1,1,3)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.aceptar)
        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        
        self.rosin=QtGui.QWidget()
        self.stacked.addWidget(self.rosin)
        self.modelo.addItem("Rosin Rammler Sperling")
        layout = QtGui.QGridLayout(self.rosin)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("S="),2,1,1,1)
        self.rosinEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.rosinEntries[0],1,2,1,1)
        layout.addWidget(self.rosinEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)
        
        self.gates=QtGui.QWidget()
        self.stacked.addWidget(self.gates)
        self.modelo.addItem("Gates Gaudin Schumann")
        layout = QtGui.QGridLayout(self.gates)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.gatesEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.gatesEntries[0],1,2,1,1)
        layout.addWidget(self.gatesEntries[1],2,2,1,1)
        
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.broadbent=QtGui.QWidget()
        self.stacked.addWidget(self.broadbent)
        self.modelo.addItem("Broadbent Callcott")
        layout = QtGui.QGridLayout(self.broadbent)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.broadbentEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.broadbentEntries[0],1,2,1,1)
        layout.addWidget(self.broadbentEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.gaudin=QtGui.QWidget()
        self.stacked.addWidget(self.gaudin)
        self.modelo.addItem("Gaudin Meloy")
        layout = QtGui.QGridLayout(self.gaudin)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),2,1,1,1)
        self.gaudintEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.gaudintEntries[0],1,2,1,1)
        layout.addWidget(self.gaudintEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.logaritmic=QtGui.QWidget()
        self.stacked.addWidget(self.logaritmic)
        self.modelo.addItem("Lognormal")
        layout = QtGui.QGridLayout(self.logaritmic)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel(u"σ="),2,1,1,1)
        self.logaritmicEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float)]
        layout.addWidget(self.logaritmicEntries[0],1,2,1,1)
        layout.addWidget(self.logaritmicEntries[1],2,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)

        self.harris=QtGui.QWidget()
        self.stacked.addWidget(self.harris)
        self.modelo.addItem("Harris")
        layout = QtGui.QGridLayout(self.harris)
        layout.addWidget(QtGui.QLabel("d*="),1,1,1,1)
        layout.addWidget(QtGui.QLabel("S="),2,1,1,1)
        layout.addWidget(QtGui.QLabel("N="),3,1,1,1)
        self.harrisEntries=[Entrada_con_unidades(unidades.Length, "ParticleDiameter"), Entrada_con_unidades(float), Entrada_con_unidades(float)]
        layout.addWidget(self.harrisEntries[0],1,2,1,1)
        layout.addWidget(self.harrisEntries[1],2,2,1,1)
        layout.addWidget(self.harrisEntries[2],3,2,1,1)
        layout.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),5,1,1,3)
        
        self.standardCambiado(0)
        
    def standardCambiado(self, estandar):
        if estandar==6:
            self.diametros.setEnabled(True)
        else:
            self.diametros.setEnabled(False)
            self.estandares=[Tyler, ASTM, DIN, BS, AFNOR, ISO][estandar]
    
    def aceptar(self):
        if self.standard.currentIndex()<6:
            d=self.estandares
        else:
            pass
        if self.modelo.currentIndex()==0:
            funcion = lambda p, d: 1.-exp(-(d/p[0]/1000.)**p[1])
            parametros=[i.value for i in self.rosinEntries]
        elif self.modelo.currentIndex()==1:
            funcion = lambda p, d: (d/p[0]/1000.)**p[1]
            parametros=[i.value for i in self.gatesEntries]
        elif self.modelo.currentIndex()==2:
            funcion = lambda p, d: 1-(1-d/p[0]/1000.)**p[1]
            parametros=[i.value for i in self.broadbentEntries]
        elif self.modelo.currentIndex()==3:
            funcion = lambda p, d: 1.-exp(-(d/p[0]/1000.)**p[1])/(1-exp(-1.))
            parametros=[i.value for i in self.gaudintEntries]
        elif self.modelo.currentIndex()==4:
            funcion = lambda p, d: erf(log(d/p[0]/1000.)/p[1]) 
            parametros=[i.value for i in self.logaritmicEntries]
        elif self.modelo.currentIndex()==5:
            funcion = lambda p, d: 1-(1-d/(p[0]/1000.)**p[1])**p[2]
            parametros=[i.value for i in self.harrisEntries]
        
        diametros=[unidades.Length(x) for x in d ]
        acumulado=[0]+[funcion(parametros, x) for x in d]
        if acumulado[-1]<1.:
            acumulado[-1]=1.
        diferencia=[acumulado[i+1]-acumulado[i] for i in range(len(d))]
        self.matriz=[[diametros[i].config("Diameter"), diferencia[i]] for i in range(len(d))]
        self.accept()




class Ui_corriente(QtGui.QWidget):
    Changed = QtCore.pyqtSignal(Corriente)
    def __init__(self, corriente=None, readOnly=False, parent=None):
        super(Ui_corriente, self).__init__(parent)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Stream"))
        self.readOnly=readOnly
        self.semaforo=QtCore.QSemaphore(1)
        self.evaluate=Evaluate()
        self.evaluate.finished.connect(self.repaint)

        self.indices, self.nombres, M=config.getComponents()
        self.solidos, self.nombreSolidos, MSolidos=config.getComponents(solidos=True)

        gridLayout1 = QtGui.QVBoxLayout(self)
        self.toolBox = QtGui.QToolBox()
        gridLayout1.addWidget(self.toolBox)

        #Caracteristicas principales
        self.PagePrincipales = QtGui.QWidget()
        grid_Principal = QtGui.QGridLayout(self.PagePrincipales)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Temperature")),1,1,1,1)
        self.T=Entrada_con_unidades(unidades.Temperature, readOnly=readOnly)
        self.T.valueChanged.connect(partial(self.calculo, "T"))
        grid_Principal.addWidget(self.T,1,2,1,1)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Pressure")),2,1,1,1)
        self.P=Entrada_con_unidades(unidades.Pressure, readOnly=readOnly)
        self.P.valueChanged.connect(partial(self.calculo, "P"))
        grid_Principal.addWidget(self.P,2,2,1,1)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Vapor fraccion")),3,1,1,1)
        self.x=Entrada_con_unidades(float, readOnly=readOnly)
        self.x.valueChanged.connect(partial(self.calculo, "x"))
        grid_Principal.addWidget(self.x,3,2,1,1)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Mass flow")),1,4,1,1)
        self.caudal=Entrada_con_unidades(unidades.MassFlow, readOnly=readOnly)
        self.caudal.valueChanged.connect(partial(self.calculo, "caudalMasico"))
        grid_Principal.addWidget(self.caudal,1,5,1,1)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Molar flow")),2,4,1,1)
        self.caudalMolar=Entrada_con_unidades(unidades.MolarFlow, readOnly=readOnly)
        self.caudalMolar.valueChanged.connect(partial(self.calculo, "caudalMolar"))
        grid_Principal.addWidget(self.caudalMolar,2,5,1,1)
        grid_Principal.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Volumetric flow")),3,4,1,1)
        self.caudalVol=Entrada_con_unidades(unidades.VolFlow, "volliq", readOnly=readOnly)
        self.caudalVol.valueChanged.connect(partial(self.calculo, "caudalVolumetrico"))
        grid_Principal.addWidget(self.caudalVol,3,5,1,1)
        
        grid_Principal.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),4,1,1,1)
        self.tipoFraccion = QtGui.QComboBox()
        self.tipoFraccion.addItem("kg/h")
        self.tipoFraccion.addItem("kmol/h")
        self.tipoFraccion.addItem("lb/h")
        self.tipoFraccion.addItem("lbmol/h")
        self.tipoFraccion.addItem(QtGui.QApplication.translate("pychemqt", "Mass fraction"))
        self.tipoFraccion.addItem(QtGui.QApplication.translate("pychemqt", "Molar fraction"))
        self.tipoFraccion.setCurrentIndex(5)
        self.tipoFraccion.currentIndexChanged.connect(self.tipoFraccionesCambiado)
        
        self.TablaComposicion=Tabla(1, verticalHeaderLabels=[""]+self.nombres, filas=len(self.nombres)+1)
        self.TablaComposicion.setFixedHeight(22*len(self.indices)+22+4)
        self.TablaComposicion.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.MinimumExpanding)
        self.TablaComposicion.editingFinished.connect(self.valueTablaFraccionesChanged)
        self.TablaComposicion.setCellWidget(0, 0, self.tipoFraccion)
        grid_Principal.addWidget(self.TablaComposicion,5,1,1,2)
        grid_Principal.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),6,0,1,5)
        self.toolBox.addItem(self.PagePrincipales,QtGui.QApplication.translate("pychemqt", "Definition"))
        
        #Solidos
        self.pageSolidos = QtGui.QWidget()
        grid_Solidos = QtGui.QGridLayout(self.pageSolidos)
        
        self.TablaSolidos=Tabla(1, horizontalHeader=[QtGui.QApplication.translate("pychemqt", "Mass flow")+", "+unidades.MassFlow.text()], verticalHeaderLabels=self.nombreSolidos, filas=len(self.solidos), stretch=False)
        self.TablaSolidos.setFixedHeight(22*len(self.solidos)+24+4)
        self.CaudalSolidos=[]
        for i in range(len(self.nombreSolidos)):
            widget=Entrada_con_unidades(unidades.MassFlow, retornar=False, texto=False, boton=False, width=self.TablaSolidos.columnWidth(0))
            widget.valueChanged.connect(self.caudalesSolidoFinished)
            self.CaudalSolidos.append(widget)
            self.TablaSolidos.setCellWidget(i, 0, widget)
        grid_Solidos.addWidget(self.TablaSolidos, 1, 1, 1, 2)
        grid_Solidos.addItem(QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed),2,4)
        self.checkDistribucion = QtGui.QCheckBox(QtGui.QApplication.translate("pychemqt", "Use particle size distribution"))
        self.checkDistribucion.toggled.connect(self.checkDistributionToggled)
        grid_Solidos.addWidget(self.checkDistribucion,3,1,1,4)

        self.distribucionTamanos = Tabla(2, [QtGui.QApplication.translate("pychemqt", "Diameter")+", "+unidades.Length(None).text("ParticleDiameter"), QtGui.QApplication.translate("pychemqt", "Fraction")], verticalHeader=False)
        self.distribucionTamanos.rowFinished.connect(self.diametro_medio)
        self.distribucionTamanos.editingFinished.connect(self.distribucionFinished)
        grid_Solidos.addWidget(self.distribucionTamanos,4,1,4,2)
        self.botonNormalizar = QtGui.QPushButton(QtGui.QApplication.translate("pychemqt", "Normalize"))
        self.botonNormalizar.clicked.connect(self.botonNormalizar_clicked)
        grid_Solidos.addWidget(self.botonNormalizar,5,3,1,1)
        self.botonGenerar = QtGui.QPushButton(QtGui.QApplication.translate("pychemqt", "Generate"))
        self.botonGenerar.clicked.connect(self.botonGenerar_clicked)
        grid_Solidos.addWidget(self.botonGenerar,6,3,1,1)

        grid_Solidos.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed),7,1,1,1)        
        grid_Solidos.addWidget(QtGui.QLabel(QtGui.QApplication.translate("pychemqt", "Mean Diameter")),8,1,1,1)
        self.diametroParticula=Entrada_con_unidades(unidades.Length, "ParticleDiameter")
        self.diametroParticula.valueChanged.connect(partial(self.calculo, "diametroMedio"))
        grid_Solidos.addWidget(self.diametroParticula,8,2,1,2)  
        grid_Solidos.addItem(QtGui.QSpacerItem(10,10,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),9,1,1,7)
        self.toolBox.addItem(self.pageSolidos,QtGui.QApplication.translate("pychemqt", "Solid"))
        self.pageSolidos.setEnabled(len(self.solidos))


        #Electrolitos
#        self.PageElectrolitos = QtGui.QWidget()
#        self.gridLayout_Electrolitos = QtGui.QGridLayout(self.PageElectrolitos)
#        self.label_5 = QtGui.QLabel(self.PageElectrolitos)
#        self.label_5.setText(QtGui.QApplication.translate("pychemqt", "No implementado"))
#        self.gridLayout_Electrolitos.addWidget(self.label_5,0,0,1,1)
#        self.toolBox.addItem(self.PageElectrolitos,"")
#        self.toolBox.setItemText(self.toolBox.indexOf(self.PageElectrolitos), QtGui.QApplication.translate("pychemqt", "Electrolitos"))

        #Propiedades
        self.PagePropiedades = QtGui.QWidget()
        self.gridLayout_Propiedades = QtGui.QGridLayout(self.PagePropiedades)
        self.TablaPropiedades=QtGui.QTableWidget(11, 2)
        for i in range(self.TablaPropiedades.rowCount()):
            self.TablaPropiedades.setRowHeight(i, 24)
        self.TablaPropiedades.setColumnWidth(0, 85)
        self.TablaPropiedades.setColumnWidth(1, 85)
        self.TablaPropiedades.setFixedHeight(11*24+28)
        self.TablaPropiedades.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.TablaPropiedades.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.TablaPropiedades.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.TablaPropiedades.horizontalHeader().resizeSections(QtGui.QHeaderView.Fixed)
        self.TablaPropiedades.setHorizontalHeaderLabels([QtGui.QApplication.translate("pychemqt", "Liquid"), QtGui.QApplication.translate("pychemqt", "Vapor")])
        self.TablaPropiedades.setVerticalHeaderLabels([QtGui.QApplication.translate("pychemqt", "Mass Flow") + ", " + unidades.MassFlow(None).text(), QtGui.QApplication.translate("pychemqt", "Molar Flow") + ", " + unidades.MolarFlow(None).text(), QtGui.QApplication.translate("pychemqt", "Vol Flow") + ", " + unidades.VolFlow(None).text("QLiq"), QtGui.QApplication.translate("pychemqt", "Enthalpy")+ ", "+ unidades.Power(None).text(), QtGui.QApplication.translate("pychemqt", "Molecular Weight"), QtGui.QApplication.translate("pychemqt", "Density")+ ", " + unidades.Density(None).text("DenLiq"), QtGui.QApplication.translate("pychemqt", "Compressibility"), QtGui.QApplication.translate("pychemqt", "Cp") + ", " + unidades.SpecificHeat(None).text(), QtGui.QApplication.translate("pychemqt", "Viscosity") +", "+ unidades.Viscosity(None).text(), QtGui.QApplication.translate("pychemqt", "Conductivity") +", "+ unidades.ThermalConductivity(None).text(), QtGui.QApplication.translate("pychemqt", "Tension")+", "+ unidades.Tension(None).text()])

        self.CaudalLiquido=Entrada_con_unidades(unidades.MassFlow, retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(0, 0, self.CaudalLiquido)
        self.CaudalGas=Entrada_con_unidades(unidades.MassFlow, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(0, 1, self.CaudalGas)
        self.CaudalMolarLiquido=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(1, 0, self.CaudalMolarLiquido)
        self.CaudalMolarGas=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(1, 1, self.CaudalMolarGas)
        self.CaudalVolumetricoLiquido=Entrada_con_unidades(unidades.VolFlow, "QLiq", retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(2, 0, self.CaudalVolumetricoLiquido)
        self.CaudalVolumetricoGas=Entrada_con_unidades(unidades.VolFlow, "QLiq", retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(2, 1, self.CaudalVolumetricoGas)
        self.entalpiaLiquido=Entrada_con_unidades(unidades.Power, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(3, 0, self.entalpiaLiquido)
        self.entalpiaGas=Entrada_con_unidades(unidades.Power, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(3, 1, self.entalpiaGas)
        self.PesoMolecularLiquido=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(4, 0, self.PesoMolecularLiquido)
        self.PesoMolecularGas=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(4, 1, self.PesoMolecularGas)
        self.DensidadLiquido=Entrada_con_unidades(unidades.Density, "DenLiq", retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(5, 0, self.DensidadLiquido)
        self.DensidadGas=Entrada_con_unidades(unidades.Density, "DenLiq", retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(5, 1, self.DensidadGas)
        self.ZLiquido=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(6, 0, self.ZLiquido)
        self.ZGas=Entrada_con_unidades(float, readOnly=True)
        self.TablaPropiedades.setCellWidget(6, 1, self.ZGas)
        self.CpLiquido=Entrada_con_unidades(unidades.SpecificHeat, retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(7, 0, self.CpLiquido)
        self.CpGas=Entrada_con_unidades(unidades.SpecificHeat, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(7, 1, self.CpGas)
        self.ViscosidadLiquido=Entrada_con_unidades(unidades.Viscosity, retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(8, 0, self.ViscosidadLiquido)
        self.ViscosidadGas=Entrada_con_unidades(unidades.Viscosity, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(8, 1, self.ViscosidadGas)
        self.ConductividadLiquido=Entrada_con_unidades(unidades.ThermalConductivity, retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(9, 0, self.ConductividadLiquido)
        self.ConductividadGas=Entrada_con_unidades(unidades.ThermalConductivity, retornar=False, readOnly=True, boton=False, texto=False)
        self.TablaPropiedades.setCellWidget(9, 1, self.ConductividadGas)
        self.Tension=Entrada_con_unidades(unidades.Tension, retornar=False, readOnly=True, texto=False, boton=False)
        self.TablaPropiedades.setCellWidget(10, 0, self.Tension)
        self.gridLayout_Propiedades.addWidget(self.TablaPropiedades,1,1,1,1)
        self.gridLayout_Propiedades.addItem(QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding),2,0,1,3)
        self.toolBox.addItem(self.PagePropiedades,
            QtGui.QIcon(os.environ["pychemqt"] + "/images/button/helpAbout.png"),
            QtGui.QApplication.translate("pychemqt", "Properties"))

        
        #Notas
        self.PageNotas = texteditor.TextEditor()
        self.toolBox.addItem(self.PageNotas,QtGui.QIcon(os.environ["pychemqt"]+"/images/button/editor.png"), QtGui.QApplication.translate("pychemqt", "Notes"))
        
        if corriente:
            self.setCorriente(corriente)
        else:
            self.corriente=Corriente()
        self.distribucionTamanos.setConnected()
        self.setReadOnly(self.readOnly)
        self.PageNotas.textChanged.connect(self.corriente.setNotas)


    def setReadOnly(self, bool):
        if bool:
            self.TablaComposicion.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.TablaSolidos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            self.distribucionTamanos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        else:
            self.TablaComposicion.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
            self.TablaSolidos.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
            self.distribucionTamanos.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)

    
    def setCorriente(self, corriente):
        if corriente:
            self.corriente=corriente
            self.repaint()
        
    def repaint(self):
        if self.semaforo.available()>0:
            self.semaforo.acquire(1)
        if self.corriente.status==1:
                self.T.setValue(self.corriente.T)
                self.P.setValue(self.corriente.P)
                self.caudal.setValue(self.corriente.caudalmasico)
                self.caudalMolar.setValue(self.corriente.caudalmolar)
                self.caudalVol.setValue(self.corriente.Q)
                
                self.TablaComposicion.item(0, 0).setText("0")
                fracciones = self.corriente.mezcla.recallZeros(self.corriente.fraccion)
                for i, fraccion in enumerate(fracciones):
                    self.TablaComposicion.item(i+1, 0).setText(representacion(fraccion))
                
                self.x.setValue(self.corriente.x)
                self.PageNotas.setText(self.corriente.notas)
                
                if self.corriente.solido:
                    for i, caudal in enumerate(self.corriente.solido.caudalUnitario):
                        self.CaudalSolidos[i].setValue(caudal)
                    if self.corriente.tipoSolido==1:
                        self.checkDistribucion.setChecked(False)
                    else:
                        self.checkDistribucion.setChecked(True)
                    if self.corriente.solido.diametros:
                        diametros=[d.config("ParticleDiameter") for d in self.corriente.solido.diametros]
                        self.distribucionTamanos.setColumn(0, diametros)
                        self.distribucionTamanos.setColumn(1, self.corriente.solido.fracciones)
                    self.diametroParticula.setValue(self.corriente.solido.diametro_medio)
                    
                if self.corriente.x>0:
                    self.CaudalGas.setValue(self.corriente.Gas.caudalmasico)
                    self.CaudalMolarGas.setValue(self.corriente.Gas.caudalmolar)
                    self.entalpiaGas.setValue(self.corriente.Gas.h)
                    self.PesoMolecularGas.setValue(self.corriente.Gas.M)
                    self.DensidadGas.setValue(self.corriente.Gas.rho)
                    self.CaudalVolumetricoGas.setValue(self.corriente.Gas.Q)
                    self.ZGas.setValue(self.corriente.Gas.Z)
                    self.CpGas.setValue(self.corriente.Gas.cp)
                    self.ViscosidadGas.setValue(self.corriente.Gas.mu)
                    self.ConductividadGas.setValue(self.corriente.Gas.k)
                if self.corriente.x<1:
                    self.CaudalLiquido.setValue(self.corriente.Liquido.caudalmasico)
                    self.CaudalMolarLiquido.setValue(self.corriente.Liquido.caudalmolar)
                    self.entalpiaLiquido.setValue(self.corriente.Liquido.h)
                    self.PesoMolecularLiquido.setValue(self.corriente.Liquido.M)
                    self.DensidadLiquido.setValue(self.corriente.Liquido.rho)
                    self.CaudalVolumetricoLiquido.setValue(self.corriente.Liquido.Q)
                    self.ZLiquido.setValue(self.corriente.Liquido.Z)
                    self.CpLiquido.setValue(self.corriente.Liquido.cp)
                    self.ViscosidadLiquido.setValue(self.corriente.Liquido.mu)
                    self.ConductividadLiquido.setValue(self.corriente.Liquido.k)
                    self.Tension.setValue(self.corriente.Liquido.epsilon)
                    
                if isinstance(self, QtGui.QDialog):
                    self.status.setState(1)
                self.Changed.emit(self.corriente)

        elif self.corriente.numInputs:
            self.T.setValue(self.corriente.kwargs["T"])
            self.P.setValue(self.corriente.kwargs["P"])
            if self.corriente.kwargs["x"]!=None:
                self.x.setValue(self.corriente.kwargs["x"])
            self.caudal.setValue(self.corriente.kwargs["caudalMasico"])
            self.caudalMolar.setValue(self.corriente.kwargs["caudalVolumetrico"])
            self.caudalVol.setValue(self.corriente.kwargs["caudalMolar"])
            
#                    "caudalUnitarioMolar": [],
#                    "caudalUnitarioMasico": [],
#                    "fraccionMolar": [],
#                    "fraccionMasica": [],
#                    "mezcla": None,
#
#                    "solido": None,
#                    "caudalSolido": [],
#                    "diametroMedio": 0.0,
#                    "distribucion_fraccion": [],
#                    "distribucion_diametro": []}
#
            
#            for key, value in self.kwargs.iteritems():
#                if key not in self.kwargs_forbidden and value:  
#                    count+=1

        if isinstance(self, QtGui.QDialog):
            self.status.setState(self.corriente.status, self.corriente.msg)

        if self.corriente.tipoSolido:
            for i, caudal in enumerate(self.corriente.solido.caudalUnitario):
                self.CaudalSolidos[i].setValue(caudal)
            if self.corriente.tipoSolido==1:
                self.checkDistribucion.setChecked(False)
            else:
                self.checkDistribucion.setChecked(True)
            if self.corriente.solido.diametros:
                diametros=[d.config("ParticleDiameter") for d in self.corriente.solido.diametros]
                self.distribucionTamanos.setColumn(0, diametros)
                self.distribucionTamanos.setColumn(1, self.corriente.solido.fracciones)
            self.diametroParticula.setValue(self.corriente.solido.diametro_medio)
        self.semaforo.release(1)

    def tipoFraccionesCambiado(self):
        if self.tipoFraccion.currentIndex()==0:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomasico[i].kgh))
        elif self.tipoFraccion.currentIndex()==1:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomolar[i]))
        elif self.tipoFraccion.currentIndex()==2:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomasico[i].lbh))
        elif self.tipoFraccion.currentIndex()==3:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.caudalunitariomolar[i]*lb))
        elif self.tipoFraccion.currentIndex()==4:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.fraccion_masica[i]))
        elif self.tipoFraccion.currentIndex()==5:
            for i in range(len(self.indices)):
                self.TablaComposicion.item(i+1, 0).setText(representacion(self.corriente.fraccion[i]))

    def composicionEntrada(self):
        fracciones=self.TablaComposicion.getColumn(0)[1:]
        if self.tipoFraccion.currentIndex()==0:
            variable="caudalUnitarioMasico"
        elif self.tipoFraccion.currentIndex()==1:
            variable="caudalUnitarioMolar"
        elif self.tipoFraccion.currentIndex()==2:
            variable="caudalUnitarioMasico"
            fracciones=[fraccion*lb for fraccion in fracciones]
        elif self.tipoFraccion.currentIndex()==3:
            variable="caudalUnitarioMolar"
            fracciones=[fraccion*lb for fraccion in fracciones]
        elif self.tipoFraccion.currentIndex()==4:
            variable="fraccionMasica"
        elif self.tipoFraccion.currentIndex()==5:
            variable="fraccionMolar"
        return variable, fracciones
        
    def valueTablaFraccionesChanged(self):
        if self.semaforo.available()>0:
            variable, fracciones=self.composicionEntrada()
            if sum(fracciones)==1. or fracciones.count(0)==0:
                self.calculo(variable, fracciones)
        
    def calculo(self, variable, valor):
        if self.semaforo.available()>0:
            if isinstance(self, QtGui.QDialog):
                self.status.setState(4)
            kwargs={variable: valor}
            if variable=="caudalMasico":
                self.caudalMolar.clear()
                self.caudalVol.clear()
            if variable=="caudalMolar":
                self.caudal.clear()
                self.caudalVol.clear()
            if variable=="caudalVolumetrico":
                self.caudalMolar.clear()
                self.caudal.clear()
            self.salida(**kwargs)


    def distribucionFinished(self):
        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
        fracciones=self.distribucionTamanos.getColumn(1, False)
        if diametros:
            kwargs={"distribucion_diametro": diametros, "distribucion_fraccion": fracciones}
            self.salida(**kwargs)
    
    def caudalesSolidoFinished(self):
        caudales=self.caudalSolido()
        kwargs={"caudalSolido": caudales}
        self.salida(**kwargs)
        
    def caudalSolido(self):
        caudales=[]
        for widget in self.CaudalSolidos:
            caudales.append(widget.value)
        return caudales

    def checkDistributionToggled(self, bool):
        self.distribucionTamanos.setEnabled(bool)
        self.botonGenerar.setEnabled(bool)
        self.botonNormalizar.setEnabled(bool)
        self.diametroParticula.setDisabled(bool)
        if bool:
            self.corriente.kwargs["diametroMedio"]=None
            self.distribucionFinished()
            
        else:
            self.corriente.kwargs["distribucion_diametro"]=[]
            self.corriente.kwargs["distribucion_fraccion"]=[]
            kwargs={"diametroMedio": self.diametroParticula.value}
            self.salida(**kwargs)


    def botonNormalizar_clicked(self, diametros=None, fracciones=None):
        if not diametros:
            diametros=self.distribucionTamanos.getColumn(0, False)
        if not fracciones:
            fracciones=self.distribucionTamanos.getColumn(1, False)
        if diametros:
            diametros.sort()
            suma=sum(fracciones)
            fracciones=[fraccion/suma for fraccion in fracciones]
            self.distribucionTamanos.setColumn(0, diametros)
            self.distribucionTamanos.setColumn(1, fracciones)


    def botonGenerar_clicked(self):
        dialog=Dialog_Distribucion(self)
        if dialog.exec_():
            self.distribucionTamanos.setMatrix(dialog.matriz)

    def diametro_medio(self):
        conversion=unidades.Length(1, "conf", "ParticleDiameter").m
        diametros=[diametro*conversion for diametro in self.distribucionTamanos.getColumn(0, False)]
        fracciones=self.distribucionTamanos.getColumn(1, False)
        if sum(fracciones)!=1.:
            suma=sum(fracciones)
            fracciones=[fraccion/suma for fraccion in fracciones]

        diametro_medio=sum([diametro*fraccion for diametro, fraccion in zip(diametros, fracciones)])
        self.diametroParticula.setValue(diametro_medio)

    def clear(self):
        pass
    
    def salida(self, **kwargs):
        """Función que crea la instancia corriente"""
        if not kwargs:
            kwargs={}
            kwargs["T"]=self.T.value
            kwargs["P"]=self.P.value
            kwargs["x"]=self.x.value
            kwargs["caudalMasico"]=self.caudal.value
            kwargs["caudalMolar"]=self.caudalMolar.value
            kwargs["caudalVolumetrico"]=self.caudalVol.value
            kwargs["notas"]=self.PageNotas.notas.toHtml()
            
            variable, fracciones=self.composicionEntrada()
            kwargs[variable]=fracciones
            
            kwargs["caudalSolido"]=self.caudalSolido()
            kwargs["diametroMedio"]=self.diametroParticula.value
            kwargs["distribucion_diametro"]=self.TablaSolidos.getColumn(0)
            kwargs["distribucion_fraccion"]=self.TablaSolidos.getColumn(1)
            
        if not self.evaluate.isRunning():
            self.evaluate.start(self.corriente, kwargs)
        
        
class Corriente_Dialog(QtGui.QDialog, Ui_corriente):
    """Dialogo de definición de formatos de líneas"""
    Changed = QtCore.pyqtSignal(Corriente)
    corriente=Corriente()
    def __init__(self, corriente=Corriente(), readOnly=False, parent=None):
        layout=QtGui.QHBoxLayout()
        self.status=Status()
        layout.addWidget(self.status)
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)
        super(Corriente_Dialog, self).__init__(corriente, readOnly)
        self.setWindowTitle(QtGui.QApplication.translate("pychemqt", "Edit stream properties"))
        self.layout().addLayout(layout)

        
class Ui_psychrometry(QtGui.QWidget):
    Changed = QtCore.pyqtSignal(PsyState)
    parameters = ["tdb", "twb", "tdp", "w", "mu", "HR", "v", "h", "Pv", "Xa", "Xw"]
    
    def __init__(self, punto=None, readOnly=False, parent=None):
        super(Ui_psychrometry, self).__init__(parent)
        self.readOnly=readOnly
        layout=QtGui.QGridLayout(self)
        
        self.inputs = PsychroInput()
        self.inputs.stateChanged.connect(self.rellenar)
        layout.addWidget(self.inputs, 1, 1, 1, 2)

        layout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed), 1, 3)
        layout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed,
                                         QtGui.QSizePolicy.Fixed), 2, 1)
        
        vlayout = QtGui.QVBoxLayout()
        layout.addLayout(vlayout,1, 4, 6, 1)
        vlayout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding))
        groupbox = QtGui.QGroupBox(QtGui.QApplication.translate(
            "pychemqt", "Calculated properties"))
        vlayout.addWidget(groupbox)
        lytGroup = QtGui.QGridLayout(groupbox)
        lytGroup.addWidget(QtGui.QLabel("Tdb"),1,1)
        self.tdb = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.tdb, 1, 2)
        lytGroup.addWidget(QtGui.QLabel("Twb"), 2, 1)
        self.twb = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.twb, 2, 2)
        lytGroup.addWidget(QtGui.QLabel("Tdp"), 3, 1)
        self.tdp = Entrada_con_unidades(unidades.Temperature, readOnly=True)
        lytGroup.addWidget(self.tdp, 3, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Absolute humidity")), 4, 1)
        massUnit = unidades.Mass(None).text()+"/"+unidades.Mass(None).text()
        self.w = Entrada_con_unidades(float, readOnly=True, textounidad=massUnit)
        lytGroup.addWidget(self.w, 4, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Degree of saturation")), 5, 1)
        self.mu=Entrada_con_unidades(float, readOnly=True, textounidad="%")
        lytGroup.addWidget(self.mu, 5, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Relative humidity")), 6, 1)
        self.HR=Entrada_con_unidades(float, readOnly=True, textounidad="%")
        lytGroup.addWidget(self.HR, 6, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Volume")), 7, 1)
        self.v=Entrada_con_unidades(unidades.SpecificVolume, readOnly=True)
        lytGroup.addWidget(self.v, 7, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Enthalpy")), 8, 1)
        self.h=Entrada_con_unidades(unidades.Enthalpy, readOnly=True)
        lytGroup.addWidget(self.h, 8, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Vapour Pressure")), 9, 1)
        self.Pv=Entrada_con_unidades(unidades.Pressure, readOnly=True)
        lytGroup.addWidget(self.Pv, 9, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Air fraction")), 10, 1)
        self.Xa=Entrada_con_unidades(float, readOnly=True)
        lytGroup.addWidget(self.Xa, 10, 2)
        lytGroup.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Water fraction")), 11, 1)
        self.Xw=Entrada_con_unidades(float, readOnly=True)
        lytGroup.addWidget(self.Xw, 11, 2)
        vlayout.addItem(QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding,
                                          QtGui.QSizePolicy.Expanding))

        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Mass Flow")), 3, 1)
        self.caudal=Entrada_con_unidades(unidades.MassFlow, readOnly=readOnly)
#        self.caudal.valueChanged.connect(self.NuevoPunto)
        layout.addWidget(self.caudal, 3, 2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Molar Flow")), 4, 1)
        self.caudalMolar=Entrada_con_unidades(unidades.MolarFlow, readOnly=readOnly)
#        self.caudalMolar.valueChanged.connect(self.NuevoPunto)
        layout.addWidget(self.caudalMolar, 4, 2)
        layout.addWidget(QtGui.QLabel(QtGui.QApplication.translate(
            "pychemqt", "Volumetric Flow")), 5, 1)
        self.caudalVolumetrico=Entrada_con_unidades(unidades.VolFlow, readOnly=readOnly)
#        self.caudalVolumetrico.valueChanged.connect(self.NuevoPunto)
        layout.addWidget(self.caudalVolumetrico, 5, 2)
        layout.addItem(QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Expanding,
                                         QtGui.QSizePolicy.Expanding),9,2)

        self.setReadOnly(readOnly)
        self.inputs.updateInputs(0)
#        if punto:
#            self.setCorriente(punto)
#        else:
#            self.AireHumedo=Psychrometry(1)

    def setCorriente(self, state):
            self.punto=state
#            self.AireHumedo=Psychrometry(punto.P.atm)
            self.rellenar(state)
            self.rellenarInput(state)
        
    def setReadOnly(self, readOnly):
        self.inputs.setReadOnly(readOnly)
        self.caudal.setReadOnly(readOnly)
        self.caudalMolar.setReadOnly(readOnly)
        self.caudalVolumetrico.setReadOnly(readOnly)
            
    def rellenar(self, state):
        for par in self.parameters:
            self.__getattribute__(par).setValue(state.__getattribute__(par))

    def rellenarInput(self, state):
        self.blockSignals(True)
        self.variables.setCurrentIndex(state.mode)
        self.P.setValue(punto.P)
#        if punto.caudal:
#            self.caudal.setValue(punto.caudal)
#        if punto.modo==0:
#            self.EntradaTdb.setValue(punto.Tdb)
#            self.EntradaH.setValue(punto.w)
#        elif punto.modo==1:
#            self.EntradaTdb.setValue(punto.Tdb)
#            self.EntradaHR.setValue(punto.HR)
#        elif punto.modo==2:
#            self.EntradaTdb.setValue(punto.Tdb)
#            self.EntradaTdp.setValue(punto.Tdp)
#        elif punto.modo==3:
#            self.EntradaTdb.setValue(punto.Tdb)
#            self.EntradaTwb.setValue(punto.Twb)
#        elif punto.modo==4:
#            self.EntradaHR.setValue(punto.HR)
#            self.EntradaTdp.setValue(punto.Tdp)
        self.blockSignals(False)

    def todos_datos(self):
        return self.punto and self.P.value and self.caudal.value
            
            
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    
#    distribucion=[[17.5, 0.02],
#                                [22.4, 0.03], 
#                                [26.2,  0.05], 
#                                [31.8,  0.1],  
#                                [37, 0.1],
#                                [42.4, 0.1], 
#                                [48, 0.1], 
#                                [54, 0.1], 
#                                [60, 0.1], 
#                                [69, 0.1], 
#                                [81.3, 0.1], 
#                                [96.5, 0.05], 
#                                [109, 0.03], 
#                                [127, 0.02]]
#    solido=Solid([638], [100], distribucion)
#
##    mezcla=Corriente(340, 1, 1000, Mezcla([10, 38, 22, 61], [.3, 0.5, 0.05, 0.15]), notas="Corriente de ejemplo")
#    mezcla=Corriente(340, 1, 1000, Mezcla([475, 7, 62], [.3, 0.5, 0.2, ]), solido, notas="Corriente de ejemplo")
#    agua=Corriente(T=300, P=1e5, caudalMasico=1, fraccionMolar=[1.])
#    agua(caudalSolido=[35], diametroMedio=0.0002, notas="Corriente de agua de ejemplo")
#    print agua.solido
#    diametros=[17.5e-5, 22.4e-5, 26.2e-5, 31.8e-5, 37e-5, 42.4e-5, 48e-5, 54e-5, 60e-5, 69e-5, 81.3e-5, 96.5e-5, 109e-5, 127e-5]
#    fracciones=[0.02, 0.03, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.03, 0.02]
#    solido=Solid(caudalSolido=[0.01], distribucion_diametro=diametros, distribucion_fraccion=fracciones)
#    corriente=Corriente(T=300, P=101325, caudalMasico=1.,  fraccionMolar=[1.], solido=solido)
#    corriente = Ui_corriente()
#    corriente=Corriente_Dialog()
#    corriente.show()
    aire=PsychroState(caudal=5, tdb=300, HR=50)
    corriente=Ui_psychrometry(aire)
#    corriente.show()
#    corriente = Dialog_Distribucion()
    corriente.show()
    sys.exit(app.exec_())



