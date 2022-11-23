# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Steedle.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction
import pyautogui as pg


#import Steedle_sercom
from Motor_controller import motor_controller

Controller = motor_controller()
const = 365
const2 =372
_translate = QtCore.QCoreApplication.translate


#Set up empty list to display messages:
Messages = ""

button_style = ("QPushButton::pressed"
                "{"
                "border: 2px solid;"
                "border-color: rgb(255, 255, 255)"
                "}"
                                               
                "QPushButton::hover"
                "{"
                "background-color: rgb( 0, 134, 172);"
                "}"
                                               
                "QPushButton{\n"
                "border-radius: 15px;\n"
                "border: none;"
                "background-color: rgb( 0, 166, 214);\n"
                "color: rgb(255, 255, 255);"
                "}")

button_style2 = ("QPushButton::pressed"
                "{"
                "border: 4px solid;"
                "border-color: rgb( 255, 255, 255)"
                "}"
                                               
                "QPushButton::hover"
                "{"
                "border-color: rgb( 0, 134, 172);"
                "}"
                                               
                "QPushButton{\n"
                "background-color: rgb(61, 61, 60);\n"
                "border: 2px solid rgb(0,166,214);\n"
                "border-bottom-right-radius: 4px;\n"
                "border-top-right-radius: 4px;\n"
                "border-bottom-left-radius: 10px;\n"
                "border-top-left-radius: 10px;\n"
                "image: url(Minus_arrow.png);"
                "}")

button_style3 = ("QPushButton::pressed"
                "{"
                "border: 4px solid;"
                "border-color: rgb( 255, 255, 255)"
                "}"
                                               
                "QPushButton::hover"
                "{"
                "border-color: rgb( 0, 134, 172);"
                "}"
                
                "QPushButton{\n"
                "border: 2px solid rgb(0,166,214);\n"
                "border-bottom-right-radius: 10px;\n"
                "border-top-right-radius: 10px;\n"
                "border-bottom-left-radius: 4px;\n"
                "border-top-left-radius: 4px;\n"
                "image: url(Plus_arrow.png);"
                "}")
                         

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #MainWindow
        app.aboutToQuit.connect(self.closeEvent)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize( 1900, 1080)
        font = QtGui.QFont()
        font.setPointSize(18)
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(QtGui.QIcon("TargetV2.png"))
        
        #Centralwidget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(61, 61, 60);")
        self.centralwidget.setObjectName("centralwidget")
        
        #Steedle_control_panal_T
        self.steedle_control_panel_T = QtWidgets.QLabel(self.centralwidget)
        self.steedle_control_panel_T.setGeometry(QtCore.QRect(590, 40, 800, 100))
        font = QtGui.QFont()
        font.setPointSize(35)
        font.setBold(True)
        font.setWeight(75)
        self.steedle_control_panel_T.setFont(font)
        self.steedle_control_panel_T.setStyleSheet("color: rgb(255, 255, 255);")
        self.steedle_control_panel_T.setAlignment(QtCore.Qt.AlignCenter)
        self.steedle_control_panel_T.setObjectName("steedle_control_panel_T")
        
        self.Setting_panel = QtWidgets.QWidget(self.centralwidget)
        self.Setting_panel.setGeometry(QtCore.QRect(130, 200, 600, 580))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Setting_panel.setFont(font)
        self.Setting_panel.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 3px solid rgb(0, 166, 214);\n"
