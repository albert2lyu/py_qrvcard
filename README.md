# py_qrvcard

一个采用 PyQt4 和 qrcode 两个库 完成的 python 二维码名片生成小程序。

二维码名片采用 VCARD格式，下面给出一个 VCARD格式例子，

## VCARD格式示例
<b>
BEGIN:VCARD<br/>
VERSION:3.0<br/>
N:王辉 <br/>
ORG:whut <br/>
EMAIL;HOME:446591615@qq.com <br/>
EMAIL;WORK:wanda1416@163.com <br/>
TEL;WORK:18200000000 <br/>
TEL;HOME:0731-24000000 <br/>
ADR:Hx-xxx <br/>
EDN:VCARD <br/>
</b>

##文件结构
所有的程序文件包含在文件夹 VARD。

test 文件夹，包含了两个测试的demo。

card.pyw python入口程序

card.ui 程序的界面设计文件

card_ui.[py/pyc] 由 card.ui 自动生成的python程序

update_ui.bat 用于重新将 card.ui 编译为 card.py 的批处理命令

logo.png 默认的二维码名片中间logo图标




##一些用法

QLabel:显示图片 card_0.jpg 到self.ui.image 

		reader = QtGui.QImageReader( QtCore.QString("card_0.jpg") )
		qimg = reader.read()
		pixmap = QtGui.QPixmap.fromImage(qimg)
		self.ui.image.setPixmap(pixmap)
	从文件中读取图片，并绘制在QLabel中
	

生成二维码并输出为文件：

		qr = qrcode.QRCode(
			version=1,
				   error_correction=qrcode.constants.ERROR_CORRECT_L,
			box_size=10,
			border=4,
		)
		qr.add_data('http://www.baidu.com/')
		qr.make(fit=True)
		img = qr.make_image()
		img_file = open("card1.jpg","wb")
		img.save(img_file,'jpeg')
		img_file.close()

connect用法：

		QtCore.QObject.connect(self.ui.pushButton_make,QtCore.SIGNAL("clicked()"),self.onGenerateQRCode)

读取lineedit数据

		qstr_name = self.ui.lineEdit_name.text()
	qstr_name 为 QtCore.QString 类型，与str 性质差不多


# debug: set param
        self.ui.lineEdit_name.setText( _fromUtf8("王辉") )
        self.ui.lineEdit_mobilephone.setText( _fromUtf8("18200000000") )
        self.ui.lineEdit_email.setText( _fromUtf8("wanda1416@163.com") )
        self.ui.lineEdit_address.setText( _fromUtf8("武汉理工大学") )