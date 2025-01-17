#!/usr/bin/env python
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import *
import numpy as np
#import pdb
from rooFitBuilder import *
import os
import configLimits as cfl
from configLimits import AutoVivification
import argparse

gROOT.SetBatch()
gSystem.SetIncludePath( "-I$ROOFITSYS/include/" );
gROOT.ProcessLine('.L ./CMSStyle.C')
CMSStyle()
gStyle.SetOptStat(0)

YR = cfl.YR
sigFit = cfl.sigFit
testPoints = cfl.testPoints
highMass = cfl.highMass

# rounding function for interpolation
def roundToN(x, N=5):
  return int(N* round(float(x)/N))

def set_palette(name='palette', ncontours=999):
  """Set a color palette from a given RGB list
  stops, red, green and blue should all be lists of the same length
  see set_decent_colors for an example"""

  if name == "gray" or name == "grayscale":
      stops = [0.00, 0.34, 0.61, 0.84, 1.00]
      red   = [1.00, 0.84, 0.61, 0.34, 0.00]
      green = [1.00, 0.84, 0.61, 0.34, 0.00]
      blue  = [1.00, 0.84, 0.61, 0.34, 0.00]
  # elif name == "whatever":
      # (define more palettes)
  else:
      # default palette, looks cool
      stops = [0.00, 0.34, 0.61, 0.84, 1.00]
      red   = [0.00, 0.00, 0.87, 1.00, 0.51]
      green = [0.00, 0.81, 1.00, 0.20, 0.00]
      blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

  s = np.array(stops, 'd')
  r = np.array(red, 'd')
  g = np.array(green, 'd')
  b = np.array(blue, 'd')

  npoints = len(s)
  TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
  gStyle.SetNumberContours(ncontours)

def getArgs():
  parser = argparse.ArgumentParser()
  group = parser.add_mutually_exclusive_group()
  group.add_argument("-v","--verbose",action = "store_true")
  group.add_argument("-q","--quiet",action = "store_true")
  parser.add_argument("--tev", help="CoM Energy", default = cfl.tevList[0], choices = ['7TeV','8TeV'] )
  parser.add_argument("--lepton", help="Lepton Flavor", default = cfl.leptonList[0], choices = ['mu','el'])
  parser.add_argument("--cat", help="Cat Number", default = cfl.catListSmall[0], type = int)
  parser.add_argument("--suffix", help="Specify suffix", default = cfl.suffixPostFix, type = str)
  parser.add_argument("--cores", help="Number of CPU cores for use (must be 1 for batch mode)", default = 12, type = int)
  args = parser.parse_args()
  return args

def SignalFitMaker(lep, tev, cat, suffix, cores):
  cpuNum = cores

  set_palette()

  massList = cfl.massListBig
  sigNameList = cfl.sigNameList

  rooWsFile = TFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/initRooFitOut_'+suffix+'.root')
  myWs = rooWsFile.Get('ws')
  #myWs.Print()
  narrow = ''
  if 'Narrow' in suffix: narrow = 'Narrow'

  RooRandom.randomGenerator().SetSeed(8675309)

  mzg = myWs.var('CMS_hzg_mass')
  cardDict = AutoVivification()
  for mass in massList:
    cardDict[lep][tev][cat][mass] = RooWorkspace('ws_card')


# we need crystal ball + gaussian fits for all mass points, and for all production methods.
# we also need to interpolate the distributions for 0.5 mass bins, so we use some tricks
# in order to create new fits out of the existing 5GeV steps

