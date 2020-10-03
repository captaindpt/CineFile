# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finalUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import cinefile

movie_scanner = cinefile.MovieScanner("/")
director_scanner = cinefile.DirectorIcon("/")

directorIconIsChecked = True
movieIconIsChecked = True
moviePattern = "{YEAR} - {MOVIENAME}"
movieFormats = ["mp4", "mkv", "avi", "flv", "avi", "wmv"]


class InfoWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(349, 294)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.directoryLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.directoryLineEdit.setGeometry(QtCore.QRect(10, 10, 241, 20))
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.directoryLineEdit.textChanged.connect(lambda s: self.line_edit_text_changed())

        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(260, 10, 81, 23))
        self.browseButton.setObjectName("browseButton")
        self.browseButton.clicked.connect(lambda s: self.handle_browse_button())

        self.setDirectorIconCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.setDirectorIconCheckbox.setEnabled(True)
        self.setDirectorIconCheckbox.setGeometry(QtCore.QRect(20, 40, 121, 17))
        self.setDirectorIconCheckbox.setChecked(True)
        self.setDirectorIconCheckbox.setObjectName("setDirectorIconCheckbox")
        self.setDirectorIconCheckbox.stateChanged.connect(lambda s: self.icon_state_changed())

        self.setMovieIconCheckcbox = QtWidgets.QCheckBox(self.centralwidget)
        self.setMovieIconCheckcbox.setGeometry(QtCore.QRect(20, 60, 121, 17))
        self.setMovieIconCheckcbox.setChecked(True)
        self.setMovieIconCheckcbox.setObjectName("setMovieIconCheckbox")
        self.setDirectorIconCheckbox.stateChanged.connect(lambda s: self.icon_state_changed())

        self.infoAboutPatternLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoAboutPatternLabel.setGeometry(QtCore.QRect(20, 90, 231, 16))
        self.infoAboutPatternLabel.setObjectName("infoAboutPatternLabel")

        self.patternLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.patternLineEdit.setGeometry(QtCore.QRect(20, 110, 191, 20))
        self.patternLineEdit.setObjectName("patternLineEdit")
        self.patternLineEdit.textChanged.connect(lambda: self.pattern_line_edit_handle())

        self.defaultPatternLabel = QtWidgets.QLabel(self.centralwidget)
        self.defaultPatternLabel.setGeometry(QtCore.QRect(20, 140, 171, 16))
        self.defaultPatternLabel.setObjectName("defaultPatternLabel")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 170, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(20, 200, 171, 16))
        self.statusLabel.setObjectName("statusLabel")

        self.startOrganizeButton = QtWidgets.QPushButton(self.centralwidget)
        self.startOrganizeButton.setEnabled(False)
        self.startOrganizeButton.setGeometry(QtCore.QRect(80, 220, 171, 23))
        self.startOrganizeButton.setObjectName("startOrganizeButton")
        self.startOrganizeButton.clicked.connect(lambda s: self.start_button_handle())

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 349, 21))
        self.menubar.setObjectName("menubar")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        self.menuFormat = QtWidgets.QMenu(self.menuSettings)
        self.menuFormat.setObjectName("menuFormat")

        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        # self.menuAbout.
        self.menuHelp = QtWidgets.QAction(MainWindow)
        self.menuHelp.setObjectName("menuHelp")
        # self.menuHelp.triggered.connect(self.open_help_window())

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)
        self.actionExclude_folders = QtWidgets.QAction(MainWindow)
        self.actionExclude_folders.setCheckable(True)
        self.actionExclude_folders.setObjectName("actionExclude_folders")

        self.actionSearch_recursively = QtWidgets.QAction(MainWindow)
        self.actionSearch_recursively.setCheckable(True)
        self.actionSearch_recursively.setChecked(True)
        self.actionSearch_recursively.setObjectName("actionSearch_recursively")

        self.action_mkv = QtWidgets.QAction(MainWindow)
        self.action_mkv.setCheckable(True)
        self.action_mkv.setChecked(True)
        self.action_mkv.setObjectName("action_mkv")

        self.action_mp4 = QtWidgets.QAction(MainWindow)
        self.action_mp4.setCheckable(True)
        self.action_mp4.setChecked(True)
        self.action_mp4.setObjectName("action_mp4")
        self.action_mp4.changed.connect(lambda: self.format_changed())

        self.action_avi = QtWidgets.QAction(MainWindow)
        self.action_avi.setCheckable(True)
        self.action_avi.setChecked(True)
        self.action_avi.setObjectName("action_avi")
        self.action_avi.changed.connect(lambda: self.format_changed())

        self.action_flv = QtWidgets.QAction(MainWindow)
        self.action_flv.setCheckable(True)
        self.action_flv.setChecked(True)
        self.action_flv.setObjectName("action_flv")
        self.action_flv.changed.connect(lambda: self.format_changed())

        self.action_wmv = QtWidgets.QAction(MainWindow)
        self.action_wmv.setCheckable(True)
        self.action_wmv.setChecked(True)
        self.action_wmv.setObjectName("action_wmv")
        self.action_wmv.changed.connect(lambda: self.format_changed())

        self.menuFormat.addAction(self.action_mkv)
        self.menuFormat.addAction(self.action_mp4)
        self.menuFormat.addAction(self.action_avi)
        self.menuFormat.addAction(self.action_flv)
        self.menuFormat.addAction(self.action_wmv)

        self.menuSettings.addAction(self.actionExclude_folders)
        self.menuSettings.addAction(self.actionSearch_recursively)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.menuFormat.menuAction())

        self.menuAbout.addAction(self.menuHelp)

        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browseButton.setText(_translate("MainWindow", "Browse"))
        self.setDirectorIconCheckbox.setText(_translate("MainWindow", "Set Icons for Directors"))
        self.setMovieIconCheckcbox.setText(_translate("MainWindow", "Set Icons for Movies"))
        self.statusLabel.setText(_translate("MainWindow", "Status: downloading icons..."))
        self.startOrganizeButton.setText(_translate("MainWindow", "Start Organizing"))
        self.patternLineEdit.setText(_translate("MainWindow", "{YEAR} - {MOVIENAME}"))
        self.defaultPatternLabel.setText(_translate("MainWindow", "Default e. g. : 1941 - Citizen Kane"))
        self.infoAboutPatternLabel.setText(_translate("MainWindow", "Insert desired pattern for your folder names:"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuFormat.setTitle(_translate("MainWindow", "Formats"))
        self.menuHelp.setText(_translate("MainWindow", "Help"))
        self.actionExclude_folders.setText(_translate("MainWindow", "Exclude folders"))
        self.actionSearch_recursively.setText(_translate("MainWindow", "Search recursively"))
        self.action_mkv.setText(_translate("MainWindow", ".mkv"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.action_mp4.setText(_translate("MainWindow", ".mp4"))
        self.action_avi.setText(_translate("MainWindow", ".avi"))
        self.action_flv.setText(_translate("MainWindow", ".flv"))
        self.action_wmv.setText(_translate("MainWindow", ".wmv"))

    def pattern_line_edit_handle(self):
        global moviePattern
        moviePattern = self.patternLineEdit


    def handle_browse_button(self):
        direct = pick_new()
        self.directoryLineEdit.setText(direct)
        self.startOrganizeButton.setEnabled(True)

    def line_edit_text_changed(self):
        self.startOrganizeButton.setEnabled(bool(self.directoryLineEdit.text()))

    def start_button_handle(self):
        pass

    def open_help_window(self):
        pass

    def icon_state_changed(self):
        global directorIconIsChecked
        directorIconIsChecked = self.setDirectorIconCheckbox.isChecked()
        global movieIconIsChecked
        movieIconIsChecked = self.setMovieIconCheckcbox.isChecked()

    def format_changed(self):
        if self.action_mp4.isChecked():
            if "mp4" not in movieFormats:
                movieFormats.append("mp4")
        else:
            if "mp4" in movieFormats:
                movieFormats.remove("mp4")

        if self.action_mkv.isChecked():
            if "mkv" not in movieFormats:
                movieFormats.append("mkv")
        else:
            if "mkv" in movieFormats:
                movieFormats.remove("mkv")

        if self.action_avi.isChecked():
            if "avi" not in movieFormats:
                movieFormats.append("avi")
        else:
            if "avi" in movieFormats:
                movieFormats.remove("avi")

        if self.action_flv.isChecked():
            if "flv" not in movieFormats:
                movieFormats.append("flv")
        else:
            if "flv" in movieFormats:
                movieFormats.remove("flv")

        if self.action_wmv.isChecked():
            if "wmv" not in movieFormats:
                movieFormats.append("wmv")
        else:
            if "wmv" in movieFormats:
                movieFormats.remove("wmv")


def pick_new():
    dialog = QtWidgets.QFileDialog()
    folder_path = dialog.getExistingDirectory(None, "Select Folder")
    return folder_path


def start_organizing(self):
    movie_scanner.formats = movieFormats
    movie_scanner.basefolder = self.directoryLineEdit.text
    if "{MOVIENAME}" in moviePattern and "{YEAR}" in moviePattern:
        movie_scanner.folder_pattern = moviePattern
    director_scanner.basefolder = self.directoryLineEdit.text + "/CineFile"

    if movieIconIsChecked and directorIconIsChecked:
        movie_scanner.scan_folder()
        movie_scanner.make_folders()
        movie_scanner.set_icons()

        director_scanner.scan_folder()
        director_scanner.set_icons()
    elif movieIconIsChecked and not directorIconIsChecked:
        movie_scanner.scan_folder()
        movie_scanner.make_folders()
        movie_scanner.set_icons()

        director_scanner.scan_folder()
    elif not movieIconIsChecked and directorIconIsChecked:
        movie_scanner.scan_folder()
        movie_scanner.make_folders()

        director_scanner.scan_folder()
        director_scanner.set_icons()
    else:
        movie_scanner.scan_folder()
        movie_scanner.make_folders()

        director_scanner.scan_folder()



def main():
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
