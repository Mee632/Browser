from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1200, 600)
        self.home_url = "http://www.google.com"
        self.second_url = "https://duckduckgo.com/"

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.home_url))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.browser)

        self.setLayout(self.layout)

        # Add navigation buttons
        self.back_button = QPushButton("Back")
        self.forward_button = QPushButton("Forward")
        self.settings_button = QPushButton("Settings")

        self.back_button.clicked.connect(self.browser.back)
        self.forward_button.clicked.connect(self.browser.forward)
        self.settings_button.clicked.connect(self.open_settings)

        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.forward_button)
        self.layout.addWidget(self.settings_button)

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()


class SettingsWindow(QWidget):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 300, 200)

        self.theme_button = QPushButton("Switch Theme")
        self.browser_button = QPushButton("Switch Browser")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.theme_button)
        self.layout.addWidget(self.browser_button)
        self.setLayout(self.layout)

        self.theme_button.clicked.connect(self.switch_theme)
        self.browser_button.clicked.connect(self.switch_browser)

        self.browser_state = 0  # start with Google as default
        self.theme_state = 0  # start with White theme as default

        self.dark_theme = """
            QPushButton {
                background-color: #000000;
                color: white;
            }
        """

        self.light_theme = """
            QPushButton {
                background-color: #FFFFFF;
                color: black;
            }
        """

    def switch_theme(self):
        if self.theme_state == 0:
            self.setStyleSheet(self.dark_theme)
            self.theme_state = 1
        else:
            self.setStyleSheet(self.light_theme)
            self.theme_state = 0

    def switch_browser(self):
        if self.browser_state == 0:
            window.browser.setUrl(QUrl(window.second_url))
            self.browser_state = 1
        else:
            window.browser.setUrl(QUrl(window.home_url))
            self.browser_state = 0


app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec_())