###################
# Start the Loop! #
###################

  for prod in sigNameList:
    dsList = []
    fitList = []
    normList = []
    startingValsLow = []
    startingValsHi = []
    oldMassHi = oldMassLow = 0
    if sigFit == 'DCB':
      paramHists = [
          TH1F('meanDCB', 'meanDCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('sigmaDCB', 'sigmaDCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('alpha1DCB', 'alpha1DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('alpha2DCB', 'alpha2DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('n1DCB', 'n1DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('n2DCB', 'n2DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('fracDCB', 'fracDCB', len(massList), float(massList[0]), float(massList[-1])),
        ]
    elif sigFit == 'DCB2':
      paramHists = [
          TH1F('meanDCB', 'meanDCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('sigma1DCB', 'sigma1DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('sigma2DCB', 'sigma2DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('alpha1DCB', 'alpha1DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('alpha2DCB', 'alpha2DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('n1DCB', 'n1DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('n2DCB', 'n2DCB', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('fracDCB', 'fracDCB', len(massList), float(massList[0]), float(massList[-1])),
        ]
    else:
      paramHists = [
          TH1F('meanGCBG', 'meanGCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('meanCBCBG', 'meanCBCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('sigmaGCBG', 'sigmaGCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('sigmaCBCBG', 'sigmaCBCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('alphaCBG', 'alphaCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('nCBG', 'nCBG', len(massList), float(massList[0]), float(massList[-1])),
          TH1F('fracCBG', 'fracCBG', len(massList), float(massList[0]), float(massList[-1])),
        ]
    for massString in massList:

      #############################################
      # Get the high and low mass references      #
      # If the point does not need interpolation, #
      # we just use it for high and low           #
      #############################################

      fitBuilder = FitBuilder(mzg,tev,lep,cat,sig=prod,mass=massString)

      mass = float(massString)
      if highMass:
        if mass <= 500:
          if mass%50.0 == 0.0:
            massHi = int(mass)
            massLow = int(mass)
          else:
            massRound = roundToN(massString,50)
            if mass<massRound:
              massHi = massRound
              massLow = massRound-50
            else:
              massHi = massRound+50
              massLow = massRound
        else:
          if mass in [800,1200,1600]:
            massHi = int(mass)
            massLow = int(mass)
          else:
            tmpHighList = [500,800,1200,1600]
            massRound = min(tmpHighList, key=lambda x:abs(x-mass))
            if mass<massRound:
              massHi = massRound
              massLow = tmpHighList[tmpHighList.index(massRound)-1]
            else:
              massHi = tmpHighList[tmpHighList.index(massRound)+1]
              massLow = massRound

      else:
        if mass%5.0 == 0.0:
          massHi = int(mass)
          massLow = int(mass)
        else:
          massRound = roundToN(massString)
          if mass<massRound:
            massHi = massRound
            massLow = massRound-5
          else:
            massHi = massRound+5
            massLow = massRound
      ###### only calc the low and high points if they change

      if oldMassLow != massLow:

        ###### fit the low mass point
        if massLow<=100:
          mzg.setRange('fitRegion1',115,int(massLow)+15)
        elif massLow > 160 and narrow == '' and int(massLow) <=500:
          mzg.setRange('fitRegion1',int(massLow)*0.61,int(massLow)*1.39)
        elif massLow > 160 and narrow == '':
          mzg.setRange('fitRegion1',int(massLow)*0.61,int(massLow)*1.39)
          #mzg.setRange('fitRegion1',int(massLow)*0.50,int(massLow)*1.5)
        else:
          #mzg.setRange('fitRegion1',int(massLow)*0.92,int(massLow)*1.08)
          mzg.setRange('fitRegion1',int(massLow)*0.80,int(massLow)*1.2)
        sigNameLow = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massLow)+narrow])
        sig_ds_Low = myWs.data(sigNameLow)
        if massLow == massHi:
          dsList.append(sig_ds_Low)


        fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(massLow))

        if sigFit == 'DCB':
          if massLow>500:
            SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low',mean=massLow, sigma = massLow*0.03)
                #nCB1High = 70, nCB1 = 20, nCB2High = 70, nCB2 = 20,
                #alphaCB1 = 5, alphaCB1Low = 0.001, alphaCB1High = 10,
                #alphaCB2 = -5, alphaCB2Low = -10, alphaCB2High = -0.001)
         # elif massLow>500 and lep == 'mu':
         #   SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low',mean=massLow, sigma = massLow*0.18,
         #       nCB1High = 70, nCB1 = 20, nCB2High = 70, nCB2 = 20,
         #       alphaCB1 = 5, alphaCB1Low = 0.001, alphaCB1High = 10,
         #       alphaCB2 = -5, alphaCB2Low = -10, alphaCB2High = -0.001)
          elif lep == 'el':
            SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low',mean=massLow, sigma = massLow*0.03)
          elif lep == 'mu':
            SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low',mean=massLow, sigma = massLow*0.03,)
                #nCB1High = 50, nCB1 = 10, nCB2High = 20, nCB2 = 10)
        elif sigFit == 'DCB2':
          SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low',mean=massLow, sigmaCB1 = massLow*0.03, sigmaCB2 = massLow*0.03)
        elif highMass and narrow=='':
          SigFit_Low,tempParamsLow= fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, sigmaG = massLow*0.08, sigmaCB = massLow*0.03)
        elif suffix == '09-3-14_Proper' and cat == '5' and lep == 'el':
          SigFit_Low,tempParamsLow = fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, meanGLow = massLow*0.95, meanGHigh = massLow*1.05, meanCBLow = massLow*0.95, meanCBHigh = massLow*1.05)
        elif highMass and '2000' in suffix:
          SigFit_Low,tempParamsLow = fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, sigmaCB = massLow*0.02, sigmaG = massLow*0.02, frac = 0.011)
          print 'lol'
        else:
          SigFit_Low,tempParamsLow = fitBuilder.Build(sigFit, piece = 'Low', mean = massLow, sigmaCB = massLow*0.02, sigmaG = massLow*0.02)

        sig_ds_Low.Print()
        #SigFit_Low.fitTo(sig_ds_Low, RooFit.Minos(True), RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(2), RooFit.NumCPU(cpuNum))
        SigFit_Low.fitTo(sig_ds_Low, RooFit.Range('fitRegion1'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(2), RooFit.NumCPU(cpuNum))

        startingValsLow = [x.getVal() for x in tempParamsLow]
        oldMassLow = massLow

      if oldMassHi != massHi:
        ###### fit the hi mass point
        if massHi<=100:
          mzg.setRange('fitRegion2',115,int(massHi)+15)
        elif massHi > 160 and narrow == '' and int(massHi) <=500:
          mzg.setRange('fitRegion2',int(massHi)*0.61,int(massHi)*1.39)
        elif massHi > 160 and narrow == '':
          mzg.setRange('fitRegion2',int(massHi)*0.61,int(massHi)*1.39)
        else:
          #mzg.setRange('fitRegion2',int(massHi)*0.92,int(massHi)*1.08)
          mzg.setRange('fitRegion2',int(massHi)*0.80,int(massHi)*1.2)
        sigNameHi = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(massHi)+narrow])
        sig_ds_Hi = myWs.data(sigNameHi)

        fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(massHi))
        if sigFit == 'DCB':
          if massHi>500:
            SigFit_Hi,tempParamsHi= fitBuilder.Build(sigFit, piece = 'Hi',mean=massHi, sigma = massHi*0.03)
                #nCB1High = 70, nCB1 = 20, nCB2High = 70, nCB2 = 20,
                #alphaCB1 = 5, alphaCB1Low = 0.001, alphaCB1High = 10,
                #alphaCB2 = -5, alphaCB2Low = -10, alphaCB2High = -0.001)
         # elif massHi>500 and lep == 'mu':
         #   SigFit_Hi,tempParamsHi= fitBuilder.Build(sigFit, piece = 'Hi',mean=massHi, sigma = massHi*0.18,
         #       nCB1High = 70, nCB1 = 20, nCB2High = 70, nCB2 = 20,
         #       alphaCB1 = 5, alphaCB1Low = 0.001, alphaCB1High = 10,
         #       alphaCB2 = -5, alphaCB2Low = -10, alphaCB2High = -0.001)
          elif lep == 'el':
            SigFit_Hi,tempParamsHi= fitBuilder.Build(sigFit, piece = 'Hi',mean=massHi, sigma = massHi*0.03)
          elif lep == 'mu':
            SigFit_Hi,tempParamsHi= fitBuilder.Build(sigFit, piece = 'Hi',mean=massHi, sigma = massHi*0.03,)
                #nCB1High = 50, nCB1 = 10, nCB2High = 20, nCB2 = 10)
        elif sigFit == 'DCB2':
          SigFit_Hi,tempParamsHi= fitBuilder.Build(sigFit, piece = 'Hi',mean=massHi, sigmaCB1 = massHi*0.03, sigmaCB2 = massHi*0.03)
        elif highMass and narrow == '':
          SigFit_Hi,tempParamsHi = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, sigmaG = massHi*0.08, sigmaCB = massHi*0.03)
        elif suffix == '09-3-14_Proper' and cat == '5' and lep == 'el':
          SigFit_Hi,tempParamsHi = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, meanGLow = massHi*0.95, meanGHigh = massHi*1.05, meanCBLow = massHi*0.95, meanCBHigh = massHi*1.05)
        elif highMass and '2000' in suffix:
          SigFit_Hi,tempParamsHi = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, sigmaCB = massHi*0.02, sigmaG = massHi*0.02, frac = 0.011)
        else:
          SigFit_Hi,tempParamsHi = fitBuilder.Build(sigFit, piece = 'Hi', mean = massHi, sigmaCB = massHi*0.02, sigmaG = massHi*0.02)

        #SigFit_Hi.fitTo(sig_ds_Hi, RooFit.Minos(True), RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(2), RooFit.NumCPU(cpuNum))
        SigFit_Hi.fitTo(sig_ds_Hi, RooFit.Range('fitRegion2'), RooFit.SumW2Error(kTRUE), RooFit.Strategy(2), RooFit.NumCPU(cpuNum))
        startingValsHi = [x.getVal() for x in tempParamsHi]
        oldMassHi = massHi

      ###### interpolate the two mass points
      if highMass:
        if massHi <= 500:
          massDiff = (massHi - mass)/50.
        elif massHi <=800:
          massDiff = (massHi - mass)/300.
        else:
          massDiff = (massHi - mass)/400.

      else:
        massDiff = (massHi - mass)/5.
      if mass<=100:
        mzg.setRange('fitRegion_'+massString,115,mass+15)
      elif mass > 160:
        mzg.setRange('fitRegion_'+massString,mass*0.61,mass*1.39)
      else:
        mzg.setRange('fitRegion_'+massString,mass*0.92,mass*1.08)
      beta = RooRealVar('beta','beta', 0.5, 0., 1.)
      if massHi == massLow:
        beta.setVal(1);
      else:
        beta.setVal(massDiff)

      if massDiff != 0.:
        interpVals = [pL+(pH-pL)*((mass-massLow)/(massHi-massLow)) for pL,pH in zip(startingValsLow, startingValsHi)]
        yieldNum = (sig_ds_Low.sumEntries()*massDiff+sig_ds_Hi.sumEntries()*(1-massDiff))
      else:
        interpVals = startingValsHi
        yieldNum = sig_ds_Hi.sumEntries()

      normList.append(yieldNum)
      yieldName = '_'.join([prod,'hzg','yield',lep,tev,'cat'+cat])
      yieldVar = RooRealVar(yieldName,yieldName,yieldNum)

      sigNameInterp = '_'.join(['ds',prod,'hzg',lep,tev,'cat'+cat,'M'+str(mass)+narrow])

      fitBuilder.__init__(mzg,tev,lep,cat,sig=prod,mass=str(mass))
      if sigFit == 'DCB':
        SigFit_Interp,paramList = fitBuilder.Build(sigFit,piece = 'Interp', mean = interpVals[0], sigma = interpVals[1], alphaCB1 = interpVals[2],alphaCB2 = interpVals[3], nCB1 = interpVals[4], nCB2 = interpVals[5], frac = interpVals[6])
      elif sigFit == 'DCB2':
        SigFit_Interp,paramList = fitBuilder.Build(sigFit,piece = 'Interp', mean = interpVals[0], sigmaCB1 = interpVals[1], sigmaCB2 = interpVals[2], alphaCB1 = interpVals[3],alphaCB2 = interpVals[4], nCB1 = interpVals[5], nCB2 = interpVals[6], frac = interpVals[7])
      else:
        SigFit_Interp,paramList = fitBuilder.Build(sigFit,piece = 'Interp', mean = mass, meanG = interpVals[0], meanCB = interpVals[1], sigmaG = interpVals[2], sigmaCB = interpVals[3], alpha = interpVals[4], n = interpVals[5], frac = interpVals[6])

      for i in paramList:
        print i.getVal()

      for i,param in enumerate(paramList):
        paramHists[i].SetBinContent(paramHists[i].FindBin(mass),param.getVal())
        paramHists[i].SetBinError(paramHists[i].FindBin(mass),param.getError())
        param.setConstant(True)

      if((highMass and ((mass<=500 and  mass%50==0) or (mass in [800,1200,1600]))) or (not highMass and mass%5==0)):
        fitList.append(SigFit_Low)
      else:
        fitList.append(SigFit_Interp)


      getattr(cardDict[lep][tev][cat][str(mass)],'import')(SigFit_Interp)
      getattr(cardDict[lep][tev][cat][str(mass)],'import')(yieldVar)
      cardDict[lep][tev][cat][str(mass)].commitTransaction()

    c = TCanvas("c","c",0,0,500,400)
    c.cd()

    if highMass:
      testFrame = mzg.frame(float(massList[0])*0.8,float(massList[-1])*1.2)
      if narrow == '':
        c.SetLogy()
    else:
      testFrame = mzg.frame(float(massList[0])-15,float(massList[-1])+15)
    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-1]
      if '800' in fit.GetName() or '1200' in fit.GetName(): continue
      fit.plotOn(testFrame, RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*15)))
      #fit.plotOn(testFrame, RooFit.LineColor(TColor.GetColorPalette(i*15)))
    #for i,signal in enumerate(dsList):
    #  signal.plotOn(testFrame, RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(80))
    if highMass: testFrame.SetMinimum(0.00005)
    testFrame.GetXaxis().SetTitle('m_{H} (GeV)')
    testFrame.GetYaxis().SetTitle('Normalized Yield')
    testFrame.GetYaxis().CenterTitle()
    testFrame.SetTitle('Interpolation Fits')
    testFrame.Draw()
    c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalFits/'+'_'.join(['test','sig','fit',sigFit,suffix,prod,lep,tev,'cat'+cat])+'.pdf')

    c.SetLogy(False)

    for hist in paramHists:
      hist.SetTitle(hist.GetName())
      hist.Draw('EP')
      c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalParams/'+'_'.join(['test',hist.GetName(),sigFit,suffix,prod,lep,tev,'cat'+cat])+'.pdf')


    for i,fit in enumerate(fitList):
      regionName = fit.GetName().split('_')[-2]
      if (float(regionName) in map(lambda x: float(x), testPoints)):
        if highMass:
          testFrame = mzg.frame(float(regionName)*0.61, float(regionName)*1.39)
        else:
          testFrame = mzg.frame(float(regionName)-15, float(regionName)+15)
        fit.plotOn(testFrame, RooFit.Name('model'),RooFit.Normalization(normList[i],RooAbsReal.NumEvent),RooFit.LineColor(TColor.GetColorPalette(i*10)))
        fit.paramOn(testFrame,RooFit.ShowConstants(True), RooFit.Layout(0.6, 1.0, 0.98))
        testFrame.getAttText().SetTextSize(0.021)

        if float(regionName)%5==0:
          signal = filter(lambda x: float(x.GetName().split('_')[-1].rstrip('Narrow').lstrip('M')) == float(regionName), dsList)[0]
          signal.plotOn(testFrame, RooFit.Name('data'),RooFit.MarkerStyle(20+i), RooFit.MarkerSize(1),RooFit.Binning(600))
          testFrame.Draw()
          ndof = 0
          if sigFit == 'TripG': ndof = 8
          else: ndof = 7
          chi2 = testFrame.chiSquare('model','data',ndof)
          txt = TText(0,0,'chi2/ndof: '+'{0:.3f}'.format(chi2))
          txt.SetNDC()
          if highMass and  narrow=='':
            txt.SetX(0.2)
            txt.SetY(0.7)
          else:
            txt.SetX(0.2)
            txt.SetY(0.3)
          txt.SetTextSize(0.04)
          testFrame.addObject(txt)
        testFrame.GetXaxis().SetTitle('m_{H} (GeV)')
        testFrame.GetYaxis().SetTitle('Normalized Yield')
        testFrame.GetYaxis().CenterTitle()
        testFrame.SetTitle('Fit for M'+regionName)
        testFrame.Draw()
        c.Print('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/debugPlots/signalFits/'+'_'.join(['test','sig','fit',sigFit,'M'+regionName,suffix,prod,lep,tev,'cat'+cat])+'.pdf')

  for prod in sigNameList:
    for mass in massList:
      fitBuilder = FitBuilder(mzg,tev,lep,cat,sig=prod,mass=mass)
      fitBuilder.SignalNameParamFixer(cardDict[lep][tev][cat][mass],sigFit)

  for mass in massList:
    fileName = '_'.join(['SignalOutput',lep,tev,'cat'+cat,mass])
    if not os.path.isdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass): os.mkdir('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass)
    cardDict[lep][tev][cat][mass].writeToFile('/tthome/bpollack/CMSSW_6_1_1/src/BiasAndLimits/outputDir/'+suffix+'_'+YR+'_'+sigFit+'/'+mass+'/'+fileName+'.root')


if __name__=="__main__":
  args = getArgs()
  SignalFitMaker(args.lepton, args.tev, str(args.cat), args.suffix, args.cores)

