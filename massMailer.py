# -*- coding: utf8 -*-

import os,sys
from mailer_ui import Ui_MainWindow
from email.utils import parseaddr
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
from smtplib import SMTP
from email_validator import validate_email, EmailNotValidError
# from validate_email import validate_email as separate_email

class mailerGui(QMainWindow):
    def __init__(self):
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
        self.ui.buttonSend.clicked.connect(self.sendMail)
        self.ui.buttonTo.clicked.connect(self.toPressed)
        self.ui.buttonCc.clicked.connect(self.ccPressed)
        self.ui.buttonBcc.clicked.connect(self.bccPressed)
        self.ui.buttonRemove.clicked.connect(self.removePressed)

        # lists

        # dicts
        # dictionary bir listede ayni mailden bir tane olmasini garantiler
        self.listTo = {}
        self.listCc = {}
        self.listBcc = {}

    def run(self):
        self.show()
        self.qt_app.exec_()

    def log(self, text):
        self.ui.logView.append(text)

    def validate_email(self, text):
        temp = parseaddr(text)
        try:
            v = validate_email(temp[1])
            email = v["email"]
            return email, temp[0]
        except:
            self.log("Invalid mail: %s" % (temp[1]))
            return False

    def readEmailList(self):
        toInput = self.ui.newEmail.text()
        toSplit = toInput.strip().split(',')
        emails = []
        for field in toSplit:
            email = self.validate_email(field)
            if email:
                emails.append(email)
        return emails

    def removePressed(self):
        items = self.ui.listTo.selectedItems()
        for item in items:
            email = item.text()
            del self.listTo[email]
            self.ui.listTo.takeItem(self.ui.listTo.row(item))
            self.log("Removed: %s" % (email))
        self.ui.listTo.update()

        items = self.ui.listCc.selectedItems()
        for item in items:
            email = item.text()
            del self.listCc[email]
            self.ui.listCc.takeItem(self.ui.listCc.row(item))
            self.log("Removed: %s" % (email))
        self.ui.listCc.update()

        items = self.ui.listBcc.selectedItems()
        for item in items:
            email = item.text()
            del self.listBcc[email]
            self.ui.listBcc.takeItem(self.ui.listBcc.row(item))
            self.log("Removed: %s" % (email))
        self.ui.listBcc.update()

    def toPressed(self):
        listMails = self.readEmailList()

        for email in listMails:
            if email[0] in self.listTo.keys():
                self.listTo[email[0]][0] = email[1]
                self.log("Modified: %s, %s" % (email[0], email[1]))
                continue
            item = QListWidgetItem(email[0])
            self.listTo[email[0]] = [ email[1], item ]
            self.ui.listTo.addItem(item)
            self.log("Added: %s, %s" % (email[0], email[1]))

    def ccPressed(self):
        listMails = self.readEmailList()

        for email in listMails:
            if email[0] in self.listCc.keys():
                self.listCc[email[0]][0] = email[1]
                self.log("Modified: %s, %s" % (email[0], email[1]))
                continue
            item = QListWidgetItem(email[0])
            self.listCc[email[0]] = [ email[1], item ]
            self.ui.listCc.addItem(item)
            self.log("Added: %s, %s" % (email[0], email[1]))

    def bccPressed(self):
        listMails = self.readEmailList()

        for email in listMails:
            if email[0] in self.listBcc.keys():
                self.listBcc[email[0]][0] = email[1]
                self.log("Modified: %s, %s" % (email[0], email[1]))
                continue
            item = QListWidgetItem(email[0])
            self.listBcc[email[0]] = [ email[1], item ]
            self.ui.listBcc.addItem(item)
            self.log("Added: %s, %s" % (email[0], email[1]))

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
            from_name = self.ui.name.text()

            to_addr = ""
            cc_addr = ""

            for email in self.listTo.keys():
                to_addr = to_addr + self.listTo[email][0] + " <" + email + ">, "
            to_addr = to_addr[:-2]

            for email in self.listCc.keys():
                cc_addr = cc_addr + self.listCc[email][0] + " <" + email + ">, "
            cc_addr = cc_addr[:-2]

            subj = self.ui.textSubject.text()
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            message_text = self.ui.textMail.toHtml()

            msg = "From: %s <%s>\n" \
                  "To: %s\n" \
                  "Cc: %s\n" \
                  "Subject: %s\n" \
                  "Date: %s\n" \
                  "\n" \
                  "%s" % (
                from_name,
                from_addr,
                to_addr,
                cc_addr,
                subj,
                date,message_text)

            # TODO: parca parca gonderim saglanacak 100'lu batchler halinde
            batch = list(self.listTo.keys()) + list(self.listCc.keys()) + \
                    list(self.listBcc.keys())

            self.log("Sending batch." + str(batch))

            smtp.sendmail(from_addr, batch, msg)
            smtp.quit()

            self.log("Email sent.")
        except:
            self.log("Sending failed.")

    def testSMTP(self):
        self.log("Testing SMTP.")
        smtp = SMTP()
        smtp.set_debuglevel(debuglevel=0)
        try:
            smtp.connect(self.smtpserver, self.smtpport)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.ui.username.text(), self.ui.password.text())
            smtp.quit()
            self.log("Test succeeded.")
        except:
            self.log("Test failed.")

def main():
    # the queue should contain no more than maxSize elements
    # QTextCodec.setCodecForCStrings(QTextCodec.codecForName("UTF-8"))

    app = mailerGui()
    app.run()

if __name__ == '__main__':
    main()

