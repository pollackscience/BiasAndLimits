#!/usr/bin/env python

# class for multi-layered nested dictionaries, pretty cool
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

##########
# common #
##########

doMVA = False
#suffix = 'Proper'
#suffix = '08-21-14_PhoMVA'
#suffix = '09-3-14_Proper'
#suffix = '09-5-14_HighMass'
#suffix = '09-26-14_HighMass'
#suffix = '10-30-14_HighMass'
#suffix = '09-26-14_HighMassNarrow'
#suffix = '09-7-14_PhoMVAKinMVA'
#suffix = '11-28-14_HighMass'
#suffix = '11-28-14_HighMassNarrow'
#suffix = '11-28-14_HighMass_noEngCor'
#suffix = '11-28-14_HighMassNarrow_noEngCor'
#suffix = '12-04-14_HighMass'
#suffix = '12-04-14_HighMassNarrow'
#suffix = '01-23-14_HighMassATLAS'
#suffix = '01-29-15_HighMass'
#suffix = '01-29-15_HighMassNarrow'
#suffix = '01-29-15_HighMassDown'
#suffix = '01-29-15_HighMassDownNarrow'
#suffix = '01-29-15_HighMassUp'
#suffix = '01-29-15_HighMassUpNarrow'
#suffix = '02-03-15_HighMassPUWeightUp'
#suffix = '02-04-15_HighMassZ75'
suffix = '02-11-15_HighMass'
#suffix = '02-11-15_HighMassNarrow'
#suffix = '02-11-15_HighMassElePt15'
#suffix = '02-11-15_HighMassNarrowElePt15'
suffixPostFix = suffix+'800'
#suffixPostFix = suffix


leptonList = ['mu','el']
#leptonList = ['el']
yearList = ['2011','2012']
#yearList = ['2012']
tevList = ['7TeV','8TeV']
#tevList = ['8TeV']
catListBig = ['0','1','2','3','4','5','6','7','8','9']
catListSmall = ['0','1','2','3','4','5']
#catListSmall = ['5']
massList = ['120','125','130','135','140','145','150','155','160']
#massList = ['125']
sigNameList = ['ggH','qqH','ttH','WH','ZH']
#sigNameList = ['ggH']
YR = 'YR3'
highMass = True

modelIndependent = True

if highMass:
  massList = ['200','250','300','350','400','450','500']
  #massList = ['200','250','300','350','400','450']
  #massList = ['500']
  sigNameList = ['ggH']
  yearList = ['2012']
  tevList = ['8TeV']
  if '5' in catListSmall: catListSmall.remove('5')
  if '5' in catListBig: catListBig.remove('5')
  catListSmall = catListBig = ['0']




######################
# initialFitProducer #
######################

debugPlots = False
verbose = False
rootrace = False
allBiasFits= True# Turn on extra fits used in bias studies
blind = False
sigNameListInput = ['gg','vbf','tth','wh','zh']

bgFitListTurnOn = ['GaussPow','GaussExp','GaussBern3','GaussBern4','GaussBern5']
bgFitListVBF = ['Exp','Pow','Bern2','Bern3','Bern4']
#bgFitListHighMass = ['Exp2','Pow','PowDecay','PowLog','Laurent','ExpSum']
bgFitListHighMass = ['Gamma','Weibull','Hill','Pow','PowDecay','PowLog','Laurent','Exp2','ExpSum','TripExpSum','PowExpSum','TripPowSum']
#bgFitListHighMass = ['Gamma','Weibull','Hill','Pow','Laurent','Exp2']
#bgFitListHighMass = ['TripExpSum']
#bgFitListHighMass = ['Gamma']

bgRange = [100,190]
if highMass:
  #bgRange = [150,600]
  #bgRange = [150,700]
  bgRange = [150,800]
blindRange = [180,550]

if highMass:
  sigNameListInput = ['gg']


##############
# bgCardPrep #
##############

doExt = False
doFancy = True
if 'Narrow' in suffix:
  doFancy = False

################
# signalCBFits #
################

if 'Narrow' in suffix:
  sigFit = 'CBG'
else:
  sigFit = 'DCB'
#sigFit = 'TripG'
#sigFit = 'DCB2'

testPoints = ['125.0']

massListBig = ['120.0','120.5','121.0','121.5','122.0','122.5','123.0','123.5','124.0','124.5',
'124.6','124.7','124.8','124.9','125.0','125.1','125.2','125.3','125.4','125.5',
'125.6','125.7','125.8','125.9','126.0','126.1','126.2','126.3','126.4','126.5',
'127.0','127.5','128.0','128.5','129.0','129.5','130.0',
'130.5','131.0','131.5','132.0','132.5','133.0','133.5','134.0','134.5','135.0',
'135.5','136.0','136.5','137.0','137.5','138.0','138.5','139.0','139.5','140.0',
'141.0','142.0','143.0','144.0','145.0','146.0','147.0','148.0','149.0','150.0',
'151.0','152.0','153.0','154.0','155.0','156.0','157.0','158.0','159.0','160.0']

