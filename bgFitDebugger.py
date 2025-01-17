#!/usr/bin/env python
import sys
sys.argv.append('-b')
import numpy as np
#import pdb
from signalCBFits import AutoVivification
from rooFitBuilder import *
from xsWeighterNew import *
from ROOT import *
import os
import configLimits as cfl

gSystem.SetIncludePath( "-I$ROOFITSYS/include/" )
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()

debugPlots = cfl.debugPlots

verbose = cfl.verbose

doMVA = cfl.doMVA

suffix = cfl.suffix

dataDict = {'mu2012_4cat':TFile('inputFiles/m_llgFile_MuMu2012ABCD_'+suffix+'.root','r'),'el2012_4cat':TFile('inputFiles/m_llgFile_EE2012ABCD_'+suffix+'.root','r'),'mu2011_4cat':TFile('inputFiles/m_llgFile_MuMu2011ABCD_Proper.root','r'),'el2011_4cat':TFile('inputFiles/m_llgFile_EE2011ABCD_Proper.root','r'),'all2011_4cat':TFile('inputFiles/m_llgFile_All2011ABCD_Proper.root','r')}

lepton = cfl.leptonList[0]
year = cfl.yearList[0]
cat= cfl.catListSmall[0]
mass = cfl.massList[0]

bgFitList = ['Pow','PowDecay','PowLog','Exp2','Laurent','ExpSum']

yearToTeV = {'2011':'7TeV','2012':'8TeV'}

xmin = 150
xmax = 500
binning = (xmax-xmin)/2

weight  = RooRealVar('Weight','Weight',0,100)
mzg  = RooRealVar('CMS_hzg_mass','CMS_hzg_mass',xmin,xmax)
#mzg.setRange('full',100,190)
#mzg.setBins(50000,'cache')
mzg.setBins((xmax-xmin)*4)

c = TCanvas("c","c",0,0,500,400)
c.cd()


################
# get the data #
################


dataName = '_'.join(['data',lepton,yearToTeV[year],'cat'+cat])
dataTree = dataDict[lepton+year+'_4cat'].Get('m_llg_DATA')
#tmpMassEventOld = np.zeros(1,dtype = 'f')
tmpMassEventOld = np.zeros(1,dtype = 'd')
if cat is '0':
  dataTree.SetBranchAddress('m_llg_DATA',tmpMassEventOld)
else:
  dataTree.SetBranchAddress('m_llgCAT'+cat+'_DATA',tmpMassEventOld)
data_argS = RooArgSet(mzg)
if cat == '5':
  data_ds = RooDataSet(dataName,dataName,data_argS)
else:
  data_ds = RooDataHist(dataName,dataName,data_argS)
for i in range(0,dataTree.GetEntries()):
  dataTree.GetEntry(i)
  if tmpMassEventOld[0]> xmin and tmpMassEventOld[0]<xmax:
    mzg.setVal(tmpMassEventOld[0])
    data_ds.add(data_argS)
dataTree.ResetBranchAddresses()

#############
# make fits #
#############

fitBuilder = FitBuilder(mzg, yearToTeV[year], lepton, cat)

leg  = TLegend(0.7,0.7,1.0,1.0)
leg.SetFillColor(0)
leg.SetShadowColor(0)
leg.SetBorderSize(1)
leg.SetHeader(', '.join([year,lepton,'cat'+cat]))

testFrame = mzg.frame()
data_ds.plotOn(testFrame,RooFit.Binning(binning),RooFit.Name('data'))

for fitName in bgFitList:

  color = fitBuilder.FitColorDict[fitName]
  ndof = fitBuilder.FitNdofDict[fitName]
  fit = fitBuilder.Build(fitName)
  fit.Print()
  fit.fitTo(data_ds, RooFit.Strategy(1))
  fit.plotOn(testFrame, RooFit.LineColor(color), RooFit.Name(fitName))
  testFrame.Draw()
  chi2 = testFrame.chiSquare(fitName,'data',ndof)
  leg.AddEntry(testFrame.findObject(fitName),fitName+' #chi2 = {0:.3f}'.format(chi2),'l')
  #leg.AddEntry(testFrame.findObject(fitName),fitName,'l')


#txt = TText(0,0,'chi2/ndof: '+'{0:.3f}'.format(chi2))
#leg.AddEntry(testFrame.findObject('PowDecay'),'PowDecay','l')
leg.Draw()
c.Print('debugPlots/'+'_'.join(['DEBUG','fits',suffix,year,lepton,'cat'+cat])+'.pdf')


