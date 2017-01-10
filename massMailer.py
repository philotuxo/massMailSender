# -*- coding: utf8 -*-

import os,sys
from mailer_ui import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import queue
import datetime
from smtplib import SMTP

class mailerGui(QMainWindow):
    def __init__(self, appQueue, cliQueue):
        # constructor

        self.qt_app = QApplication(sys.argv)
        QWidget.__init__(self, None)

       # create the main ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # constants
        self.smtpserver = "smtp.gmail.com"
        self.smtpport = 587

        # buttons
        self.ui.buttonTestSMTP.clicked.connect(self.testSMTP)

    def run(self):
        self.show()
        self.qt_app.exec_()


    def log(self, text):
        self.ui.logView.append(text)


    def sendMail(self):
        self.log("Sending mail.")
        smtp = SMTP()
        smtp.set_debuglevel(debuglevel=0)
        try:
            smtp.connect(self.smtpserver, self.smtpport)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.ui.username.text(), self.ui.password.text())
            from_addr = self.ui.username.text()
            to_addr = "test@gmail.com"

            subj = "hello"
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            message_text = "Hello\nThis is a mail from %s\n\nBye\n" % (
                self.ui.username.text())

            msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (
                from_addr, to_addr, subj, date, message_text)

            smtp.sendmail(from_addr, to_addr, msg)
            smtp.quit()

            self.log("Email sent.")
        except:
            self.log("Sending failed.")

    def testSMTP(self):
        self.log("Testing SMTP.")
        smtp = SMTP()
        smtp.set_debuglevel(debuglevel=0)
        print(self.ui.username.text())
        print(self.ui.password.text())
        try:
            smtp.connect(self.smtpserver, self.smtpport)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.ui.username.text(), self.ui.password.text())
            self.log("Test succeeded.")
        except:
            self.log("Test failed.")

def main():
    # the queue should contain no more than maxSize elements
    # QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    workThreads = []
    appQueue = queue.Queue()
    cliQueue = queue.Queue()

    app = mailerGui(appQueue, cliQueue)
    app.run()

    for thread in workThreads:
        thread.join()

if __name__ == '__main__':
    main()

