# -*- coding: utf-8 -*-

"""
xujing
2020-06-17
mainwindow
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from Ui_my_main_ui import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtWidgets import  *
from PyQt5 import *
from PyQt5.QtGui import *
import sys
import time

import cv2
import numpy as np
from PIL import Image
from mtcnn import MTCNN
from numba import jit, prange

# import qdarkstyle
# dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()


# 仿射变换，用于将贴图点映射到人脸点,得到变换矩阵M
def get_text_trans_matrix(x1, y1, x2, y2, x3, y3, tx1, ty1, tx2, ty2, tx3, ty3):
    '''
    src：原始图像中的三个点的坐标
    dst：变换后的这三个点对应的坐标
    M：根据三个对应点求出的仿射变换矩阵2X3
    '''
    # 放射变换
    return cv2.getAffineTransform( np.float32([ [tx1, ty1], [tx2, ty2], [tx3, ty3] ]), np.float32( [ [x1, y1], [x2, y2], [x3, y3] ]) ).flatten() # 按行拉直
    # 透视变换
    # return cv2.getPerspectiveTransform( np.float32([ [tx1, ty1], [tx2, ty2], [tx3, ty3] ]), np.float32( [ [x1, y1], [x2, y2], [x3, y3] ]) ).flatten()

@jit(nopython=True)
def sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, H):
    def CLIP3(x, a, b):
        return min(max(a,x), b)
    # 用于将贴图点映射到人脸点 
    for i in range(height):
    # for i in prange(height):
        for j in range(width):
            x = float(i)
            y = float(j)
            tx = (int)((H[0] * (x)+H[1] * (y)+H[2]) + 0.5)
            ty = (int)((H[3] * (x)+H[4] * (y)+H[5]) + 0.5)
            tx = CLIP3(tx, 0, maskHeight - 1)
            ty = CLIP3(ty, 0, maskWidth - 1)

            mr = int( mask[ int(tx), int(ty), 0 ] ) 
            mg = int( mask[ int(tx), int(ty), 1 ] ) 
            mb = int( mask[ int(tx), int(ty), 2 ] ) 
            alpha = int( mask[ int(tx), int(ty), 3 ] )  
            #if alpha!=0:
            #    print( '>>>', alpha )
            b = srcData[i, j, 0]
            g = srcData[i, j, 1]
            r = srcData[i, j, 2]        
            srcData[i, j, 0] =CLIP3((b * (255 - alpha) + mb * alpha) / 255, 0, 255)
            srcData[i, j, 1] =CLIP3((g * (255 - alpha) + mg * alpha) / 255, 0, 255)
            srcData[i, j, 2] =CLIP3((r * (255 - alpha) + mr * alpha) / 255, 0, 255)
    return srcData


# @jit(parallel=True,nogil=True)
# @njit(parallel=True,nogil=True)
def trent_sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, ratio):
    ret = 0
    H = get_text_trans_matrix( maskFacePoints[0], maskFacePoints[1],maskFacePoints[2],maskFacePoints[3],maskFacePoints[4],maskFacePoints[5], srcFacePoints[0], srcFacePoints[1],srcFacePoints[2],srcFacePoints[3],srcFacePoints[4],srcFacePoints[5] )
    #print ('H', H) 
    srcData = sticker(srcData, width, height, stride, mask, maskWidth, maskHeight, maskStride, srcFacePoints, maskFacePoints, H)
    return srcData, ret 

# 京剧脸谱配置
face_key_point = {
    "01": [ 958.0,599.0, 958.0,1083.0, 1516.0,838.0 ],
    "02": [ 182.0,155.0, 182.0,243.0, 290.0,199.0 ],
    "03": [ 249.0,224.0, 247.0,342.0, 392.0,247.0 ],
    "04": [ 232.0,136.0, 232.0,267.0, 378.0,200.0 ],
    "05": [ 241.0,189.0, 241.0,323.0, 405.0,253.0 ],
    "06": [ 237.0,159.0, 237.0,284.0, 381.0,213.0 ],
    "07": [ 256.0,219.0, 256.0,342.0, 405.0,281.0 ],
    "08": [ 217.0,185.0, 217.0,298.0, 356.0,243.0 ],
    "09": [ 391.0,223.0, 391.0,428.0, 652.0,324.0 ],
    "10": [ 197.0,203.0, 197.0,313.0, 329.0,249.0 ],
    "11": [ 153.0,98.0, 153.0,164.0, 232.0,129.0 ],
    "12": [ 248.0,216.0, 248.0,345.0, 402.0,280.0 ],
    "13": [ 264.0,177.0, 264.0,325.0, 459.0,252.0 ],
    "14": [ 290.0,171.0, 290.0,333.0, 478.0,250.0 ],
    "15": [ 154.0,105.0, 154.0,196.0, 271.0,149.0]
    }


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.left_button = 0
        self.right_button = 4
        QToolTip.setFont(QFont('SansSerif', 40))

        self.my_face_choose = "01"
        self.label.mylabelSig.connect(self.label_choose)
        self.label_2.mylabelSig.connect(self.label_2_choose)
        self.label_3.mylabelSig.connect(self.label_3_choose)
        self.label_4.mylabelSig.connect(self.label_4_choose)



    def label_choose(self):
        # self.label.setStyleSheet("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)#设置字体颜色
        self.label.setPalette(pe)

        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Roman times",20,QFont.Bold))

        try:
            self.label.setText("<b>选择: %02d</b>"%self.face_1[0])
            self.my_face_choose = "%02d"%self.face_1[0]
        except:
            self.label.setText("<b>选择: 01</b>")

    def label_2_choose(self):
        # self.label.setStyleSheet("")
        self.label.setText("")
        self.label_3.setText("")
        self.label_4.setText("")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)#设置字体颜色
        self.label_2.setPalette(pe)

        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setFont(QFont("Roman times",20,QFont.Bold))

        try:
            self.label_2.setText("<b>选择: %02d</b>"%self.face_2[0])
            self.my_face_choose = "%02d"%self.face_2[0]
        except:
            self.label_2.setText("<b>选择: 02</b>")
            self.my_face_choose = "02"

    def label_3_choose(self):
        # self.label.setStyleSheet("")
        self.label_2.setText("")
        self.label.setText("")
        self.label_4.setText("")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)#设置字体颜色
        self.label_3.setPalette(pe)

        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setFont(QFont("Roman times",20,QFont.Bold))

        try:
            self.label_3.setText("<b>选择: %02d</b>"%self.face_3[0])
            self.my_face_choose = "%02d"%self.face_3[0]
        except:
            self.label_3.setText("<b>选择: 03</b>")
            self.my_face_choose = "03"

    def label_4_choose(self):
        # self.label.setStyleSheet("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label.setText("")

        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.green)#设置字体颜色
        self.label_4.setPalette(pe)

        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setFont(QFont("Roman times",20,QFont.Bold))

        try:
            self.label_4.setText("<b>选择: %02d</b>"%self.face_4[0])
            self.my_face_choose = "%02d"%self.face_4[0]
        except:
            self.label_4.setText("<b>选择: 04</b>")
            self.my_face_choose = "04"



    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        左翻页
        """

        if self.right_button == 4:
            self.left_button += 1

            self.face_1 = [self.left_button+1 if self.left_button <= 11 else 12]
            self.face_2 = [self.left_button+2 if self.left_button <= 12 else 13]
            self.face_3 = [self.left_button+3 if self.left_button <= 13 else 14]
            self.face_4 = [self.left_button+4 if self.left_button <= 14 else 15]
        else:
            self.face_1 = [self.face_1[0]+1]
            self.face_2 = [self.face_2[0]+1]
            self.face_3 = [self.face_3[0]+1]
            self.face_4 = [self.face_4[0]+1]


        self.label.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_1[0])
        self.label_2.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_2[0])
        self.label_3.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_3[0])
        self.label_4.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_4[0])

        self.label.setToolTip("<b>%02d</b>"%self.face_1[0])
        self.label_2.setToolTip("<b>%02d</b>"%self.face_2[0])
        self.label_3.setToolTip("<b>%02d</b>"%self.face_3[0])
        self.label_4.setToolTip("<b>%02d</b>"%self.face_4[0])

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        "右翻页"
        """

        if self.left_button == 0:
            self.right_button += 1
   
            self.face_1 = [self.right_button-4 if self.right_button > 4 else 1]
            self.face_2 = [self.right_button-3 if self.right_button > 3 else 2]
            self.face_3 = [self.right_button-2 if self.right_button > 2 else 3]
            self.face_4 = [self.right_button-1 if self.right_button > 1 else 4]
        else:
            self.face_1 = [self.face_1[0]-1]
            self.face_2 = [self.face_2[0]-1]
            self.face_3 = [self.face_3[0]-1]
            self.face_4 = [self.face_4[0]-1]


        self.label.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_1[0])
        self.label_2.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_2[0])
        self.label_3.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_3[0])
        self.label_4.setStyleSheet("border-image: url(:/my_pic/pic/mask/%02d.png);"%self.face_4[0])

        self.label.setToolTip("<b>%02d</b>"%self.face_1[0])
        self.label_2.setToolTip("<b>%02d</b>"%self.face_2[0])
        self.label_3.setToolTip("<b>%02d</b>"%self.face_3[0])
        self.label_4.setToolTip("<b>%02d</b>"%self.face_4[0])


    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        AI人脸识别 + 仿射变换
        """
        jingju = self.my_face_choose
        self.my_face_choose = "01"
        self.label.setText("")
        self.label_2.setText("")
        self.label_3.setText("")
        self.label_4.setText("")
        print(jingju)

        img = Image.open("./static/{}.png".format(jingju)) 

        r,g,b,a=img.split()   #分离4通道 
        im_array = np.array(img) 
        # 高宽通道 (坐标取值为y, x) 
        mask_h, mask_w, mask_c = im_array.shape 

        try:
            # img = cv2.imread( './test_img/001.jpg' )
            openfile_name = QFileDialog.getOpenFileName(self,'AI京剧换脸','','JPEG Files(*.jpg);;PNG Files(*.png);;PGM Files(*.pgm)')
          
            img = cv2.imread( openfile_name[0] )
            # 高宽通道 (坐标取值为y, x)
            h, w, c = img.shape
            bbox, scores, landmarks = mtcnn.detect(img)
          
            for box, pts in zip(bbox, landmarks):
                faceInfos = np.array( [ 1, box[1], box[0], box[3] - box[1], box[2] - box[0], pts[5], pts[0], pts[6], pts[1], pts[7], pts[2], pts[8], pts[3], pts[9], pts[4] ] )


            srcFacePoints = np.array( [faceInfos[6], faceInfos[5], faceInfos[8], faceInfos[7], (faceInfos[12]+faceInfos[14])/2.0, (faceInfos[11] + faceInfos[13])/2.0 ] ) 
            print ('srcFacePoints:', srcFacePoints) 

           
            maskFacePoints = np.array(face_key_point[jingju]) 
            print ('maskFacePoints:', maskFacePoints)

            # start_time = time.time()
            srcData, ret  = trent_sticker( img, w, h, 3, im_array, mask_w, mask_h, 4, srcFacePoints, maskFacePoints, 100 ) 
            # print ( 'time >>>>', time.time() - start_time )
            img_mask = np.array(srcData, dtype=np.uint8) 
            # cv2.imwrite('res.jpg', img_mask)

            bytesPerLine = c * w

            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            QImg = QImage(img.data, w, h,bytesPerLine, QImage.Format_RGB888)
            self.label_6.setAlignment(Qt.AlignCenter)
            self.label_6.setPixmap(QPixmap.fromImage(QImg).scaled(self.label_6.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

            self.save_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(e)



    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        TODO: 视频流
        """

        QMessageBox.information(self,
                                    "AI京剧换脸 消息",  
                                    "目前不提供视频应用！",  
                                    QMessageBox.Yes | QMessageBox.No)
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        下载图像
        """

        try:
            filename=QFileDialog.getSaveFileName(self,'AI京剧换脸 保存','','JPEG Files(*.jpg);;PNG Files(*.png);;PGM Files(*.pgm)')
            cv2.imwrite(filename[0],self.save_img)
        except:
            QMessageBox.warning(self,
                                    "AI京剧换脸 警告",  
                                    "没有需要下载保存的图片！",  
                                    QMessageBox.Yes | QMessageBox.No)



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(dark_stylesheet)
    
    splash = QSplashScreen(QtGui.QPixmap(':/my_pic/pic/face.png'))
    # splash = MySplashScreen('./pic/face.gif', Qt.WindowStaysOnTopHint)
    splash.show()
    splash.showMessage('渲染界面...')
    # QThread.sleep(0.5)
    time.sleep(0.5)
    splash.showMessage('正在初始化程序...')
    mtcnn = MTCNN('./pb/mtcnn.pb')   # 实例化MTCNN
    app. processEvents()
    ui =MainWindow()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())
    
