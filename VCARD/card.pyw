# -*- coding: utf-8 -*-
import sys 
import os
from PyQt4 import QtCore,QtGui 
from card_ui import Ui_MainWindow

try:
    import qrcode
except ImportError:
    qrcode = None
    
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

defaultFileName = "card_0.jpg"
defaultTempFileName = "card_temp_x3dt1d.jpg"
defaultLogoFileName = "logo.png"

class VCard(QtGui.QMainWindow): 
    def __init__(self, parent=None): 
        QtGui.QWidget.__init__(self, parent) 
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)
        # connect pushButton 
        QtCore.QObject.connect(self.ui.pushButton_make,QtCore.SIGNAL("clicked()"),self.onGenerateQRCode)
        QtCore.QObject.connect(self.ui.pushButton_openDialog,QtCore.SIGNAL("clicked()"),self.onChooseFile)
        QtCore.QObject.connect(self.ui.pushButton_save,QtCore.SIGNAL("clicked()"),self.onSaveQRCode)
        QtCore.QObject.connect(self.ui.pushButton_openLogo,QtCore.SIGNAL("clicked()"),self.onOpenLogo)
        # default save path
        self.ui.lineEdit_path.setText( (os.getcwd()+"\\"+defaultFileName).decode("gb18030") )
        self.ui.lineEdit_logoPath.setText( (os.getcwd()+"\\"+defaultLogoFileName).decode("gb18030") )
        self.m_logoName = _fromUtf8(defaultLogoFileName)
        self.showLogoOnScreen(self.m_logoName)
    
    #----------------------------------------------------------------------    
    def onOpenLogo(self):
        currentFile = self.ui.lineEdit_path.text()
        filedialog = QtGui.QFileDialog.getOpenFileName(filter=QtCore.QString("Images(*.jpg *.png *.gif *jpeg)"))
        if len(filedialog) == 0:
            filedialog = currentFile
        self.ui.lineEdit_logoPath.setText( filedialog )
        self.showLogoOnScreen( filedialog )
        self.m_logoName = filedialog
        
    #----------------------------------------------------------------------    
    
    def showLogoOnScreen(self,logopath):
        qlogo = QtGui.QImage()
        qlogo.load( logopath )
        logo_width = self.ui.label_logo.width()
        logo_height = self.ui.label_logo.height()
        qpixmap = QtGui.QPixmap()
        qpixmap.convertFromImage( qlogo.scaled(logo_width,logo_height) )
        self.ui.label_logo.setPixmap(qpixmap)    
    #----------------------------------------------------------------------
    
    def onSaveQRCode(self):
        currentFile = self.ui.lineEdit_path.text()
        self.m_image.save( currentFile )
        self.ui.statusbar.showMessage( _fromUtf8("文件保存成功！") )
    
    #----------------------------------------------------------------------    
    
    def onChooseFile(self):
        # init
        currentFile = self.ui.lineEdit_path.text()
        filedialog = QtGui.QFileDialog.getSaveFileName(filter=QtCore.QString("Images(*.jpg)"))
        if len(filedialog) == 0:
                filedialog = currentFile
        self.ui.lineEdit_path.setText( filedialog )
    #----------------------------------------------------------------------

    def onGenerateQRCode(self):
        qstr_data = self.getVCardData()
        self.showDataToScreen(qstr_data)
    
    #----------------------------------------------------------------------

    def getVCardData(self):
        """ -> str  , the vcard data"""
        # read frame_vcard data 
        qstr_name = self.ui.lineEdit_name.text()
        if len(qstr_name) > 0:
            qstr_name = "N:" + qstr_name + "\n"
        qstr_mobilephone = self.ui.lineEdit_mobilephone.text()
        if len(qstr_mobilephone) > 0:
            qstr_mobilephone = "TEL;HOME:" + qstr_mobilephone + "\n"
        qstr_mobilephone2 = self.ui.lineEdit_mobilephone2.text()
        if len(qstr_mobilephone2) > 0:
            qstr_mobilephone2 = "TEL;HOME:" + qstr_mobilephone2 + "\n"
        qstr_workphone = self.ui.lineEdit_workphone.text()
        if len(qstr_workphone) > 0:
            qstr_workphone = "TEL;WORK:" +  qstr_workphone + "\n"
        qstr_email = self.ui.lineEdit_email.text()     
        if len(qstr_email) > 0:
            qstr_email = "EMAIL:" + qstr_email + "\n"
        qstr_address = self.ui.lineEdit_address.text()
        if len(qstr_address) > 0:
            qstr_address = "ADR:" + qstr_address + "\n"
        qstr_comment = self.ui.textEdit_comment.toPlainText()
        if len(qstr_comment) > 0:
            qstr_comment = "NOTES:" + qstr_comment + "\n"
        qstr_const0 = "BEGIN:VCARD\nVERSION:3.0\n"
        qstr_const1 = "EDN:VCARD\n"
        qstr_data = qstr_const0+qstr_name+qstr_mobilephone+qstr_mobilephone2+qstr_workphone+qstr_email+qstr_address+qstr_comment+qstr_const1
        return qstr_data

    #----------------------------------------------------------------------
     

    def transformDataToPilImage(self,data):
        # initialize qrcode
        # read level 
        levelIndex = self.ui.comboBox_level.currentIndex()
        level = 0
        if levelIndex == 0:
            level = 1
        elif levelIndex == 2:
            level = 3
        elif levelIndex == 3:
            level = 2
        self.m_qr_level = levelIndex
        #read box_size
        size = self.ui.comboBox_size.currentIndex()
        size += 1
        self.m_qr_size = size
        qr = qrcode.QRCode( version=1,  error_correction=level, box_size=1,border=1)
        # generate qrcode image
        qr.add_data(data)
        qr.make(fit=True)
        t_img = qr.make_image()
        return t_img

    #----------------------------------------------------------------------
     
    def addLogoToImage(self):
        # add logo to image 
        rate = 0.22 + 0.06*self.m_qr_level
        qlogo = QtGui.QImage()
        qlogo.load( self.m_logoName )
        qlogo = qlogo.convertToFormat(QtGui.QImage.Format_RGB32)
        code_width = self.m_image.width()
        code_height = self.m_image.height()
        src_logo_width = qlogo.width()
        src_logo_height = qlogo.height()
        dest_logo_width = int(rate * code_width)
        dest_logo_height = int(rate * code_height)
        qlogo = qlogo.scaled(dest_logo_width,dest_logo_height) 
        begin_x = int((code_width-dest_logo_width)/2)
        begin_y = int((code_height-dest_logo_height)/2)
        for i in range(0,dest_logo_width-1):
            for j in range(0,dest_logo_height-1):
                ci = i + begin_x
                cj = j + begin_y
                self.m_image.setPixel(ci,cj,qlogo.pixel(i,j))
        

    #----------------------------------------------------------------------

    def showDataToScreen(self,data):
        """ showDataToScreen """
        t_img = self.transformDataToPilImage(data)
        # condition : PilImage to QImage
        t_img_file = open(defaultTempFileName,"wb")
        t_img.save(t_img_file,'jpeg')
        t_img_file.close()
        # generate m_image 
        label_height = self.ui.label_image.height()
        label_width = self.ui.label_image.width()
        t_image = QtGui.QImage()
        t_image.load(QtCore.QString(defaultTempFileName))
        # condition : get the standard size QImage
        t_image = t_image.scaled(t_image.width()*self.m_qr_size,t_image.height()*self.m_qr_size)
        self.m_image = t_image.convertToFormat(QtGui.QImage.Format_RGB32)
        # add logo to image 
        isLogo = self.ui.checkBox_isLogo.checkState()
        if isLogo == 2:
	        self.addLogoToImage()
        # show image to ui.label_image
        qpixmap = QtGui.QPixmap()
        qpixmap.convertFromImage( self.m_image.scaled(label_width,label_height) )
        self.ui.label_image.setPixmap(qpixmap)    
        # condition : if need to save file , save it
        isSave = self.ui.checkBox_isSave.checkState()
        # bug: if not in same directory , the file can't create!
        if isSave == 2:
            currentFileName = self.ui.lineEdit_path.text()
            self.m_image.save( currentFileName )
        os.remove( defaultTempFileName )
    #----------------------------------------------------------------------
    
    
if __name__ == "__main__": 
    app = QtGui.QApplication(sys.argv) 
    myapp = VCard()
    myapp.setWindowTitle( _fromUtf8("VCard") )
    myapp.show() 
    sys.exit(app.exec_()) 
