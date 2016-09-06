import sys
import sip
import string
import os
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QDialog
from namechecker_ui import Ui_NameChecker
from build_lists import *
from check_avoids import *
from check_domains import *
from search_keys import *

"""
C:/Python27/Lib/site-packages/PyQt4/pyuic4.bat -x <UI FILE NAME>.ui -o <PYTHON FILE NAME>.py
"""

reload(sys)
sys.setdefaultencoding('utf-8')

class MainWindow(QMainWindow):

    # Set up our project specific avoids - these will load the last saved avoids on start
    project_avoids = {}
    project_avoids_list = []
    internal_names = []
    competitor_names = []

    # Starts empty lists for different name input/outputs
    created_names = []
    stripped_names = []
    url_names = []

    # Builds INN and Pharma avoids lists
    inn_avoids = INN_AVOIDS_DICTIONARY
    pharma_avoids = PHARMA_AVOIDS_DICTIONARY


    def __init__(self):
        super(MainWindow, self).__init__()
        #self.ui = uic.loadUi('genie_ui.ui')
        self.ui = Ui_NameChecker()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('lamp.ico'))

        # Save names
        self.ui.save_names_btn.clicked.connect(self.save_names)
        self.ui.save_names_btn.setShortcut("Ctrl+S")

        # Save avoids
        self.ui.save_avoids_btn.clicked.connect(self.save_avoids)
        self.ui.save_avoids_btn.setShortcut("Ctrl+S")

        # Check names
        self.ui.check_names_btn.clicked.connect(self.check_names)
        self.ui.check_names_btn.setShortcut("Ctrl+Enter")

        # Get URL status
        self.ui.get_url_btn.clicked.connect(self.check_url)
        self.ui.get_url_btn.setShortcut("Ctrl+Enter")

        # Exit app
        self.ui.exit_btn.clicked.connect(self.close_app)
        self.ui.exit_btn.setShortcut("Ctrl+Q")

        # Clear avoids
        self.ui.clear_avoids_btn.clicked.connect(self.clear_avoids)

        # Check all boxes
        self.ui.checkBox_all.stateChanged.connect(self.check_uncheck)

        # Sort names
        self.ui.sort_names_btn.clicked.connect(self.sort_names)

        # Set up text outputs with known avoids
        self.get_avoids_at_start()
        self.show_avoids()
        self.show_pharma_avoids()
        self.show_inn_avoids()

        self.ui.PIU_radio.setChecked(True)
        self.ui.parse_btn.clicked.connect(self.get_keys)


    # Gets names input by user, saves them to a list, and displays stripped names in textBrowser_stripped
    def save_names(self):
        # Take in input names and convert to string
        names_text = str(self.ui.textEdit_names.toPlainText())

        # Build a list of items from the names text split on each new line
        self.created_names = [x.strip(string.whitespace) for x in names_text.split("\n") if x.strip(string.whitespace)]

        # Strip the names of rationale and other notes to disply in textBrowser_stripped
        self.stripped_names = strip_names(names_text)

        # Create a seperate list of stripped_names that can be shown sorted - we do not want the
        # url names and search key names sorted or some names will be out of order in an annoying way
        show_stripped = [x for x in self.stripped_names]
        show_stripped.sort()

        # Join the list items as text for display purposes
        self.ui.textBrowser_stripped.setPlainText("\n".join(show_stripped))

        # put names into the proper form for the URL status tab text output
        self.url_names = ["--- : " + x for x in self.stripped_names]
        self.ui.textBrowser_url_status.setText("\n".join(self.url_names))
        self.ui.names_text.setPlainText("\n".join(self.stripped_names))
        self.ui.textBrowser_conflicts.clear()


    # Allows user to sort their imput names
    def sort_names(self):
        self.save_names()
        self.created_names.sort()
        self.ui.textEdit_names.setPlainText("\n".join(self.created_names))

    # Check or uncheck all boxes
    def check_uncheck(self) :
        if self.ui.checkBox_all.isChecked() :
            self.check_all_boxes()
        else :
            self.uncheck_all_boxes()

    # Checks all avoids
    def check_all_boxes(self) :
        self.ui.check_box_pharma.setChecked(True)
        self.ui.check_box_inn.setChecked(True)
        self.ui.check_box_project.setChecked(True)
        self.ui.check_box_internal.setChecked(True)
        self.ui.check_box_competitor.setChecked(True)

    # Unchecks all avoids
    def uncheck_all_boxes(self) :
        self.ui.check_box_pharma.setChecked(False)
        self.ui.check_box_inn.setChecked(False)
        self.ui.check_box_project.setChecked(False)
        self.ui.check_box_internal.setChecked(False)
        self.ui.check_box_competitor.setChecked(False)

    # Finds conflicts for each name based on conflicts selected
    def check_names(self) :
        checks = 0
        # Get user's input for stem(s) to ignore
        ignore = self.ui.lineEdit_ignore.text()
        self.save_avoids()

        # Start with blank text each time conflict checks are run
        text = "<p style =\" white-space: pre-wrap;\" >"

        if len(self.created_names) == 0 :
            text +="<h4style \"font-weight:bold;\">No names committed!<h4>"
        else:

            # Check names against INN avoids - return html text with avoid highlighted in red within name
            if self.ui.check_box_inn.isChecked() :
                text += "<h4>INN Avoid Conflicts</h4>" + check_avoids(self.stripped_names, self.inn_avoids, "inn", ignore)
                checks += 1

            # Check names against Pharma avoids - return html text with avoid highlighted in red within name
            if self.ui.check_box_pharma.isChecked() :
                text += "<h4>Pharma Avoid Conflicts</h4>" + check_avoids(self.stripped_names, self.pharma_avoids, "pharma")
                checks += 1

            # Check names against project avoids - return html text with avoid highlighted in red within name
            if self.ui.check_box_project.isChecked() :
                text += "<h4>Project Avoid Conflicts</h4>" + check_avoids(self.stripped_names, self.project_avoids, "project")
                checks += 1

            # Check names against internal/presented names and return html text listing the conflicts
            if self.ui.check_box_internal.isChecked() :
                text += "<h4>Internal/Presented Name Conflicts:</h4>" + check_internal_names(self.stripped_names, self.internal_names)
                checks += 1

            # Check names against competitor names and return html text listing the conflicts and with conflicting strings in red
            if self.ui.check_box_competitor.isChecked() :
                text += "<h4>Competitor Name Conflicts:</h4>" + check_competitor_names(self.stripped_names, self.competitor_names)
                checks += 1

            if checks == 0 :
                text +="<h4style \"font-weight:bold;\">No avoids checked!<h4>"


        text += "</p>"


        self.ui.textBrowser_conflicts.setText(text)

        # Close the application
    def close_app(self):
        choice = QtGui.QMessageBox.question(self, "Quit", "Leave?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes :
            print "Yes: Exiting..."
            sys.exit()
        else :
            print "No: Not exiting..."
            pass

    def get_avoids_at_start(self) :

        # Check if
        try:
            with open("avoids.txt", "r") as f:
                for line in f:
                    if line[0:4] == "Proj":
                        self.project_avoids_list = line.strip("Project:").split(",")
                    if line[0:4] == "Inte":
                        self.internal_names = line.strip("Internal:").split(",")
                    if line[0:4] == "Comp":
                        self.competitor_names = line.strip("Competitor:").split(",")
            f.close()
        except:
            pass

    def clear_avoids(self):
        choice = QtGui.QMessageBox.question(self, "Quit", "Clear all avoids?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        if choice == QtGui.QMessageBox.Yes :

            print "Clearing avoids"
            with open("avoids.txt", "w")as f:
                f.close()
            del self.project_avoids_list[:]
            self.ui.plainTextEdit_project.clear()
            del self.internal_names[:]
            self.ui.plainTextEdit_internal.clear()
            del self.competitor_names[:]
            self.ui.plainTextEdit_competitor.clear()

            # Deleted the avoids.txt file when clearing avoids
            try:
                os.remove("avoids.txt")
            except:
                pass
            self.show_avoids()
        else :
            pass

    def show_avoids(self):
        if self.project_avoids_list :
            self.ui.plainTextEdit_project.setPlainText("\n".join(self.project_avoids_list))
        if self.internal_names :
            self.ui.plainTextEdit_internal.setPlainText("\n".join(self.internal_names))
        if self.competitor_names :
            self.ui.plainTextEdit_competitor.setPlainText("\n".join(self.competitor_names))



    # Saves avoids input by the user
    def save_avoids(self):
        print "Saving avoids"
        #First converts any special characters (e.g smart quotes to staright quotes or em dashes to regular deshes) then splits each item into a list
        p_text=(str(self.ui.plainTextEdit_project.toPlainText()).replace(u"\u2018", '"').replace(u"\u2019", '"').\
        replace(u"\u201c",'"').replace(u"\u201d", '"').replace(u"\u2013", "-")).split("\n")

        # Strip each avoid of any extra whitespace characters then send to build_project_avoids to get a sorted dictionary
        self.project_avoids_list = [str(x).strip(string.whitespace) for x in p_text if x.strip()]
        self.project_avoids = build_project_avoids(self.project_avoids_list)

        # Take in all names listed under presented/internal names
        i_text = str(self.ui.plainTextEdit_internal.toPlainText())

        # Split text on the \n and strips whitespace leaving out any lines that are purely whitespace
        self.internal_names = [x.strip(string.whitespace) for x in i_text.split("\n") if x.strip(string.whitespace)]

        # Take in all names listed under presented/internal names
        c_text = str(self.ui.plainTextEdit_competitor.toPlainText())

        # Split text on the \n and strips whitespace leaving out any lines that are purely whitespace
        self.competitor_names = [x.strip(string.whitespace) for x in c_text.split("\n") if x.strip(string.whitespace)]

        self.project_avoids_list.sort()
        self.project_avoids["prefix"].sort()
        self.project_avoids["infix"].sort()
        self.project_avoids["suffix"].sort()
        self.internal_names.sort()
        self.competitor_names.sort()
        self.show_avoids()
        write_avoids(self.project_avoids_list, self.internal_names, self.competitor_names)


    def show_pharma_avoids(self):
        text_list = build_avoids_output(self.pharma_avoids)
        self.ui.textBrowser_pharma_prefix.setPlainText(text_list[0])
        self.ui.textBrowser_pharma_infix.setPlainText(text_list[1])
        self.ui.textBrowser_pharma_suffix.setPlainText(text_list[2])

    def show_inn_avoids(self):
        text_list = build_avoids_output(self.inn_avoids)
        self.ui.textBrowser_inn_prefix.setPlainText(text_list[0])
        self.ui.textBrowser_inn_infix.setPlainText(text_list[1])
        self.ui.textBrowser_inn_suffix.setPlainText(text_list[2])


    # Checks the status of the url for each name (*name*.com for each name)
    def check_url(self):
        url_text = check_domain(self.stripped_names)
        self.ui.textBrowser_url_status.setText(url_text)


    def get_keys(self) :
        if self.ui.structural_radio.isChecked() :
            self.get_structural()
        else:
            self.get_PIU()

    def get_PIU(self) :

        print "Getting PIU search keys..."
        text = str(self.ui.names_text.toPlainText())

        names_list = [x.lower() for x in strip_names(text) if x.strip(string.whitespace)]

        search_key = ""
        for x in names_list:
            if len(x) > 1 :

                # Check if starting letter is a vowel and add search keys to line
                if x[0].lower() in VOWELS[0:5] and len(x[1:]) >= 5:
                    search_key += get_piu_key(x) + " or " + get_piu_key(x[1:]) + "\n"
                # Get search key for main name
                else :
                    search_key += get_piu_key(x) + "\n"

                search_key += check_j(x)
                search_key += check_q(x)
                search_key += check_x(x)

        self.ui.parsed_text.setPlainText(search_key)
        self.ui.names_text.setPlainText("\n".join(names_list))

    def get_structural(self) :
        print "Getting structural search keys..."
        text = str(self.ui.names_text.toPlainText())

        names_list = [x.lower() for x in strip_names(text) if x.strip(string.whitespace)]

        search_key = ""
        for x in names_list:
            if len(x) > 1 :
                search_key += get_structural_key(x) + "\n"

        self.ui.names_text.setPlainText("\n".join(names_list))
        self.ui.parsed_text.setPlainText(search_key)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")

    NameChecker = MainWindow()
    NameChecker.show()

    sip.setdestroyonexit(False)
    sys.exit(app.exec_())