#massListBig = ['120.0','125.0','130.0','135.0','140.0','145.0','150.0','155.0','160.0']
#massListBig = ['125.0']
if highMass:
  #massListBig = ['200.0', '210.0', '220.0', '230.0', '240.0', '250.0', '260.0', '270.0', '280.0', '290.0',
  #    '300.0', '310.0', '320.0', '330.0', '340.0', '350.0', '360.0', '370.0', '380.0', '390.0',
  #    '400.0', '410.0', '420.0', '430.0', '440.0', '450.0', '460.0', '470.0', '480.0', '490.0', '500.0']

  massListBig = ['200.0', '205.0', '210.0', '215.0', '220.0', '225.0', '230.0', '235.0', '240.0', '245.0',
      '250.0', '255.0', '260.0', '265.0', '270.0', '275.0', '280.0', '285.0', '290.0', '295.0', '300.0',
      '305.0', '310.0', '315.0', '320.0', '325.0', '330.0', '335.0', '340.0', '345.0', '350.0', '355.0',
      '360.0', '365.0', '370.0', '375.0', '380.0', '385.0', '390.0', '395.0', '400.0', '405.0', '410.0',
      '415.0', '420.0', '425.0', '430.0', '435.0', '440.0', '445.0', '450.0', '455.0', '460.0',
      '465.0', '470.0', '475.0', '480.0', '485.0', '490.0', '495.0', '500.0']
  #massListBig= ['200.0']
  testPoints = ['200.0','250.0','300.0','350.0','400.0','450.0','500.0']

###############
# batchSignal #
###############

#no special switches

#############
# cardMaker #
#############

#no special switches

#################
# limitProducer #
#################

fullCombo = True
byParts = False
noCats = False
if highMass:
  noCats = True

###############
# batchLimits #
###############

mode = 'Combo'
#mode = 'noCombo'

syst = True

################
# limitPlotter #
################

obs = True

########################
########################
# Define limit bgFits: #
########################
########################

bgLimitDict = AutoVivification()
#bgLimitDict[highMass][tev][lepton][cat]
bgLimitDict[True]['8TeV']['mu']['0'] = 'TripExpSum'
bgLimitDict[True]['8TeV']['mu']['1'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['2'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['3'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['4'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['5'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['6'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['7'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['8'] = 'PowDecay'
bgLimitDict[True]['8TeV']['mu']['9'] = 'PowDecay'

bgLimitDict[True]['8TeV']['el']['0'] = 'TripExpSum'
bgLimitDict[True]['8TeV']['el']['1'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['2'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['3'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['4'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['5'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['6'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['7'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['8'] = 'PowDecay'
bgLimitDict[True]['8TeV']['el']['9'] = 'PowDecay'

bgLimitDict[False]['8TeV']['mu']['0'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['1'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['2'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['3'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['4'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['5'] = 'Bern3'
bgLimitDict[False]['8TeV']['mu']['6'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['7'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['8'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['mu']['9'] = 'GaussBern5'

bgLimitDict[False]['8TeV']['el']['0'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['1'] = 'GaussBern4'
bgLimitDict[False]['8TeV']['el']['2'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['3'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['4'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['5'] = 'Bern4'
bgLimitDict[False]['8TeV']['el']['6'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['7'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['8'] = 'GaussBern5'
bgLimitDict[False]['8TeV']['el']['9'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['mu']['0'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['1'] = 'GaussBern4'
bgLimitDict[False]['7TeV']['mu']['2'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['3'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['mu']['4'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['el']['0'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['1'] = 'GaussBern4'
bgLimitDict[False]['7TeV']['el']['2'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['3'] = 'GaussBern5'
bgLimitDict[False]['7TeV']['el']['4'] = 'GaussBern5'

bgLimitDict[False]['7TeV']['all']['5'] = 'Bern3'

#if __name__=='configLimits':
#  for name in dir():
#      myvalue = eval(name)
#      if '__' not in name:
#        print name, "=", myvalue

##################################################################################################
##################################################################################################
########################################## BIAS STUDY ############################################
##################################################################################################
##################################################################################################

######################
# biasStudy_toyMaker #
######################

if highMass:
  testFuncs = bgFitListHighMass
  #testFuncs = ['PowDecay','PowLog','ExpSum','TripExpSum','PowExpSum','TripPowSum']
  testFuncs = ['PowDecay','ExpSum','TripExpSum','PowExpSum','TripPowSum']
  #testFuncs = ['TripExpSum']
  #genFuncs = ['Pow','Laurent','Exp2','Gamma','Weibull','Hill']
  genFuncs = ['Gamma']
else:
  testFuncs = bgFitListTurnOn
  genFuncs = ['GaussPow']

trials = 100
#trials = 1
jobs = 100
#jobs = 1
plotEvery = 50
#plotEvery = 1

#############
# pullPlots #
#############

# no special switches

##############
# makeTables #
##############
tableFuncs = ['PowDecay','ExpSum','PowExpSum','TripExpSum','TripPowSum']


