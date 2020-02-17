import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QFileDialog
#from PyQt5.QtCore import pyqtSignal, pyqtSlot  ## may need later

import numpy as np

#################################################################
#### import matplotlib classes to enable plots in PyQt5
#################################################################
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


#### Initialize Death Prob Arrays based on 2016 data                          ####
#### These stats are taken from: https://www.ssa.gov/oact/STATS/table4c6.html ####
####                                                                          ####
#### Originally had these as part of the uiMainWindow class not sure what the ####
#### standard practice should be.  Pulled them out as globas vars to experiment ##
deathProbAge = np.array([50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,
                80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,
                108,109,110,111,112,113,114,115,116,117,118,119])

deathProbMale = np.array([0.005007,0.005493,0.006016,0.006575,0.00717,0.007805,0.008477,0.009181,0.009916,0.010683,
                0.011533,0.012434,0.013302,0.014109,0.014913,0.015808,0.016868,0.018101,0.019544,0.021206,
                0.023122,0.025265,0.027585,0.03007,0.032794,0.035963,0.039588,0.043511,0.04772,0.052358,
                0.057712,0.063886,0.070782,0.078442,0.086997,0.096603,0.10739,0.119456,0.132853,0.147599,
                0.163689,0.181104,0.19981,0.219765,0.240913,0.261868,0.282225,0.301555,0.319421,0.335392,
                0.352162,0.36977,0.388259,0.407672,0.428055,0.449458,0.471931,0.495527,0.520304,0.546319,
                0.573635,0.602317,0.632432,0.664054,0.697257,0.732119,0.768725,0.807162,0.84752,0.889896])

deathProbFemale = np.array([0.003193,0.003492,0.003803,0.004126,0.004462,0.004829,0.00522,0.005612,0.006,0.006397,
                    0.006848,0.007358,0.007893,0.008453,0.009063,0.009761,0.010581,0.011535,0.012646,0.013919,
                    0.015413,0.017089,0.018861,0.020705,0.022703,0.025035,0.027766,0.030822,0.034227,0.038062,
                    0.042539,0.047663,0.053278,0.059378,0.066132,0.073763,0.082465,0.09237,0.103546,0.115997,
                    0.129706,0.144636,0.160741,0.177971,0.19627,0.214769,0.233174,0.251158,0.268378,0.284481,
                    0.30155,0.319643,0.338821,0.359151,0.3807,0.403542,0.427754,0.45342,0.480625,0.509462,0.54003,
                    0.572432,0.606778,0.643184,0.681775,0.722682,0.766043,0.807162,0.84752,0.889896])
#### Initialize these arrays to zero ####
probLiveMale = np.zeros(40)
probLiveFemale = np.zeros(40)
probLiveJoint = np.zeros(40)





class MplFigure(object):
    def __init__(self, parent):
        self.figure = plt.figure(facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, parent)


        

class uiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('RetirementPlngV2.ui', self)  #### load Qt Designer UI design
        self.version = "0.2"
        self.setWindowTitle("Retirement Planner " + self.version)


        #### Stock, Bond and CPI Historical Data - used to calc defaults vals ####
        #### These stats are taken from: Bogleheads Backdating Spreadsheets   ####
        #### http://bit.ly/36W8sXF                                            ####
        ####                                                                  ####
        # S&P Total Return since 1871
        stockTR = [15.64,11.23,-2.47,4.71,5.35,-14.17,-1.34,16.25,49.41,26.69,
            0.31,3.61,-5.48,-12.38,29.90,11.94,-0.63,3.29,7.06,-6.16,
            18.88,6.16,-18.80,3.56,4.96,3.22,20.37,29.34,3.68,20.95,
            19.46,8.29,-17.09,32.10,21.31,0.70,-24.18,39.42,16.19,-3.38,
            3.52,7.18,-4.74,-5.47,31.22,8.23,-18.54,18.06,19.63,-13.98,
            10.08,29.13,5.46,27.12,25.87,11.56,37.16,47.62,-9.43,-22.73,
            -44.26,-6.16,56.66,-8.00,54.96,32.72,-34.73,30.76,-0.38,-9.77,
            -11.59,20.15,25.63,19.53,36.31,-8.02,5.63,5.37,18.60,31.46,
            23.97,18.16,-0.94,52.27,31.41,6.48,-10.72,43.15,11.95,0.45,
            26.88,-8.66,22.76,16.43,12.46,-10.02,23.89,11.04,-8.40,3.89,
            14.30,19.00,-14.69,-26.47,37.23,23.93,-7.16,6.57,18.61,32.50,
            -4.92,21.55,22.56,6.27,31.73,18.67,5.25,16.61,31.69,-3.10,30.47,
            7.62,10.08,1.32,37.58,22.96,33.36,28.58,21.04,-9.10,-11.89,
            -22.10,28.68,10.88,4.91,15.79,5.49,-37.00,26.46,15.06,2.11,
            16.00,32.39,13.69,1.38,11.96,21.83,-4.38,31.49]

        # T-Bills Total Return since 1871
        bondTR = [6.35,7.81,8.35,6.86,4.96,5.33,5.03,4.90,4.25,5.10,
            4.79,5.26,5.35,5.65,4.22,4.26,6.11,5.02,4.68,5.41,
            5.97,3.93,8.52,3.32,3.09,5.76,3.44,3.55,3.36,4.64,
            4.30,4.72,5.50,4.34,4.17,5.47,6.23,5.32,3.65,5.26,
            4.00,4.35,5.65,4.64,3.65,3.64,4.25,5.98,5.56,7.30,
            7.44,4.58,4.96,4.34,3.87,4.28,4.26,4.64,6.01,4.15,
            2.43,3.36,1.46,0.32,0.18,0.17,0.30,0.08,0.04,0.03,
            0.08,0.34,0.38,0.38,0.38,0.38,0.57,1.03,1.11,1.18,
            1.49,1.68,1.91,0.97,1.67,2.58,3.27,1.79,3.29,3.08,
            2.29,2.81,3.15,3.55,3.96,4.93,4.40,5.36,6.73,6.85,
            4.62,4.01,6.90,8.01,6.13,5.06,5.23,7.11,10.31,11.70,
            15.08,11.47,8.72,9.96,7.70,6.17,5.85,6.61,8.36,7.77,
            5.73,3.45,3.02,4.04,5.63,5.12,5.15,4.81,4.59,5.89,
            3.72,1.67,1.03,1.23,3.04,4.76,4.72,1.59,0.14,0.13,
            0.07,0.08,0.06,0.03,0.03,0.28,0.87,1.86,2.14]

        # Inflation since 1871
        cpiHist = [1.53,2.26,-4.41,-6.92,-5.79,0.88,-15.65,-10.31,20.69,-5.71,
            8.08,-1.87,-7.62,-10.31,-3.45,0.00,4.76,-4.55,-4.76,2.50,
            -6.10,7.79,-13.25,-4.17,1.45,-2.86,2.94,1.43,16.90,-2.41,
            2.47,9.64,-4.40,2.30,0.00,4.49,-2.15,3.30,10.64,-6.73,
            -1.03,7.29,2.04,1.00,2.97,12.50,19.66,17.86,16.97,-1.55,
            -11.05,-0.59,2.98,0.00,3.47,-2.23,-1.14,-1.16,0.00,-7.02,
            -10.06,-9.79,2.33,3.03,1.47,2.17,2.86,-2.78,0.00,0.71,
            9.93,9.03,2.96,2.30,2.25,18.13,8.84,2.99,-2.07,5.93,
            6.00,0.75,0.75,-0.74,0.37,2.99,2.90,1.76,1.73,1.36,
            0.67,1.33,1.64,0.97,1.92,3.46,3.04,4.72,6.20,5.57,
            3.27,3.41,8.71,12.34,6.94,4.86,6.70,9.02,13.29,12.52,
            8.92,3.83,3.79,3.95,3.80,1.10,4.43,4.42,4.65,6.11,
            3.06,2.90,2.75,2.67,2.54,3.32,1.70,1.61,2.68,3.39,
            1.55,2.38,1.88,3.26,3.42,2.54,4.08,0.09,2.72,1.50,
            2.96,1.74,1.50,0.76,0.73,2.07,2.11,1.91,2.29]




        #### Populate default values into spinner boxes ####
        self.distrRate = 4.0
        self.cashNeeded = 40000
        self.stockPct = 60
        self.bondPct = 100 - self.stockPct
        self.totalPortfolio = self.cashNeeded/(self.distrRate/100)
        self.stockAmt = self.stockPct/100 * self.totalPortfolio
        self.bondAmt = self.bondPct/100 * self.totalPortfolio
        self.distrRateBox.setValue(self.distrRate)
        self.cashNeededBox.setValue(self.cashNeeded)
        self.stockPctEntryBox.setValue(self.stockPct)
        self.bondPctCalcBox.setValue(self.bondPct)
        self.totalPortfolioBox.setValue(self.totalPortfolio)
        self.stockAmtBox.setValue(self.stockAmt)
        self.bondAmtBox.setValue(self.bondAmt)

        self.stockAvg = np.average(stockTR)
        self.bondAvg = np.average(bondTR)
        self.cpiAvg = np.average(cpiHist)
        self.stockStdev = np.std(stockTR)
        self.bondStdev = np.std(bondTR)
        self.cpiStdev = np.std(cpiHist)
        self.stockAvgEntryBox.setValue(self.stockAvg)
        self.bondAvgEntryBox.setValue(self.bondAvg)
        self.cpiAvgEntryBox.setValue(self.cpiAvg)
        self.stockStdevEntryBox.setValue(self.stockStdev)
        self.bondStdevEntryBox.setValue(self.bondStdev)
        self.cpiStdevEntryBox.setValue(self.cpiStdev)

        self.rebalanceComboBox.addItems(["Rebalance Annually", "Do Not Rebalance", "Barbell", "4-yr Cash Buffer"])

        #### Populate values into age combo boxes (50 to 80)  ####
        self.ageSelectionList = np.linspace(50, 80, 31, dtype=int)
        for age in self.ageSelectionList:
            self.ageMComboBox.addItem(str(age))
            self.ageFComboBox.addItem(str(age))
        self.ageMComboBox.setCurrentIndex(15) # default index = 15 (65 yrs)
        self.ageFComboBox.setCurrentIndex(15) # default index = 15 (65 yrs)
        self.ageMComboBox.currentIndexChanged.connect(self.onValueChanged)
        self.ageFComboBox.currentIndexChanged.connect(self.onValueChanged)

        self.progressBar.setValue(0)


        covarMatrix = np.cov([stockTR, bondTR, cpiHist], rowvar=True)

        self.k00 = covarMatrix[0][0]
        self.k01 = covarMatrix[0][1]
        self.k02 = covarMatrix[0][2]
        self.k10 = covarMatrix[1][0]
        self.k11 = covarMatrix[1][1]
        self.k12 = covarMatrix[1][2]        
        self.k20 = covarMatrix[2][0]
        self.k21 = covarMatrix[2][1]
        self.k22 = covarMatrix[2][2]
        self.k00DoubleSpinBox.setValue(self.k00)
        self.k01DoubleSpinBox.setValue(self.k01)
        self.k02DoubleSpinBox.setValue(self.k02)
        self.k10DoubleSpinBox.setValue(self.k10)
        self.k11DoubleSpinBox.setValue(self.k11)
        self.k12DoubleSpinBox.setValue(self.k12)
        self.k20DoubleSpinBox.setValue(self.k20)
        self.k21DoubleSpinBox.setValue(self.k21)
        self.k22DoubleSpinBox.setValue(self.k22)

        #### Connect signals from menu item selections ####
        self.actionOpen.triggered.connect(lambda: self.clicked("Open Was Clicked" ))
        self.actionSave.triggered.connect(lambda: self.clicked("Save Was Clicked" ))
        self.actionClose.triggered.connect(sys.exit)
        self.actionAbout.triggered.connect(lambda: self.clicked("About Was Clicked" ))


        #### Connect signals from entry box changes ####
        self.distrRateBox.valueChanged.connect(self.onValueChanged)
        self.cashNeededBox.valueChanged.connect(self.onValueChanged)
        self.stockPctEntryBox.valueChanged.connect(self.onValueChanged)

        self.stockAvgEntryBox.valueChanged.connect(self.onValueChanged)
        self.bondAvgEntryBox.valueChanged.connect(self.onValueChanged)
        self.cpiAvgEntryBox.valueChanged.connect(self.onValueChanged)
        self.stockStdevEntryBox.valueChanged.connect(self.onValueChanged)
        self.bondStdevEntryBox.valueChanged.connect(self.onValueChanged)
        self.cpiStdevEntryBox.valueChanged.connect(self.onValueChanged)
        
        self.rebalanceComboBox.currentIndexChanged.connect(self.onValueChanged)

        self.redrawPushButton.clicked.connect(self.onValueChanged)

        self.k01DoubleSpinBox.valueChanged.connect(self.onValueChanged)
        self.k02DoubleSpinBox.valueChanged.connect(self.onValueChanged)
        self.k12DoubleSpinBox.valueChanged.connect(self.onValueChanged)

    
        #### Setup and initialize plotting area in the verticalLayout box ####
        self.main_figure = MplFigure(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.main_figure.toolbar)
        self.verticalLayout.addWidget(self.main_figure.canvas)
        #self.setLayout(self.verticalLayout)  # test for resizing -- does nothing obvious
        self.show()
        self.initMplWidget()




    #################################################################
    #### initialize MatPlotLib plot and update with default values
    #################################################################
    def initMplWidget(self):
        self.ax = self.main_figure.figure.add_subplot(111)
        self.ax2 = self.ax.twinx() # add "jt prob of being alive and broke" plot

        self.onValueChanged() # call event handler that reads input and updates plot
    #################################################################
        
    #################################################################
    #### This method handles clicking menu items and displays
	#### text that is passed using the triggered/clicked connects
    #################################################################
    def clicked(self, text):
        self.setStatusTip(text)
        if text == 'About Was Clicked':
            QMessageBox.about(self,"Retirement Planner", 
                                    "Retirement Planner Simulator \n" +
                                    "Version: " + self.version + "\n" +
                                    "Author: Steve Harbin \n" +
                                    "Date: Jan 31, 2020 \n\n" +
                                    "----------------------------------- \n" +
                                    "Uses Covariance: \n" +
                                    "Executes slower than v0.1 \n" +
                                    "Results Don't Change Significantly ")

        if text == 'Open Was Clicked':
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Parameters File", "", "Retirement Planner Files (*.rp);;All Files (*)")
            if fileName:
                try:
                    with open(fileName, "r") as paramFile:
                        self.distrRateBox.setValue(float(paramFile.readline()))
                        self.cashNeededBox.setValue(float(paramFile.readline()))
                        self.stockPctEntryBox.setValue(float(paramFile.readline()))
                        self.stockAvgEntryBox.setValue(float(paramFile.readline()))
                        self.stockStdevEntryBox.setValue(float(paramFile.readline()))
                        self.bondAvgEntryBox.setValue(float(paramFile.readline()))
                        self.bondStdevEntryBox.setValue(float(paramFile.readline()))
                        self.cpiAvgEntryBox.setValue(float(paramFile.readline()))
                        self.cpiStdevEntryBox.setValue(float(paramFile.readline()))
                        self.rebalanceComboBox.setCurrentIndex(int(paramFile.readline()))
                        self.ageMComboBox.setCurrentIndex(int(paramFile.readline()))
                        self.ageFComboBox.setCurrentIndex(int(paramFile.readline()))
                        self.k01DoubleSpinBox.setValue(float(paramFile.readline()))
                        self.k02DoubleSpinBox.setValue(float(paramFile.readline()))
                        self.k12DoubleSpinBox.setValue(float(paramFile.readline()))
                except Exception:
                    QMessageBox.warning(self,"Retirement Planner - File Open Warning",
                    "Open: " + fileName + "\n\nFile not compatible with Retirement Planner v" + self.version)

        if text == 'Save Was Clicked':
            fileName, _ = QFileDialog.getSaveFileName(self,"Save Current Parameters","*.rp","Retirement Planner Files (*.rp);;All Files (*)")
            if fileName:
                with open(fileName, "w") as paramFile:
                    paramFile.write(str(self.distrRate)+"\n")
                    paramFile.write(str(self.cashNeeded)+"\n")
                    paramFile.write(str(self.stockPct)+"\n")
                    paramFile.write(str(self.stockAvg)+"\n")
                    paramFile.write(str(self.stockStdev)+"\n")
                    paramFile.write(str(self.bondAvg)+"\n")
                    paramFile.write(str(self.bondStdev)+"\n")
                    paramFile.write(str(self.cpiAvg)+"\n")
                    paramFile.write(str(self.cpiStdev)+"\n")
                    paramFile.write(str(self.rebalanceComboBox.currentIndex()) + "\n")
                    paramFile.write(str(self.ageMComboBox.currentIndex()) + "\n")
                    paramFile.write(str(self.ageFComboBox.currentIndex()) + "\n")
                    paramFile.write(str(self.k01)+"\n")
                    paramFile.write(str(self.k02)+"\n")
                    paramFile.write(str(self.k12))
    #################################################################

    #################################################################
    #### This method to handles changes in spinner boxes and 
	#### display new value calculations then updates plot
    #################################################################
    #@pyqtSlot()   # Do I need this??
    def onValueChanged(self):
        self.distrRate = self.distrRateBox.value()
        self.cashNeeded = self.cashNeededBox.value()
        self.stockPct = self.stockPctEntryBox.value()

        self.bondPct = 100.0 - self.stockPct
        self.totalPortfolio = self.cashNeeded/(self.distrRate/100)
        self.stockAmt = self.stockPct/100 * self.totalPortfolio
        self.bondAmt = self.bondPct/100 * self.totalPortfolio

        self.bondPctCalcBox.setValue(self.bondPct)
        self.totalPortfolioBox.setValue(self.totalPortfolio)
        self.stockAmtBox.setValue(self.stockAmt)
        self.bondAmtBox.setValue(self.bondAmt)


        self.stockAvg = self.stockAvgEntryBox.value()
        self.bondAvg = self.bondAvgEntryBox.value()
        self.cpiAvg = self.cpiAvgEntryBox.value()
        self.stockStdev = self.stockStdevEntryBox.value()
        self.bondStdev = self.bondStdevEntryBox.value()
        self.cpiStdev = self.cpiStdevEntryBox.value()


        self.ageMSelected = int(self.ageMComboBox.currentText())
        self.ageFSelected = int(self.ageFComboBox.currentText())
        ####  Calculate probability of living based on SSA death stats arrays  ####
        ####  and values selected for M and F age when withdrawals start       #### <--- move to update plot method?
        probLiveMale[0] = 1   # Assumes male is alive when start withdrawals
        probLiveFemale[0] = 1 # Assumes female is alive when start withdrawals
        probLiveJoint[0] = 1
        for year in range(1, 40): 
            indexM = self.ageMSelected - deathProbAge[0] + year
            indexF = self.ageFSelected - deathProbAge[0] + year

            probLiveMale[year] = (1-deathProbMale[indexM]) * probLiveMale[year-1]
            probLiveFemale[year] = (1-deathProbFemale[indexF]) * probLiveFemale[year-1]
            probLiveJoint[year] = 1 - ( (1-probLiveMale[year]) * (1-probLiveFemale[year]) ) 


        ####  Handle changes to covariance boxes on Tab 2   ####
        self.k00 = self.stockStdev**2
        self.k01 = self.k01DoubleSpinBox.value()
        self.k02 = self.k02DoubleSpinBox.value()
        self.k10 = self.k01
        self.k11 = self.bondStdev**2
        self.k12 = self.k12DoubleSpinBox.value()
        self.k20 = self.k02
        self.k21 = self.k12
        self.k22 = self.cpiStdev**2

        self.k00DoubleSpinBox.setValue(self.k00)
        self.k01DoubleSpinBox.setValue(self.k01)
        self.k02DoubleSpinBox.setValue(self.k02)
        self.k10DoubleSpinBox.setValue(self.k10)
        self.k11DoubleSpinBox.setValue(self.k11)
        self.k12DoubleSpinBox.setValue(self.k12)
        self.k20DoubleSpinBox.setValue(self.k20)
        self.k21DoubleSpinBox.setValue(self.k21)
        self.k22DoubleSpinBox.setValue(self.k22)


        self.updatePlot()
    #################################################################


    ############ Recalculate and Redraw plot when values changed from the User Interface ############
    def updatePlot(self):
        # generates numScenarios x 40 array of normally-distributed random returns based on statistics entered
        numScenarios = 1000 # more than about 1,000 is very slow to execute but adds little to the convergence
                            # more than about 100 sometimes triggers spurious extra valuechange signals on doublespinboxes
        mean = [self.stockAvg, self.bondAvg, self.cpiAvg]
        cov = [[self.k00, self.k01, self.k02], [self.k10, self.k11, self.k12], [self.k20, self.k21, self.k22]] # covar of stock, t-bill, inflation 
        self.stockReturns, self.bondReturns, self.cpiReturns = np.random.multivariate_normal(mean, cov, size=(1, 40, numScenarios)).T
        self.bondReturns = np.abs(self.bondReturns)  # bond returns are always positive

        # To Do: Analyse distributions to see if standard_normal is the appropriate model for each

        # call algorithm corresponding to investment strategy selected
        if self.rebalanceComboBox.currentText() == "Rebalance Annually":
            self.RebalAlg(numScenarios) # call algorithm that rebalances annually
        elif self.rebalanceComboBox.currentText() == "Do Not Rebalance":
            self.noRebalAlg(numScenarios) # call algorithm that never rebalances
        elif self.rebalanceComboBox.currentText() == "Barbell":
            self.barbellAlg(numScenarios) # call algorithm that pulls from stocks in up years
        elif self.rebalanceComboBox.currentText() == "4-yr Cash Buffer":
            cashBuffer = 4 # number of years of cash (bonds) maintained to ride out down years
            self.bondAmt = cashBuffer * self.cashNeeded 
            self.stockAmt = max([self.totalPortfolio - self.bondAmt, 0])
            self.cashBuff4Alg(numScenarios, cashBuffer) # call algorithm that maintains 4 yrs of cash/bonds
        else:
            return # should never get here (leave space for additional algorithms)


        self.ax.clear()  #also clears titles and gridlines, etc.  Is there a better way to do this?
        self.ax.set_title('Portfolio Value')
        self.ax.set_xlabel('Retirement Year', fontsize=6)
        self.ax.set_ylabel('Portfolio Balance ($1,000)', fontsize=6)
        self.ax.grid(True) 
        self.ax.set_ylim(0,2000) 
        self.ax.set_xlim(1, 40) 

        ### Calculate 20th, 50th and 80th percentiles of portfolio balance each year and plot them
        retirementYr = np.linspace(1, 40, 40)
        self.ax.plot(retirementYr, np.percentile(self.portfBal/1000, 50., 0), '--')
        #self.ax.plot(retirementYr, np.average(self.portfBal/1000, 0), '--') # don't trust avg.  Skewed by zeroing values <0
        self.ax.plot(retirementYr, np.percentile(self.portfBal/1000, 20., 0), '-')
        self.ax.plot(retirementYr, np.percentile(self.portfBal/1000, 80., 0), '-')
        self.ax.plot(retirementYr, np.percentile(self.portfBal/1000, 2., 0), '--', linewidth=0.5, color="black")
        self.ax.fill_between(retirementYr, np.percentile(self.portfBal/1000,20.,0), np.percentile(self.portfBal/1000,80.,0), alpha=0.25)
        #self.ax.legend(["Median", "Average", "20th %", "80th %", "2nd %"], fontsize =6)
        self.ax.legend(["Median", "20th %", "80th %", "2nd %"], fontsize =6)

        for scenario in range(min([400, numScenarios])):  # plot some of the random sample points just for fun
            self.ax.plot(retirementYr, self.portfBal[scenario]/1000, 'bo', markersize=7, alpha=0.025)

        self.ax.figure.canvas.draw()



        ###### calculate percent of scenarios that did not have a zero portf balance                 ########
        ###### plot the joint probability that one or both spouses will outlive the portfolio        ########
        ###### jtProbLiv is based on SSA.gov 2016 tables and assumes M/F both alive at starting ages ########
        ###### Plots curve on second Y-axis using shared X-axis                                      ########
        jtProbLiv = probLiveJoint * 100
        self.ax2.clear()
        self.ax2.grid(True) 
        self.ax2.set_ylim(0,40) 
        self.ax2.set_ylabel('Probability of Either Spouse Outliving Portfolio (%)', fontsize=6)
        self.ax2.plot(retirementYr, (1-np.count_nonzero(self.portfBal,0)/numScenarios)*jtProbLiv, linewidth=2.0, color="red")

        ### use these to plot mortality curves for debugging purposes ####
        #self.ax2.plot(retirementYr, probLiveMale*100)
        #self.ax2.plot(retirementYr, probLiveFemale*100)
        #self.ax2.plot(retirementYr, probLiveJoint*100)

        self.ax2.legend(["Pr Outliving $"], fontsize =6)
        self.ax2.figure.canvas.draw()

    #####################################################################################

    #####################################################################################
    def noRebalAlg(self, numScenarios):
        ### Calculate portfolio balance changes for numScenarios monte carlo trials
        ### Assumes that portfolio is NOT rebalanced each year. Input parameters are starting values
        ### Takes distributions from bond portfolio until it is depleted then switch to stocks
        self.portfBal = np.zeros((numScenarios, 40)) # create a numScenarios x 40 array and fill with zeros
        for scenario in range(numScenarios):
            ### Calculate portfolio balance changes YoY based on entered parameters            
            distribution = self.cashNeeded*(1+self.cpiReturns[scenario][0]/100) # account for inflation on cash needs
            stockBal = self.stockAmt*(1+self.stockReturns[scenario][0]/100) # adjust for stock growth in year 0
            bondBal = self.bondAmt*(1+self.bondReturns[scenario][0]/100) - distribution # adjust for bond growth in year 0 & take distr from bond portfolio
            self.portfBal[scenario][0] = stockBal + bondBal  # adjust portfolio balance at end of year 0
            for year in range(1, 40):
                distribution = distribution*(1+self.cpiReturns[scenario][year]/100) # account for inflation on cash needs in year=year
                stockBal = stockBal*(1+self.stockReturns[scenario][year]/100) # adjust for stock growth in year=year
                bondBal = bondBal*(1+self.bondReturns[scenario][year]/100) # etc.
                if bondBal >= distribution:     # take distributions from bond portfolio if it has enough funds
                    bondBal = bondBal - distribution
                elif stockBal >= distribution:  # if bond funds are insufficient, take from stock portfolio
                    stockBal = stockBal - distribution
                else:                           # if neither stocks or bonds have sufficient funds, we are broke
                    break
                self.portfBal[scenario][year] = stockBal + bondBal  # take a distr at end of year
                if (self.portfBal[scenario][year]<distribution):
                    break  # Insufficient funds to keep going.  Breaking here speeds up the simulation
                    #pass # To Do: decide how to handle balances that are too low (zero out portfBal, end loop, etc.)
            self.progressBar.setValue(int(scenario/numScenarios*100))
        self.progressBar.setValue(100)
    #####################################################################################

    #####################################################################################
    def RebalAlg(self, numScenarios):
        ### Calculate portfolio balance changes for numScenarios monte carlo trials
        ### Portfolio is rebalanced each year per the input parameters for stock/bond mix
        self.portfBal = np.zeros((numScenarios, 40)) # create a numScenarios x 40 array and fill with zeros
        for scenario in range(numScenarios):
            ### Calculate portfolio balance changes YoY based on entered parameters            
            stockBal = self.stockAmt*(1+self.stockReturns[scenario][0]/100) # adjust for stock growth in year 0
            bondBal = self.bondAmt*(1+self.bondReturns[scenario][0]/100) # adjust for bond growth in year 0
            distribution = self.cashNeeded*(1+self.cpiReturns[scenario][0]/100) # account for inflation on cash needs
            self.portfBal[scenario][0] = stockBal + bondBal - distribution  # take a distr at end of year 0
            stockBal = self.stockPct/100*self.portfBal[scenario][0]  # rebalance stocks and bonds at end of year 0
            bondBal = self.bondPct/100*self.portfBal[scenario][0]
            for year in range(1, 40):
                stockBal = stockBal*(1+self.stockReturns[scenario][year]/100) # adjust for stock growth in year=year
                bondBal = bondBal*(1+self.bondReturns[scenario][year]/100) # etc.
                distribution = distribution*(1+self.cpiReturns[scenario][year]/100) # etc.
                self.portfBal[scenario][year] = stockBal + bondBal - distribution  # take a distr at end of year
                stockBal = self.stockPct/100*self.portfBal[scenario][year] # rebalance after at end of year
                bondBal = self.bondPct/100*self.portfBal[scenario][year]   # etc.
                if (self.portfBal[scenario][year]<distribution):
                    break  # Insufficient funds to keep going.  Breaking here speeds up the simulation
                    #pass # To Do: decide how to handle balances that are too low (zero out portfBal, end loop, etc.)
            self.progressBar.setValue(int(scenario/numScenarios*100))
        self.progressBar.setValue(100)
    #####################################################################################

    #####################################################################################
    def cashBuff4Alg(self, numScenarios, cashBuffer):
        ### Calculate portfolio balance changes for numScenarios monte carlo trials
        ### Portfolio maintains 4 years of cash/bonds each year and rest is invested in stocks
        self.portfBal = np.zeros((numScenarios, 40)) # create a numScenarios x 40 array and fill with zeros
        for scenario in range(numScenarios):
            ### Calculate portfolio balance changes YoY based on entered parameters            
            stockBal = self.stockAmt*(1+self.stockReturns[scenario][0]/100) # adjust for stock growth in year 0
            bondBal = self.bondAmt*(1+self.bondReturns[scenario][0]/100) # adjust for bond growth in year 0
            distribution = self.cashNeeded*(1+self.cpiReturns[scenario][0]/100) # account for inflation on cash needs
            self.portfBal[scenario][0] = stockBal + bondBal - distribution  # take a distr at end of year 0
            bondBal = bondBal - distribution # take funds from bond balance if sufficient. ToDo: need to test if sufficient
            for year in range(1, 40):
                stockBal = stockBal*(1+self.stockReturns[scenario][year]/100) # adjust for stock growth in year=year
                bondBal = bondBal*(1+self.bondReturns[scenario][year]/100) # etc.
                distribution = distribution*(1+self.cpiReturns[scenario][year]/100) # etc.
                self.portfBal[scenario][year] = stockBal + bondBal - distribution  # take a distr at end of year
                if bondBal >= distribution:
                    bondBal = bondBal - distribution # take funds from bond balance if sufficient
                    # Top off bondBal from stockBal to ride out down years
                    stockBal = max([stockBal - (cashBuffer*self.cashNeeded-bondBal), 0])
                    bondBal = self.portfBal[scenario][year] - stockBal  ####### THIS NEEDS TO BE LOOKED AT #####
                else:
                    bondBal = 0 # use up remaining bond balance
                    stockBal = max([self.portfBal[scenario][year] - distribution, 0]) # take additional from stocks
                    # Top off bondBal to ride out down years
                    stockBal = max([stockBal - (cashBuffer*self.cashNeeded-bondBal), 0])
                    bondBal = self.portfBal[scenario][year] - stockBal  ####### THIS NEEDS TO BE LOOKED AT #####
                if (self.portfBal[scenario][year]<distribution):
                    break  # Insufficient funds to keep going.  Breaking here speeds up the simulation
                    #pass # To Do: decide how to handle balances that are too low (zero out portfBal, end loop, etc.)
            self.progressBar.setValue(int(scenario/numScenarios*100))
        self.progressBar.setValue(100)
    #####################################################################################

     #####################################################################################
    def barbellAlg(self, numScenarios):
        ### Calculate portfolio balance changes for numScenarios monte carlo trials
        ### Distributions pull from stocks in an up year, bonds in a down year, stocks if NSF in bonds
        self.portfBal = np.zeros((numScenarios, 40)) # create a numScenarios x 40 array and fill with zeros
        for scenario in range(numScenarios):
            ### Calculate portfolio balance changes YoY based on entered parameters            
            stockBal = self.stockAmt*(1+self.stockReturns[scenario][0]/100) # adjust for stock growth in year 0
            bondBal = self.bondAmt*(1+self.bondReturns[scenario][0]/100) # adjust for bond growth in year 0
            distribution = self.cashNeeded*(1+self.cpiReturns[scenario][0]/100) # account for inflation on cash needs
            self.portfBal[scenario][0] = stockBal + bondBal - distribution  # take a distr at end of year 0
            stockBal = stockBal - distribution # take funds from sttock balance if sufficient. ToDo: need to test if sufficient
            for year in range(1, 40):
                stockBal = stockBal*(1+self.stockReturns[scenario][year]/100) # adjust for stock growth in year=year
                bondBal = bondBal*(1+self.bondReturns[scenario][year]/100) # etc.
                distribution = distribution*(1+self.cpiReturns[scenario][year]/100) # etc.
                if self.stockReturns[scenario][year] > 0: ## in an up year, take from stock portfolio if sufficient
                    if stockBal >= distribution:
                        stockBal = stockBal - distribution # take funds from stock balance if sufficient
                    else:
                        stockBal = 0 # use up remaining stock balance
                        bondBal = max([bondBal - distribution, 0]) # take additional from bonds                 
                else: ## in a down year, take from bond portfolio if sufficient
                    if bondBal >= distribution:
                        bondBal = bondBal - distribution # take funds from bond balance if sufficient
                    else:
                        bondBal = 0 # use up remaining bond balance
                        stockBal = max([stockBal - distribution, 0]) # take additional from stocks
                self.portfBal[scenario][year] = stockBal + bondBal  # update balance after distr taken out

                if (self.portfBal[scenario][year]<distribution):
                    break  # Insufficient funds to keep going.  Breaking here speeds up the simulation
                    #pass # To Do: decide how to handle balances that are too low (zero out portfBal, end loop, etc.)
            self.progressBar.setValue(int(scenario/numScenarios*100))
        self.progressBar.setValue(100)
    #####################################################################################
       




        

#######################################
#### Start application and UI Loop ####
if __name__ == "__main__":
    app = QApplication(sys.argv)        
    ui = uiMainWindow()
    ui.show()
    sys.exit(app.exec_())
######### End of application ##########
#######################################

