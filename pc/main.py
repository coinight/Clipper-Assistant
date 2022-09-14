import _thread
import sys, socket
import threading
import time
import clipboard
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QMessageBox, QPushButton,
                             QLabel, QCheckBox, QComboBox, QLineEdit, QSpinBox, QWidget,
                             QMenu, QAction, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QTextEdit, QGroupBox, QStyle, QSystemTrayIcon)


class SystemTrayDemo(QDialog):
    def __init__(self):
        super(SystemTrayDemo, self).__init__()
        self.alive = True
        self.cil_enable = False
        self.first_socket = True
        # 设置窗口标题
        self.setWindowTitle('剪切板小助手')
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # 设置窗口尺寸
        self.resize(400, 300)
        self.size = 26
        self.dy = -5
        self.grpMessageBox = QGroupBox('设置')
        self.label = QLabel(self.grpMessageBox)
        self.label.setGeometry(QtCore.QRect(10, 10, 180, 41))
        self.label.setObjectName("label")
        self.label.setText("当前IP:" + socket.gethostbyname(socket.gethostname()) + ':8080')

        self.pushButton = QPushButton("开启服务器", self)
        self.pushButton.setGeometry(QtCore.QRect(25, 80, 75, 30))
        self.pushButton.clicked.connect(self.cil_open)

        self.select_size = QLineEdit(self.grpMessageBox)
        self.size_label = QLabel('字体大小', self.grpMessageBox)
        self.size_label.setGeometry(QtCore.QRect(10, 40, 70, 20))
        self.select_size.setGeometry(QtCore.QRect(60, 40, 60, 20))
        self.select_size.setText(str(self.size))

        self.select_bias_dy = QLineEdit(self.grpMessageBox)
        self.bias_dy_label = QLabel('y偏移', self.grpMessageBox)
        self.bias_dy_label.setGeometry(QtCore.QRect(10, 65, 70, 20))
        self.select_bias_dy.setGeometry(QtCore.QRect(60, 65, 60, 20))
        self.select_bias_dy.setText(str(self.dy))

        self.sysIcon = QIcon('./test.ico')
        self.setWindowIcon(self.sysIcon)

        self.initUi()

    def cil_open(self):
        if not self.cil_enable:
            self.cil_enable = True
            self.size = int(self.select_size.text())
            print(self.size)
            self.pushButton.setText("关闭服务器")
            self.st = threading.Thread(target=self._socketThread)
            self.st.start()
        else:
            self.cil_enable = False
            self.pushButton.setText("开启服务器")

    def initUi(self):

        self.createTrayIcon()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.grpMessageBox)
        mainLayout.addWidget(self.pushButton)
        self.setLayout(mainLayout)

        # 让托盘图标显示在系统托盘上
        self.trayIcon.show()

    def _socketThread(self):
        if self.first_socket:
            clipboard.Socket_Connect.s.bind((clipboard.Socket_Connect.ip, 8080))
            clipboard.Socket_Connect.s.listen(10)
            self.first_socket = False
        print("等待连接")
        new_cil, addr = clipboard.Socket_Connect.s.accept()  # 建立客户端连接。
        _thread.start_new_thread(clipboard.Socket_Connect.shack_hand, (new_cil, addr))
        while self.cil_enable and self.alive:
            t = time.time()
            if t - clipboard.flag_delta > clipboard.flag_delta_time and clipboard.win32api.GetKeyState(
                    clipboard.win32con.VK_CONTROL) < 0 and clipboard.win32api.GetKeyState(ord('F')) < 0:
                clipboard.flag_delta = t
                print("copy")
                clipboard.get_clipboard(self.size)
        new_cil.close()

    def onDestroy(self):
        self.alive = False
        QApplication.instance().quit()

    # 创建托盘图标
    def createTrayIcon(self):
        aRestore = QAction('恢复(&R)', self, triggered=self.showNormal)
        aQuit = QAction('退出(&Q)', self, triggered=self.onDestroy)

        menu = QMenu(self)
        menu.addAction(aRestore)
        menu.addAction(aQuit)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)

    # 显示气球信息
    def showMessage(self):
        # 根据消息类型获取图标
        icon = QSystemTrayIcon.MessageIcon(self.cmbType.itemData(self.cmbType.currentIndex()))
        self.trayIcon.showMessage(self.titleEdit.text(),  # 标题
                                  self.bodyEdit.toPlainText(),  # 信息
                                  icon,  # 图标
                                  self.durationSpinBox.value() * 1000)  # 信息显示持续时间

    # 关闭事件处理, 不关闭，只是隐藏，真正的关闭操作在托盘图标菜单里
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QMessageBox.information(self, '提示',
                                    '程序已隐藏到托盘')
            self.hide()
            event.ignore()

    def messageClicked(self):
        # 弹出信息被点击
        self.showNormal()
        print('clicked')
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) #置顶
        # self.setWindowFlags(QtCore.Qt.Widget) #取消置顶
        # QMessageBox.information(None, '系统托盘',
        #                         '对不起，我已经尽力了。'
        #                         '也许你应该试着问一个人?')

    def iconActivated(self, reason):
        if reason == 3:
            self.showNormal()
        print(reason)
        # self.showNormal()
        # print('iconActivated')
        # if reason in (QSystemTrayIcon.DoubleClick, QSystemTrayIcon.MiddleClick):
        #     self.showMessage()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 如果系统不支持最小化到托盘
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, '系统托盘', '本系统不支持托盘功能')
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    window = SystemTrayDemo()
    window.show()
    sys.exit(app.exec())
