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
from parser import *
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

        # size considerations
        self.ui.treeSources.header().resizeSection(0, 160)
        self.ui.treeSources.header().resizeSection(1, 160)
        self.ui.treeSources.header().resizeSection(2, 40)
        self.ui.treeDestination.header().resizeSection(0, 145)
        self.ui.treeDestination.header().resizeSection(1, 145)
        self.ui.treeDestination.header().resizeSection(2, 40)

        # buttons
        self.ui.buttonTestSMTP.pressed.connect(self.testSMTP)
        self.ui.buttonSend.pressed.connect(self.sendMail)
        self.ui.buttonTo.pressed.connect(lambda: self.modePressed("To"))
        self.ui.buttonCc.pressed.connect(lambda: self.modePressed("Cc"))
        self.ui.buttonBcc.pressed.connect(lambda: self.modePressed("Bcc"))
        self.ui.buttonSourceTo.pressed.connect(lambda:
                                               self.modeSourcePressed("To"))
        self.ui.buttonSourceCc.pressed.connect(lambda:
                                               self.modeSourcePressed("Cc"))
        self.ui.buttonSourceBcc.pressed.connect(lambda:
                                                self.modeSourcePressed("Bcc"))
        self.ui.buttonRemove.pressed.connect(self.removePressed)

        # load buttons
        self.ui.buttonReadCharlemagne.pressed.connect(self.readCharleData)

        # lists
        self.ui.listCategories.itemSelectionChanged.connect(
            self.onSelectionChanged)
        self.ui.buttonClearCategories.pressed.connect(self.clearCategories)

        # dictionary bir listede ayni mailden bir tane olmasini garantiler
        self.emailList = {}
        self.parents = {}
        self.categories = {}

    def run(self):
        self.show()
        self.qt_app.exec_()

    def log(self, text):
        self.ui.logView.append(text)

    def readCharleData(self):
        dataFile, filt = QFileDialog.getOpenFileName(self,
                                               caption='Open file',
                                               directory='./data',
                                               filter='Charlemagne Data (*.csv)')
        print(dataFile)

        self.parents, self.categories = parse_charlemagne(dataFile, delim=';')
        for category in self.categories.keys():
            item = QListWidgetItem(category)
            self.ui.listCategories.addItem(item)
        self.ui.listCategories.sortItems()

        for email in self.parents.keys():
            item = QTreeWidgetItem((
                email,
                self.parents[email][0],
                ' '.join(self.parents[email][1])))
            self.ui.treeSources.addTopLevelItem(item)
            self.parents[email].append(item)

    def onSelectionChanged(self):
        # get selected categories
        selectedCategories = []
        temp = self.ui.listCategories.selectedItems()
        for item in temp:
            selectedCategories.append(item.text())

        # selection = []

        self.ui.treeSources.clearSelection()
        for category in selectedCategories:
            for email in self.categories[category]:
                self.parents[email][2].setSelected(True)

    def clearCategories(self):
        self.ui.listCategories.clearSelection()

    def validate_email(self, text):
        temp = parseaddr(text)
        try:
            v = validate_email(temp[1])
            email = v["email"]
            return email, temp[0]
        except:
            self.log("Invalid mail: %s" % (temp[1]))
            return False

    def readEmailLine(self):
        toInput = self.ui.newEmail.text()
        toSplit = toInput.strip().split(',')
        emails = []
        for field in toSplit:
            email = self.validate_email(field)
            if email:
                emails.append(email)
        return emails

    def removePressed(self):
        items = self.ui.treeDestination.selectedItems()
        root = self.ui.treeDestination.invisibleRootItem()
        for item in items:
            email = item.text(0)
            root.removeChild(item)
            del self.emailList[email]
            self.log("Removed: %s" % (email))
        self.ui.treeDestination.update()

    def modePressed(self, mode):
        listMails = self.readEmailLine()

        for email in listMails:
            if email[0] in self.emailList.keys():
                self.emailList[email[0]][0] = email[1]
                self.emailList[email[0]][1] = mode

                self.emailList[email[0]][2].setText(1, email[1])
                self.emailList[email[0]][2].setText(2, mode)

                self.log("Modified: %s, %s, %s" % (email[0], email[1], mode))
                continue
            item = QTreeWidgetItem()
            item.setText(1, email[1])
            item.setText(0, email[0])
            item.setText(2, mode)
            self.ui.treeDestination.addTopLevelItem(item)
            self.emailList[email[0]] = [email[1], mode, item]
            self.log("Added: %s, %s, %s" % (email[0], email[1], mode))

    def modeSourcePressed(self, mode):

        for item in self.ui.treeSources.selectedItems():
            email = (item.text(0), item.text(1))

            if email[0] in self.emailList.keys():
                self.emailList[email[0]][0] = email[1]
                self.emailList[email[0]][1] = mode

                self.emailList[email[0]][2].setText(1, email[1])
                self.emailList[email[0]][2].setText(2, mode)

                self.log("Modified: %s, %s, %s" % (email[0], email[1], mode))
                continue

            item = QTreeWidgetItem()
            item.setText(1, email[1])
            item.setText(0, email[0])
            item.setText(2, mode)
            self.ui.treeDestination.addTopLevelItem(item)
            self.emailList[email[0]] = [email[1], mode, item]
            self.log("Added: %s, %s, %s" % (email[0], email[1], mode))


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

