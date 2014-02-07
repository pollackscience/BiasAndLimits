#!/usr/bin/env python
import os
import sys

def produceLimits(inputFolder = 'testCards/', outPutFolder = 'limitOutputs/', mass = '125.0'):
  fullCombo = True
  byParts = False
  MVATest = True
  suffix = 'MVA_02-06-14_Cats'

  leptonList = ['mu','el']
  yearList = ['2012','2011']
  catListBig = ['1','2','3','4','5','6','7','8','9']
  catListSmall = ['1','2','3','4','5']

  if fullCombo:
    cardNames = ''
    if MVATest:
      comboName = inputFolder+'_'.join(['hzg','FullCombo','M'+mass,suffix])+'.txt'
      outputName = outPutFolder+'_'.join(['Output','FullCombo','M'+mass,suffix])+'.txt'
    else:
      comboName = inputFolder+'_'.join(['hzg','FullCombo','M'+mass])+'.txt'
      outputName = outPutFolder+'_'.join(['Output','FullCombo','M'+mass])+'.txt'
    for year in yearList:
      if year == '2011': catList = catListSmall
      else: catList = catListBig
      for lepton in leptonList:
        for cat in catList:
          if year is '2011' and cat is '5' and lepton is 'mu': continue
          elif year is '2011' and cat is '5' and lepton is 'el': lepton='all'
          if MVATest:
            cardNames = cardNames+' '+inputFolder+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass,suffix])+'.txt'
          else:
            cardNames = cardNames+' '+inputFolder+'_'.join(['hzg',lepton,year,'cat'+cat,'M'+mass])+'.txt'
    print 'making combined cards'
    print 'combineCards.py '+cardNames+' > '+comboName
    os.system('combineCards.py '+cardNames+' > '+comboName)
    print 'running limit software, M:',mass
    os.system('combine -M Asymptotic '+comboName+' > '+outputName)
    #os.system('combine -M ProfileLikelihood '+comboName+' > '+outputName)

if __name__ == "__main__":
  print sys.argv
  if len(sys.argv)<2:
    produceLimits()
  elif len(sys.argv) is 2:
    produceLimits('testCards/','',str(sys.argv[1]))
  elif len(sys.argv) is 4:
    produceLimits(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))
  else:
    'you did something wrong'
