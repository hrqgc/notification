import webbrowser

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import sys
import sqlite3
import os

from google.cloud import pubsub_v1

from banco import cursor, conexao
import time
import re
import simplegmail

import threading
from simplegmail import Gmail
from simplegmail.query import construct_query
import urllib.request


class ItemDelegate(QStyledItemDelegate):
    def paint(self,painter,option,index):

        painter.save()
        is_pressed = index.data(Qt.UserRole +5) or False

        option.state &= ~QStyle.State_Selected
        option.state &= ~QStyle.State_HasFocus

        if is_pressed:
            bg = QPixmap('assets/images/itemBackgroundPressed.png')
            option.rect.translate(1,1)
        else:
            bg = QPixmap('assets/images/itemBackground.png')

        painter.drawPixmap(option.rect,bg)
        painter.restore()

        super().paint(painter,option,index)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mail Notification")
        self.setFixedWidth(200)
        self.setObjectName("MainWindow")
        self.setStyleSheet("QWidget#MainWindow { background: transparent; }")
        self.setFocusPolicy(Qt.StrongFocus)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/images/btnTrash.png"))

        tray_menu = QMenu()
        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.restartApp)
        tray_menu.addAction(reload_action)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(quit_action)



        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.menuScreen= QMenu("Switch Monitor", self)
        tray_menu.addMenu(self.menuScreen)
        for i,screen in enumerate(QApplication.screens()):
            action = QAction(f'Screen {i+1}', self)
            action.triggered.connect(lambda checked, idx=i: self.changeMonitor(idx))
            self.menuScreen.addAction(action)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.UiComponents()
        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_x = screen_geometry.width() -self.width()
        pos_y = screen_geometry.height()-self.height()

        self.move(pos_x, pos_y)


        self.show()
        # self.setupUi(self)

    def changeMonitor(self, index):
        telas = QApplication.screens()
        if index< len(telas):
            chooseScreen = telas[index]
            screen_geometry = chooseScreen.geometry()
            pos_x = screen_geometry.x() + screen_geometry.width() - self.width()
            pos_y = screen_geometry.y() + screen_geometry.height() - self.height()

            self.move(pos_x, pos_y)

    def UiComponents(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        caminho_fonte = os.path.abspath('assets/fonts/Pix32.ttf')
        id_fonte = QFontDatabase.addApplicationFont(caminho_fonte)
        if id_fonte != -1:
            nome_fonte = QFontDatabase.applicationFontFamilies(id_fonte)[0]
        else:
            nome_fonte = 'Arial'
        appFont = QFont(nome_fonte,11)



        cursor.execute('''SELECT * FROM requests ORDER BY id DESC''')
        historico_request = cursor.fetchall()

        cursor.execute('''SELECT * FROM finals ORDER BY id DESC''')
        historico_finals = cursor.fetchall()


        imgNotification = QPixmap('assets/images/5789RED.bmp')
        corfundo2 = imgNotification.toImage().pixelColor(0, 0)
        molde2 = imgNotification.createMaskFromColor(corfundo2)
        imgNotification.setMask(molde2)
        imgNotification = imgNotification.scaled(25, 25, Qt.KeepAspectRatio)


        self.timerBlink = QTimer(self)
        self.timerBlink.setInterval(500)
        self.timerBlink.timeout.connect(self.animateBlink)
        self.timerBlink.start()




        self.clickSound = QSoundEffect()
        caminho_som = os.path.abspath('assets/sounds/mouseClick.wav')
        self.clickSound.setSource(QUrl.fromLocalFile(caminho_som))

        self.notificationSound = QSoundEffect()
        pathNo = os.path.abspath('assets/sounds/notificationSound.wav')
        self.notificationSound.setSource(QUrl.fromLocalFile(pathNo))

        self.requestOpen = False
        self.finalsOpen = False
        self.deleteOpen = False


        self.internetStatus = True
        self.connectionStatus = False


        self.containerBtn = QWidget()
        self.containerBtn.setFixedSize(120,70)
        # transparent background
        # container.setStyleSheet("background: transparent;")
        self.containerBtn.setStyleSheet("QWidget {background: transparent;}")

        self.pixRe = QPixmap('assets/images/btnRequest.png').scaled(50,50,Qt.KeepAspectRatio)
        self.pixReOff = QPixmap('assets/images/btnRequestOff.png').scaled(50,50,Qt.KeepAspectRatio)
        self.pixFi = QPixmap('assets/images/btnFinal.png').scaled(50,50,Qt.KeepAspectRatio)
        self.pixFiOff = QPixmap('assets/images/btnFinalOff.png').scaled(50, 50, Qt.KeepAspectRatio)
        self.pixPressed = QPixmap('assets/images/btnPressed.png').scaled(50, 50, Qt.KeepAspectRatio)
        self.pixPressedOff = QPixmap('assets/images/btnPressedOff.png').scaled(50, 50, Qt.KeepAspectRatio)


        self.button_request = QPushButton(self.containerBtn)
        self.button_request.setStyleSheet("background: transparent;border: none;")
        self.button_request.setIcon(QIcon(self.pixRe))
        self.button_request.setIconSize(QSize(50,50))
        self.button_request.setFocusPolicy(Qt.NoFocus)
        self.button_request.setGeometry(1, 1, 50, 50)



        self.button_request.clicked.connect(self.clickRequest)

        self.button_final = QPushButton(self.containerBtn)
        self.button_final.setStyleSheet("background: transparent; border: none;")
        self.button_final.setIcon(QIcon(self.pixFi))
        self.button_final.setIconSize(QSize(50, 50))
        self.button_final.setFocusPolicy(Qt.NoFocus)

        self.button_final.setGeometry(70, 1, 50, 50)



        self.button_request.pressed.connect(lambda: self.button_request.setIcon(QIcon(self.pixPressed if (self.internetStatus and self.connectionStatus) else self.pixPressedOff)))
        self.button_request.pressed.connect(lambda: self.button_request.move(2, 2))
        self.button_request.released.connect(lambda: self.button_request.setIcon(QIcon(self.pixRe if (self.internetStatus and self.connectionStatus) else self.pixReOff)))
        self.button_request.released.connect(lambda: self.button_request.move(1, 1))

        self.button_final.pressed.connect(lambda: self.button_final.setIcon(QIcon(self.pixPressed if (self.internetStatus and self.connectionStatus) else self.pixPressedOff)))
        self.button_final.pressed.connect(lambda: self.button_final.move(71, 2))
        self.button_final.released.connect(lambda: self.button_final.setIcon(QIcon(self.pixFi if (self.internetStatus and self.connectionStatus) else self.pixFiOff)))
        self.button_final.released.connect(lambda: self.button_final.move(70, 1))



        self.button_final.clicked.connect(self.clickFinals)

        self.notificationRequest = QLabel(self.button_request)
        self.notificationRequest.setGeometry(24, 0, 25, 25)
        # self.notificationRequest.setStyleSheet("background-color: red; border-radius: 8px;")
        self.notificationRequest.setStyleSheet("background-color: transparent; border-radius: 0px;padding: 0px;")
        self.notificationRequest.setPixmap(imgNotification)
        #
        self.notificationFinal = QLabel(self.button_final)
        self.notificationFinal.setGeometry(24, 0, 25, 25)
        self.notificationFinal.setStyleSheet("background-color: transparent; border-radius: 0px;padding: 0px;")
        self.notificationFinal.setPixmap(imgNotification)



        self.blinkRequest = False
        self.blinkFinal = False
        self.blinkMinimized = False
        self.notificationFinal.hide()
        self.notificationRequest.hide()

        #

        self.containerListRequest = QWidget()
        self.containerListRequest.setObjectName("Fundo")
        self.containerListRequest.setStyleSheet("QWidget#Fundo {border-image: url('assets/images/mainBg.png')}")
        # imagemBackground = QLabel(self.containerListRequest)
        # imagemBackground.setPixmap(imgNotification)
        # imagemBackground.setGeometry(0, 0, 200, 200)





        layout2 = QVBoxLayout(self.containerListRequest)
        layout2.setContentsMargins(5, 5, 5, 5)


        self.containerListFinal = QWidget()
        self.containerListFinal.setObjectName("Fundo")
        self.containerListFinal.setStyleSheet("QWidget#Fundo {border-image: url('assets/images/mainBg.png')}")
        layout3 = QVBoxLayout(self.containerListFinal)
        layout3.setContentsMargins(5, 5, 5, 5)


        self.label_lista_request = QListWidget(self)
        self.label_lista_request.setItemDelegate(ItemDelegate(self))
        self.label_lista_request.viewport().installEventFilter(self)
        self.label_lista_request.setFocusPolicy(Qt.NoFocus)

        textRequest = QLabel('Requests',self.label_lista_request)
        textRequest.setStyleSheet("color: white;padding-left: 2px;")
        textRequest.setFont(appFont)
        textRequest.move(0, -2)
        self.textNoWorkRe = QLabel("U've got no work homie :)",self.label_lista_request)
        self.textNoWorkRe.setStyleSheet("color: black; ")
        self.textNoWorkRe.setWordWrap(True)
        self.textNoWorkRe.setFont(appFont)
        self.textNoWorkRe.setAlignment(Qt.AlignCenter)
        self.textNoWorkRe.resize(180, 150)
        self.textNoWorkRe.hide()
        for linha in historico_request:
            item = QListWidgetItem(linha[1])
            item.setData(Qt.UserRole, linha[2])
            self.label_lista_request.addItem(item)
        if len(historico_request) == 0:
            self.textNoWorkRe.show()
        self.label_lista_request.setStyleSheet("""
        QListWidget {
                background: transparent;
                border: none;
                margin-top: 25px;
            }
            QListWidget::item {
                background: transparent;
                padding: 5px;
                margin-bottom: 5px;
            }
        """)


        # label_lista_request.itemClicked.connect(self.itemClickd)
        self.label_lista_request.setWordWrap(True)
        layout2.addWidget(self.label_lista_request)

        # qtd_request = self.label_lista_request.count()
        # if qtd_request > 0:
        #     altura_req = self.label_lista_request.sizeHintForRow(0) * qtd_request + 5
        #     self.label_lista_request.setFixedHeight(altura_req)
        self.label_lista_request.setFixedHeight(170)
        self.label_lista_request.setFixedWidth(180)



        self.label_lista_finals = QListWidget(self)
        self.label_lista_finals.setItemDelegate(ItemDelegate(self))
        self.label_lista_finals.viewport().installEventFilter(self)
        self.label_lista_finals.setFocusPolicy(Qt.NoFocus)
        textFinals = QLabel('Finals', self.label_lista_finals)
        textFinals.setStyleSheet("color: white;padding-left: 2px;")
        textFinals.setFont(appFont)
        textFinals.move(0, -2)
        self.textNoWorkFi = QLabel("U've got no work homie :D", self.label_lista_finals)
        self.textNoWorkFi.setStyleSheet("color: black;")
        self.textNoWorkFi.setWordWrap(True)
        self.textNoWorkFi.setFont(appFont)
        self.textNoWorkFi.setAlignment(Qt.AlignCenter)
        self.textNoWorkFi.resize(180, 150)
        self.textNoWorkFi.hide()
        for linha in historico_finals:
            item = QListWidgetItem(linha[1])
            item.setData(Qt.UserRole, linha[2])
            self.label_lista_finals.addItem(item)
        if len(historico_finals) == 0:
            self.textNoWorkFi.show()
        self.label_lista_finals.setStyleSheet("""
                QListWidget {
                background: transparent;
                border: none;
                margin-top: 25px;
            }
            QListWidget::item {
                background: transparent;
                padding: 5px;
                margin-bottom: 5px;
            
                }""")

        # label_lista_finals.itemClicked.connect(self.itemClickd)
        self.label_lista_finals.setWordWrap(True)
        layout3.addWidget(self.label_lista_finals)

        # qtd_final = self.label_lista_finals.count()
        # if qtd_final > 0:
        #     altura_req = self.label_lista_finals.sizeHintForRow(0) * qtd_final + 5
        #     self.label_lista_finals.setFixedHeight(altura_req)
        self.label_lista_finals.setFixedHeight(170)
        self.label_lista_finals.setFixedWidth(180)

        self.label_lista_request.verticalScrollBar().setStyle(QStyleFactory.create('Windows'))
        self.label_lista_finals.verticalScrollBar().setStyle(QStyleFactory.create('Windows'))

        closeImg = QIcon(QPixmap('assets/images/btnClose.png'))
        btnCloseRe = QPushButton(self.containerListRequest)
        btnCloseRe.setStyleSheet("background: transparent; border: none; padding: 0px;")
        btnCloseRe.setIcon(closeImg)
        btnCloseRe.setGeometry(168, 4, 20, 20)
        btnCloseRe.clicked.connect(self.fechar)

        trashImg = QIcon(QPixmap('assets/images/btnTrash.png'))
        btnTrashRe = QPushButton(self.containerListRequest)
        btnTrashRe.setStyleSheet("""
            QPushButton {
                background: transparent; 
                border: none; 
                padding: 0px;
            }
            QPushButton:pressed {
                padding-top: 2px;
                padding-left: 2px;
            }
        """)
        btnTrashRe.setFocusPolicy(Qt.NoFocus)
        btnTrashRe.setIcon(trashImg)
        btnTrashRe.setGeometry(145, 4, 20, 20)
        btnTrashRe.clicked.connect(self.vanish)

        btnCloseFi = QPushButton(self.containerListFinal)
        btnCloseFi.setStyleSheet("background: transparent; border: none; padding: 0px;")
        btnCloseFi.setIcon(closeImg)
        btnCloseFi.setGeometry(168, 4, 20, 20)
        btnCloseFi.clicked.connect(self.fechar)

        btnTrashFi = QPushButton(self.containerListFinal)
        btnTrashFi.setStyleSheet("""
            QPushButton {
                background: transparent; 
                border: none; 
                padding: 0px;
            }
            QPushButton:pressed {
                padding-top: 2px;
                padding-left: 2px;
            }
        """)
        btnTrashFi.setFocusPolicy(Qt.NoFocus)
        btnTrashFi.setIcon(trashImg)
        btnTrashFi.setGeometry(145, 4, 20, 20)
        btnTrashFi.clicked.connect(self.vanish)


        self.containerDelete = QWidget()
        self.containerDelete.setObjectName("Fundo")
        self.containerDelete.setStyleSheet("QWidget#Fundo {border-image: url('assets/images/deleteBackground.png')}")

        self.containerDelete.setFixedSize(180,120)
        self.containerDelete.setContentsMargins(2, 2, 2, 2)
        textDelete = QLabel('Delete', self.containerDelete)
        textDelete.setStyleSheet("color: white;padding-left: 5px;")
        textDelete.setFont(appFont)
        self.labele =QLabel('',self.containerDelete)
        self.labele.setStyleSheet("QWidget{background: transparent;}")
        self.labele.setWordWrap(True)
        self.labele.setAlignment(Qt.AlignCenter)
        btnYesDelete = QPushButton('YES',self.containerDelete)
        btnNoDelete = QPushButton('NO',self.containerDelete)
        layout4 = QVBoxLayout(self.containerDelete)
        layout4.addWidget(self.labele)
        btnYesDelete.setFocusPolicy(Qt.NoFocus)
        btnNoDelete.setFocusPolicy(Qt.NoFocus)
        btnYesDelete.clicked.connect(self.confirmDelete)
        btnNoDelete.clicked.connect(self.cancelDelete)
        btnYesDelete.setStyleSheet("""
        QPushButton {
                border-image: url('assets/images/yesono.png');
            }
            QPushButton:pressed {
                border-image: url('assets/images/yesonoPressed.png');                
            }
        """)



        btnNoDelete.setStyleSheet("""
        QPushButton {
                border-image: url('assets/images/yesono.png');
            }
            QPushButton:pressed {
                border-image: url('assets/images/yesonoPressed.png');                
            }
        """)
        btnYesDelete.setGeometry(20,80,65,30)
        btnNoDelete.setGeometry(95,80,65,30)
        btnYesDelete.setFont(appFont)
        btnNoDelete.setFont(appFont)

        self.vanishRn = False

        self.labele.setFont(appFont)
        self.label_lista_finals.setFont(appFont)
        self.label_lista_request.setFont(appFont)





        main_layout.addWidget(self.containerDelete, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.containerListRequest, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.containerListFinal, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.containerBtn, alignment=Qt.AlignHCenter)

        self.containerListRequest.hide()
        self.containerListFinal.hide()
        self.containerDelete.hide()


        self.miniminizeBtn = QPushButton(self)
        self.miniminizeBtn.setStyleSheet("background: rgba(255, 255, 255, 0.01); border: none;")

        self.miniminizeBtn.setGeometry(192, 0, 8, 35)
        y_inicial = self.height() - 50
        self.miniminizeBtn.move(192, y_inicial)
        self.miniminizeBtn.clicked.connect(self.miniminizeScreen)
        self.miniminized = False
        self.miniminizeBtn.installEventFilter(self)

        self.notificationMinimized = QLabel(self)
        self.notificationMinimized.setGeometry(177, 0, 16, 16)
        self.notificationMinimized.setScaledContents(True)
        self.notificationMinimized.setStyleSheet("background-color: transparent; border-radius: 0px;padding: 0px;")
        self.notificationMinimized.setPixmap(imgNotification)

        self.notificationMinimized.hide()





        self.thread_pubsub = pubsubListener()
        self.thread_pubsub.newRequest.connect(self.AddItemListRequest,Qt.QueuedConnection)
        self.thread_pubsub.newFinal.connect(self.AddItemListFinals,Qt.QueuedConnection)

        self.thread_pubsub.statusChanged.connect(self.updateConnection, Qt.QueuedConnection)

        self.thread_pubsub.authError.connect(lambda: webbrowser.open('https://console.cloud.google.com/apis/credentials'), Qt.QueuedConnection)

        self.thread_pubsub.start()


        self.internetTimer = QTimer(self)
        self.internetTimer.setInterval(5000)
        self.internetTimer.timeout.connect(self.checkInternet)
        self.internetTimer.start()

        threading.Thread(target=self.thread_pubsub.Serach).start()


    def clickRequest(self):
        # self.clickSound.play()
        if self.requestOpen == False:
            if self.finalsOpen:
                self.containerListFinal.hide()
                self.finalsOpen = False
            self.containerListRequest.show()
            self.requestOpen = True

            self.blinkRequest = False
            self.notificationRequest.hide()
            self.containerDelete.hide()
            self.deleteOpen = False

            self.adjustSize()

            screen_geometry = QApplication.desktop().availableGeometry(self)
            pos_y = screen_geometry.height()-self.height()
            self.move(self.x(), pos_y)
            # print("clickmere")
        elif self.requestOpen == True:
            self.requestOpen = False
            self.containerListRequest.hide()
            self.containerDelete.hide()
            self.deleteOpen = False

    def clickFinals(self):
        if self.finalsOpen == False:
            if self.requestOpen:
                self.containerListRequest.hide()
                self.requestOpen = False
            self.containerListFinal.show()
            self.finalsOpen = True

            self.blinkFinal = False
            self.notificationFinal.hide()
            self.containerDelete.hide()
            self.deleteOpen = False

            self.adjustSize()

            screen_geometry = QApplication.desktop().availableGeometry(self)
            pos_y = screen_geometry.height() - self.height()
            self.move(self.x(), pos_y)
            # print("clickmefi")
        elif self.finalsOpen == True:
            self.finalsOpen = False
            self.containerListFinal.hide()

    def eventFilter(self,source,event):

        if getattr(self, 'miniminizeBtn', None) == source:
            preciseY = self.height() - 60
            if event.type() == QEvent.Enter:
                # print('mouse is over')
                self.miniminizeBtn.setGeometry(180, preciseY, 20, 35)
                self.miniminizeBtn.setStyleSheet("background: white;")
                self.notificationMinimized.setGeometry(172, preciseY-10, 16, 16)
                return False
            elif event.type() == QEvent.Leave:
                # print('mouse is not over anynmore')
                self.miniminizeBtn.setGeometry(192, preciseY, 8, 35)
                if self.miniminized == True:
                    self.miniminizeBtn.setStyleSheet("background: white; border: none;")
                    self.notificationMinimized.setGeometry(180, preciseY-10, 16, 16)
                else:
                    self.miniminizeBtn.setStyleSheet("background: rgba(255, 255, 255, 0.01); border: none;")
                return False
        if isinstance(source, QWidget) and isinstance(source.parent(), QListWidget):

            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                if getattr(self,'deleteOpen',False):
                    self.cancelDelete()
                    return True
                item_clicked = source.parent().itemAt(event.pos())
                if item_clicked:
                    self.item_atual = item_clicked


                    self.item_atual.setData(Qt.UserRole +5, True)
                    source.parent().viewport().update()

                return False

            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
                if hasattr(self, 'item_atual') and self.item_atual is not None:

                    print(f'click quiky itme {self.item_atual.text()} e no link {self.item_atual.data(Qt.UserRole)}')
                    url = self.item_atual.data(Qt.UserRole)
                    webbrowser.open(url)
                    self.item_atual.setData(Qt.UserRole + 5,False)
                    source.parent().viewport().update()

                    self.item_atual = None
                return False
            elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.RightButton:

                item_clicked = source.parent().itemAt(event.pos())

                if item_clicked:

                    self.item_atual = item_clicked
                    self.item_atual.setData(Qt.UserRole + 5, True)
                    source.parent().viewport().update()

                    self.deleteItem(self.item_atual)

                return True
            elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.RightButton:
                self.item_atual.setData(Qt.UserRole + 5, False)
                source.parent().viewport().update()

                self.item_atual = None



        return super().eventFilter(source, event)
        # QDesktopServices.openUrl(QUrl(item.data(Qt.UserRole)))


    def deleteItem(self,item):
        self.waitingItem = item
        # print('deleting item')
        self.labele.setText(f'Delete {item.text()}?')
        self.containerDelete.show()
        self.deleteOpen = True

        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)

    def confirmDelete(self):

        if self.vanishRn:
            if self.requestOpen:
                cursor.execute('''DELETE FROM requests''')
                conexao.commit()
                self.label_lista_request.clear()
                self.textNoWorkRe.show()
            elif self.finalsOpen:
                cursor.execute('''DELETE FROM finals''')
                conexao.commit()
                self.label_lista_finals.clear()
                self.textNoWorkFi.show()
        elif self.requestOpen:
            cursor.execute('''DELETE FROM requests WHERE name = ?''',(self.waitingItem.text(),))
            conexao.commit()
            line = self.label_lista_request.row(self.waitingItem)
            self.label_lista_request.takeItem(line)

            if self.label_lista_request.count() == 0:
                self.textNoWorkRe.show()
            # qtd_request = self.label_lista_request.count()
            # if qtd_request > 0:
            #     altura_req = self.label_lista_request.sizeHintForRow(0) * qtd_request + 5
            #     self.label_lista_request.setFixedHeight(altura_req)

        elif self.finalsOpen:
            cursor.execute('''DELETE FROM finals WHERE name = ?''', (self.waitingItem.text(),))
            conexao.commit()
            line = self.label_lista_finals.row(self.waitingItem)
            self.label_lista_finals.takeItem(line)

            if self.label_lista_finals.count() == 0:
                self.textNoWorkFi.show()
            # qtd_final = self.label_lista_finals.count()
            # if qtd_final > 0:
            #     altura_fin = self.label_lista_finals.sizeHintForRow(0) * qtd_final + 5
            #     self.label_lista_finals.setFixedHeight(altura_fin)



        self.containerDelete.hide()
        self.deleteOpen = False

        QApplication.processEvents()
        self.adjustSize()


        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)

        self.waitingItem = None

    def cancelDelete(self):

        # print('cancelling deletion')
        self.containerDelete.hide()
        self.deleteOpen = False
        self.vanishRn = False

        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)


    def focusOutEvent(self, event):
        # print("focusOutEvent")
        if getattr(self, 'requestOpen', False):
            self.containerListRequest.hide()
            self.requestOpen = False

        if getattr(self, 'finalsOpen', False):
            self.containerListFinal.hide()
            self.finalsOpen = False
        if getattr(self, 'deleteOpen', False):
            self.containerDelete.hide()
            self.deleteOpen = False


        super().focusOutEvent(event)

    def AddItemListRequest(self,customer_name, costumer_link):

        cursor.execute('''INSERT INTO requests (name,link) VALUES(?,?)''', (customer_name, costumer_link,))
        conexao.commit()
        item = QListWidgetItem(customer_name)

        item.setData(Qt.UserRole,costumer_link)

        self.label_lista_request.insertItem(0,item)

        # qnt_request = self.label_lista_request.count()
        # altura_req = self.label_lista_request.sizeHintForRow(0) * qnt_request + 5
        # self.label_lista_request.setFixedHeight(altura_req)

        self.adjustSize()


        self.textNoWorkRe.hide()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)
        if getattr(self, 'requestOpen', False) == False:
            self.notificationRequest.show()
            self.blinkRequest = True
            self.notificationSound.stop()
            self.notificationSound.play()
            if getattr(self, 'minimized', False):
                self.notificationMinimized.show()
                self.blinkMinimized = True

    def AddItemListFinals(self, customer_name,costumer_link):

        cursor.execute('''INSERT INTO finals (name,link) VALUES(?,?)''', (customer_name, costumer_link,))
        conexao.commit()

        item = QListWidgetItem(customer_name)

        item.setData(Qt.UserRole, costumer_link)

        self.label_lista_finals.insertItem(0, item)

        self.textNoWorkFi.hide()

        # qnt_request = self.label_lista_finals.count()
        # altura_req = self.label_lista_finals.sizeHintForRow(0) * qnt_request + 5
        # self.label_lista_finals.setFixedHeight(altura_req)

        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)
        if getattr(self, 'finalsOpen', False) == False:
            self.notificationFinal.show()
            self.blinkFinal = True
            self.notificationSound.stop()
            self.notificationSound.play()
            if getattr(self, 'miniminized', False):
                self.notificationMinimized.show()
                self.blinkMinimized = True

    def animateBlink(self):
        if self.blinkRequest:
            currentState = self.notificationRequest.isVisible()
            self.notificationRequest.setVisible(not currentState)
        if self.blinkFinal:
            currentState = self.notificationFinal.isVisible()
            self.notificationFinal.setVisible(not currentState)
        if self.blinkMinimized:
            currentState = self.notificationMinimized.isVisible()
            self.notificationMinimized.setVisible(not currentState)



    def vanish(self):
        self.labele.setText(f'Delete ALL the leads?')
        self.containerDelete.show()
        self.deleteOpen = True

        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)

        self.vanishRn = True



    def miniminizeScreen(self):
        self.fechar()
        if self.miniminized == False:
            self.button_request.hide()
            self.button_final.hide()


            self.miniminized = True
        elif self.miniminized == True:
            self.button_request.show()
            self.button_final.show()
            self.notificationMinimized.hide()
            self.blinkMinimized = False
            self.miniminized = False

        self.adjustSize()

        screen_geometry = QApplication.desktop().availableGeometry(self)
        pos_y = screen_geometry.height() - self.height()
        self.move(self.x(), pos_y)

    def fechar(self):
        if self.finalsOpen:
            self.containerListFinal.hide()
            self.finalsOpen = False
        elif self.requestOpen:
            self.containerListRequest.hide()
            self.requestOpen = False



    def updateConnection(self, status):
        self.connectionStatus = status
        if status == True:
            self.button_request.setIcon(QIcon(self.pixRe))
            self.button_final.setIcon(QIcon(self.pixFi))
        else:
            self.button_request.setIcon(QIcon(self.pixReOff))
            self.button_final.setIcon(QIcon(self.pixFiOff))

    def resizeEvent(self, event):
        preciseY = self.height() - 60

        if getattr(self,'miniminizeBtn',None):
            total_width = self.miniminizeBtn.width()
            posXHeight = self.miniminizeBtn.x()
            self.miniminizeBtn.setGeometry(posXHeight, preciseY, total_width,35)
            self.notificationMinimized.setGeometry(posXHeight, preciseY - 10, 16, 16)

        super().resizeEvent(event)



    def restartApp(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def checkInternet(self):
        try:
            urllib.request.urlopen('https://www.google.com',timeout=2)
            if self.internetStatus == False:
                print('[REDE] internet is back')
                self.tray_icon.setToolTip('Notification On')
                self.button_request.setIcon(QIcon(self.pixRe))
                self.button_final.setIcon(QIcon(self.pixFi))

                if hasattr(self, 'thread_pubsub'):
                    threading.Thread(target=self.thread_pubsub.Serach).start()


            self.internetStatus = True
        except:
            if self.internetStatus == True:
                print('[REDE] lost internet')
                self.tray_icon.setToolTip('Notification Off')
                self.button_request.setIcon(QIcon(self.pixReOff))
                self.button_final.setIcon(QIcon(self.pixFiOff))
            self.internetStatus = False









class pubsubListener(QThread):

    newRequest = pyqtSignal(str,str)
    newFinal = pyqtSignal(str,str)

    statusChanged = pyqtSignal(bool)

    authError = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.travar_banco = threading.Lock()


    def run(self):
        time.sleep(2)
        while True:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

            project_id = "SEU_PROJECT_ID_AQUI"
            subscription_id = "NOME_DA_SUA_INSCRICAO"
            print('[THREAD] iniciando conexao com o pubsub')

            topicName = f'projects/{project_id}/topics/NOME_DO_SEU_TOPICO'
            try:
                gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')
                request = {
                'labelIds': ['INBOX'],
                'topicName': topicName
                 }
                resposta = gmail.service.users().watch(userId='me', body=request).execute()
                print('conexao renovada')
                self.statusChanged.emit(True)

                print(resposta)
            except Exception as e:
                print(f'erro ao renovar conexao: {e}')
                self.statusChanged.emit(False)
                self.checkJsonError(e)
                time.sleep(60)
                continue


            try:
                subscriber = pubsub_v1.SubscriberClient()
                subscription_path = subscriber.subscription_path(project_id, subscription_id)
                print('[THREAD] conectado a pubsub')
                self.statusChanged.emit(True)

            except Exception as e:
                print(f'erro ao conectar o pubsub: {e}')
                self.tray_icon.setToolTip('Notification Off')
                self.statusChanged.emit(False)
                self.checkJsonError(e)
                time.sleep(60)
                continue

            def callback(message):
                print("\n========================================")
                print('mensagem recebida')


                message.ack()

                try:
                    self.Serach()
                except Exception as e:
                    print(f'erro ao serach: {e}')
                    print("========================================\n")
                    self.statusChanged.emit(False)

            future = subscriber.subscribe(subscription_path, callback=callback)

            try:
                future.result()
            except Exception:
                print('erro no future pubsub')
                self.statusChanged.emit(False)
                future.cancel()

                time.sleep(60)

    def checkJsonError(self, erro):
        errorText = str(erro).lower()
        if 'credential' in errorText or 'json' in errorText or 'auth' in errorText:
            self.authError.emit()


    def Serach(self):
        gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')



        with self.travar_banco:
            query_params = {
                'newer_than': (1, "day"),
                'unread': True
            }

            new_email = gmail.get_messages(query=construct_query(query_params))

            pattern_costumer = re.compile(r'Customer:\s*(.*)', re.IGNORECASE)
            pattern_link = re.compile(r'Open task\s*(.*)', re.IGNORECASE)
            for email in new_email:
                if email.plain:
                    match_name = pattern_costumer.search(email.plain)
                    match_link = pattern_link.search(email.plain)
                    if not match_name or not match_link:
                        continue

                    costumer_name = match_name.group(1).strip()
                    link = match_link.group(1).strip()

                    if email.subject == 'New task: Design Request':

                        print(f'email 3 {costumer_name}')
                        print(f'email 4 {link}')


                        # print(email.subject)
                        email.mark_as_read()
                        self.newRequest.emit(costumer_name, link)
                    elif email.subject == 'New task: Final Design & Production':

                        print(f'email 3 {costumer_name}')
                        print(f'email 4 {link}')


                        # print(email.subject)
                        email.mark_as_read()
                        self.newFinal.emit(costumer_name,link)



    # def setupUi(self,Window):
    #     Window.setObjectName('Window')
    #     Window.resize(800,600)
    #     Window.setStyleSheet('background-color: rgb(255, 255, 255);')
    #     flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    #     self.setWindowFlags(flags)




if __name__ == "__main__":
    App = QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(App.exec_())