"border-radius: 25px;")
        self.Setting_panel.setObjectName("Setting_panel")
        self.Connection_status_T = QtWidgets.QLabel(self.Setting_panel)
        self.Connection_status_T.setGeometry(QtCore.QRect(25, 100, 260, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Connection_status_T.setFont(font)
        self.Connection_status_T.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               "border: None;\n"
                                               "")
        self.Connection_status_T.setObjectName("Connection_status_T")
        self.Set_X_pos_T = QtWidgets.QLabel(self.Setting_panel)
        self.Set_X_pos_T.setGeometry(QtCore.QRect(25, 250, 260, 35))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Set_X_pos_T.setFont(font)
        self.Set_X_pos_T.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border: None;")
        self.Set_X_pos_T.setObjectName("Set_X_pos_T")
        self.Set_Y_pos_T = QtWidgets.QLabel(self.Setting_panel)
        self.Set_Y_pos_T.setGeometry(QtCore.QRect(25, 300, 260, 35))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Set_Y_pos_T.setFont(font)
        self.Set_Y_pos_T.setStyleSheet("color: rgb(255, 255, 255);\n"
                                       "border: None;")
        
        self.Set_Y_pos_T.setObjectName("Set_Y_pos_T")
        
        """
        self.Set_insertion_speed_T = QtWidgets.QLabel(self.Setting_panel)
        self.Set_insertion_speed_T.setGeometry(QtCore.QRect(25, 420, 265, 35))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Set_insertion_speed_T.setFont(font)
        self.Set_insertion_speed_T.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                 "border: None;")
        self.Set_insertion_speed_T.setObjectName("Set_insertion_speed_T")
        """
        
        self.Homing_status_T = QtWidgets.QLabel(self.Setting_panel)
        self.Homing_status_T.setGeometry(QtCore.QRect(25, 140, 260, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Homing_status_T.setFont(font)
        self.Homing_status_T.setStyleSheet("border: None;")
        self.Homing_status_T.setObjectName("Homing_status_T")
        self.Settings_T = QtWidgets.QLabel(self.Setting_panel)
        self.Settings_T.setGeometry(QtCore.QRect(200, 10, 200, 80))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.Settings_T.setFont(font)
        self.Settings_T.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: None;")
        self.Settings_T.setAlignment(QtCore.Qt.AlignCenter)
        self.Settings_T.setObjectName("Settings_T")
        
        
        self.Connection_status = QtWidgets.QLabel(self.Setting_panel)
        self.Connection_status.setGeometry(QtCore.QRect(310, 100, 260, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Connection_status.setFont(font)
        self.Connection_status.setStyleSheet("color:  rgb(85, 255, 127);\n"
                                             "border: None;")
        self.Connection_status.setObjectName("Connection_status")
        self.Homing_status = QtWidgets.QLabel(self.Setting_panel)
        self.Homing_status.setGeometry(QtCore.QRect(310, 140, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Homing_status.setFont(font)
        self.Homing_status.setStyleSheet("color:  rgb( 0, 134, 172);\n"
                                         "border: None;")
        self.Homing_status.setObjectName("Homing_status")
        
        #Home button
        self.Home_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Home_BT.setGeometry(QtCore.QRect(185, 200, 230, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Home_BT.setFont(font)
        self.Home_BT.setStyleSheet(button_style)
        self.Home_BT.setObjectName("Home_BT")
        self.Home_BT.clicked.connect(self.Home)
        
        #Move needle tip button
        self.Move_needle_tip_B = QtWidgets.QPushButton(self.Setting_panel)
        self.Move_needle_tip_B.setGeometry(QtCore.QRect(175, 355, 250, 45))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Move_needle_tip_B.setFont(font)
        self.Move_needle_tip_B.setStyleSheet(button_style)
        self.Move_needle_tip_B.setObjectName("Move_needle_tip_B")
        self.Move_needle_tip_B.clicked.connect(self.Move_needle_tip)
        
        
        #Start insertion button
        self.Start_insertion_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Start_insertion_BT.setGeometry(QtCore.QRect(175, 500, 250, 45))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Start_insertion_BT.setFont(font)
        self.Start_insertion_BT.setStyleSheet(button_style)
        self.Start_insertion_BT.setObjectName("Start_insertion_BT")
        self.Start_insertion_BT.clicked.connect(self.Insert)
        
        #X minus one
        self.Min_X_pos_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Min_X_pos_BT.setGeometry(QtCore.QRect(310, 255, 35, 35))
        self.Min_X_pos_BT.setStyleSheet(button_style2)
        self.Min_X_pos_BT.setText("")
        self.Min_X_pos_BT.setObjectName("Min_X_pos_BT")
        self.Min_X_pos_BT.clicked.connect(lambda: self.Minus_one(0))
        
        #X plus one line edit
        self.X_pos_LE = QtWidgets.QLineEdit(self.Setting_panel)
        self.X_pos_LE.setGeometry(QtCore.QRect(350, 255, 80, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.X_pos_LE.setFont(font)
        self.X_pos_LE.setStyleSheet("border: 2px solid;\n"
                                    "border-radius: 5px;\n"
                                    "border-color: rgb(0,166,214);\n"
                                    "")
        self.X_pos_LE.setAlignment(QtCore.Qt.AlignCenter)
        self.X_pos_LE.setObjectName("X_pos_LE")
        self.X_pos_LE.setPlaceholderText("X-pos")
        
        #X plus one button
        self.Plus_X_pos_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Plus_X_pos_BT.setGeometry(QtCore.QRect(435, 255, 35, 35))
        self.Plus_X_pos_BT.setStyleSheet(button_style3)
        self.Plus_X_pos_BT.setText("")
        self.Plus_X_pos_BT.setObjectName("Plus_X_pos_BT")
        self.Plus_X_pos_BT.clicked.connect(lambda: self.Plus_one(0))
        
        #Y min one button
        self.Min_Y_pos_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Min_Y_pos_BT.setGeometry(QtCore.QRect(310, 300, 35, 35))
        self.Min_Y_pos_BT.setStyleSheet(button_style2)
        self.Min_Y_pos_BT.setText("")
        self.Min_Y_pos_BT.setObjectName("Min_Y_pos_BT")
        self.Y_pos_LE = QtWidgets.QLineEdit(self.Setting_panel)
        self.Y_pos_LE.setGeometry(QtCore.QRect(350, 300, 80, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Min_Y_pos_BT.clicked.connect(lambda: self.Minus_one(1))
        
        #Y position line edit
        self.Y_pos_LE.setFont(font)
        self.Y_pos_LE.setStyleSheet("border: 2px solid;\n"
                                    "border-radius: 5px;\n"
                                    "border-color: rgb(0,166,214);\n"
                                    "")
        self.Y_pos_LE.setObjectName("Y_pos_LE")
        self.Y_pos_LE.setAlignment(QtCore.Qt.AlignCenter)
        self.Y_pos_LE.setPlaceholderText("Y-pos")
        
        #Y plus one button
        self.Plus_Y_pos_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Plus_Y_pos_BT.setGeometry(QtCore.QRect(435, 300, 35, 35))
        self.Plus_Y_pos_BT.setStyleSheet(button_style3)
        self.Plus_Y_pos_BT.setText("")
        self.Plus_Y_pos_BT.setObjectName("Plus_Y_pos_BT")
        self.Plus_Y_pos_BT.clicked.connect(lambda: self.Plus_one(1))
        
        #Min_insertion_depth_BT
        self.Min_insertion_depth_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Min_insertion_depth_BT.setGeometry(QtCore.QRect(310, 430, 35, 35))
        self.Min_insertion_depth_BT.setStyleSheet(button_style2)
        self.Min_insertion_depth_BT.setText("")
        self.Min_insertion_depth_BT.setObjectName("Min_insertion_depth_BT")
        self.Min_insertion_depth_BT.clicked.connect(lambda: self.Minus_one(2))
        
        #Insertion depth line edit
        self.Insertion_depth_LE = QtWidgets.QLineEdit(self.Setting_panel)
        self.Insertion_depth_LE.setGeometry(QtCore.QRect(350, 430, 80, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        
        #Insertion_depth_LE
        self.Insertion_depth_LE.setFont(font)
        self.Insertion_depth_LE.setStyleSheet("border: 2px solid;\n"
                                              "border-radius: 5px;\n"
                                              "border-color: rgb(0,166,214);\n"
                                              "")
        self.Insertion_depth_LE.setObjectName("Insertion_depth_LE")
        self.Insertion_depth_LE.setAlignment(QtCore.Qt.AlignCenter)
        self.Insertion_depth_LE.setPlaceholderText("Depth")
        #self.Insertion_depth.returnPressed.connect(change_text)
        
        #Insertion depth plus one
        self.Plus_insertion_depth_BT = QtWidgets.QPushButton(self.Setting_panel)
        self.Plus_insertion_depth_BT.setGeometry(QtCore.QRect(435, 430, 35, 35))
        self.Plus_insertion_depth_BT.setStyleSheet(button_style3)
        self.Plus_insertion_depth_BT.setText("")
        self.Plus_insertion_depth_BT.setObjectName("Plus_insertion_depth_BT")
        self.Plus_insertion_depth_BT.clicked.connect(lambda: self.Plus_one(2))
        
        #Insertion depth title
        self.Set_intersion_depth_T = QtWidgets.QLabel(self.Setting_panel)
        self.Set_intersion_depth_T.setGeometry(QtCore.QRect(25, 430, 265, 35))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Set_intersion_depth_T.setFont(font)
        self.Set_intersion_depth_T.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                 "border: None;")
        self.Set_intersion_depth_T.setObjectName("Set_intersion_depth_T")
        
        #Click on target widget
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(900, 130, 838, 763))
        self.widget_2.setObjectName("widget_2")
        
        #Click on target button
        self.Click_on_target = QtWidgets.QPushButton(self.widget_2)
        self.Click_on_target.setGeometry(QtCore.QRect(0, 0, 838, 763))
        self.Click_on_target.setStyleSheet("image: url(TargetV2.png);"
                                           "border: None;")
        self.Click_on_target.setText("")
        self.Click_on_target.setObjectName("Click_on_target")
        self.Click_on_target.pressed.connect(self.click_target)
            
        #Target
        self.Needle_pos = QtWidgets.QLabel(self.widget_2)      
        self.Needle_pos.setStyleSheet("background-color: rgb(255, 0, 0);\n"
                                      "border-radius: 10px;")
        self.Needle_pos.setText("")
        self.Needle_pos.setObjectName("Needle_pos")
        self.x_tag = 387
        self.y_tag = 368
        self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
               
        #Click on target title
        self.Clic_on_target_T = QtWidgets.QLabel(self.centralwidget)
        self.Clic_on_target_T.setGeometry(QtCore.QRect(900, 900, 838, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Clic_on_target_T.setFont(font)
        self.Clic_on_target_T.setStyleSheet("color: rgb(255, 255, 255);")
        self.Clic_on_target_T.setAlignment(QtCore.Qt.AlignCenter)
        #self.Clic_on_target_T.setObjectName("Clic_on_target_T")
        
        #Message box
        self.Message_box = QtWidgets.QLabel(self.centralwidget)
        self.Message_box.setGeometry(QtCore.QRect( 385, 820, 565, 150))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Message_box.setFont(font)
        self.Message_box.setStyleSheet("color: rgb(255, 255 ,255);\n"
                                       "border: 3px solid rgb(0, 166, 214);\n"
                                       "border-radius: 20px;")
        self.Message_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        
        #Message box title
        self.Message_box.setObjectName("Message_box")
        self.Message_box_T = QtWidgets.QLabel(self.centralwidget)
        self.Message_box_T.setGeometry(QtCore.QRect( 130, 820, 230, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.Message_box_T.setFont(font)
        self.Message_box_T.setStyleSheet("color: rgb(255,255,255);\n"
                                         "")
        self.Message_box_T.setObjectName("Message_box_T")
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.steedle_control_panel_T.setText(_translate("MainWindow", "Steedle control panel"))
        self.Connection_status_T.setText(_translate("MainWindow", "Connection status:"))
        self.Set_X_pos_T.setText(_translate("MainWindow", "Set X-position:"))
        self.Set_Y_pos_T.setText(_translate("MainWindow", "Set Y-position:"))
        self.Homing_status_T.setText(_translate("MainWindow", "Homing status:"))
        self.Settings_T.setText(_translate("MainWindow", "Settings"))
        self.Connection_status.setText(_translate("MainWindow", "You are connected"))
        self.Homing_status.setText(_translate("MainWindow", "Steedle is not home"))
        self.Home_BT.setText(_translate("MainWindow", "Home"))
        self.Move_needle_tip_B.setText(_translate("MainWindow", "Move extremity"))
        self.Start_insertion_BT.setText(_translate("MainWindow", "Start insertion"))
        self.Set_intersion_depth_T.setText(_translate("MainWindow", "Set insertion depth:"))
        self.Clic_on_target_T.setText(_translate("MainWindow", "Click on the target to set the needle tip position"))
        self.Message_box.setText(_translate("MainWindow", "> You don't have any messages"))
        self.Message_box_T.setText(_translate("MainWindow", "Messages box:"))

#########################################################################################################################
                                                            #Button actions#
#########################################################################################################################
    def Move_needle_tip(self):
        X = int(self.X_pos_LE.text())
        Y = int(self.Y_pos_LE.text())
        
        X_coord, Y_coord = Controller.Move_tip( X, Y)
        
        global Messages
        Messages = "> X_pos = {}, Y_pos = {} \n".format(int(X_coord), int(Y_coord)) + Messages
        self.Message_box.setText(_translate("MainWindow", Messages))
    
    def Insert(self):
        depth = int(self.Insertion_depth_LE.text())    
        Current_X, Current_Y, X_coord, Y_coord = Controller.Insert(depth)
    
        global Messages
        
        if Current_X != 'To much':
            self.X_pos_LE.setText('{}'.format( Current_X))
            self.Y_pos_LE.setText('{}'.format( Current_Y))
                       
            Messages = "> X_pos = {}, Y_pos = {} \n".format(int(X_coord), int(Y_coord)) + Messages
            self.Message_box.setText(_translate("MainWindow", Messages))
                  
        else:
            Messages = ">You can't take out the needle tip this far\n" + Messages
            self.Message_box.setText(_translate("MainWindow", Messages))
                 
    def closeEvent(self):
        Controller.close_connection()
    
    def Home(self):
        Controller.Home()
        self.Homing_status.setStyleSheet("color:  rgb( 85, 255, 127);\n"
                                         "border: None;")
        self.Homing_status.setText(_translate("MainWindow", "Steedle is home"))
    
    def click_target(self):
        x, y = pg.position()
        R_targ = 362                 #Radius of circle in pixels
        x_widg = x - 1297
        y_widg = 543 - y
        x_Le = int(100 -((R_targ - x_widg)/R_targ)*100)
        y_Le = int(100 -((R_targ - y_widg)/R_targ)*100)
       
        self.Needle_pos.setObjectName("Needle_pos")
        self.X_pos_LE.setText('{}'.format(x_Le))
        self.Y_pos_LE.setText('{}'.format(y_Le))
        self.x_tag = x - 905
        self.y_tag = y - 165
        
        self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
        QtCore.QCoreApplication.processEvents()
    
    def Minus_one(self, x):        
        Arr_1 = [self.X_pos_LE.text(),
                 self.Y_pos_LE.text(),
                 self.Insertion_depth_LE.text()]   
    
        if Arr_1[x] != '':
            Minus_one = int(Arr_1[x]) - 1
        else:                                       #Check if line edit box is empty
            Minus_one = -1
        
        if x == 0:
            self.x_tag = int((const * Minus_one)/ 100) + const
            self.X_pos_LE.setText('{}'.format(Minus_one))
            self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
        elif x == 1:
            print('y_tag=', self.y_tag)
            self.y_tag = int((const2 * Minus_one)/ 100)*-1 + const2 + 10
            self.Y_pos_LE.setText('{}'.format(Minus_one))
            print(self.y_tag, const2, Minus_one)
            self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
        else:
            self.Insertion_depth_LE.setText('{}'.format(Minus_one))
    
    def Plus_one(self, x):       
        Arr_1 = [self.X_pos_LE.text(),
                 self.Y_pos_LE.text(),
                 self.Insertion_depth_LE.text()]
      
        if Arr_1[x] != '':
            Plus_one = int(Arr_1[x]) + 1
        else:                                       #Check if line edit box is empty
            Plus_one = +1
        
        if x == 0:
            self.x_tag = int((const * Plus_one)/ 100) + const
            self.X_pos_LE.setText('{}'.format(Plus_one))
            self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
        elif x == 1:
            self.y_tag = int((const2 * Plus_one)/ 100)*-1 + const2 + 10
            print(self.y_tag)
            self.Y_pos_LE.setText('{}'.format(Plus_one))
            self.Needle_pos.setGeometry(QtCore.QRect( self.x_tag, self.y_tag, 20, 20))
        else:
            self.Insertion_depth_LE.setText('{}'.format(Plus_one))
        
        
#import source_rc

if __name__ == "__main__":   
    app = QtWidgets.QApplication(sys.argv)
    
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.showMaximized()
    sys.exit(app.exec_())
        
      
    
