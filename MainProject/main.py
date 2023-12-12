import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QAction, QToolBar, QDialog, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.browser = parent
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Button for theme change
        self.themeButton = QPushButton("Change Theme", self)
        self.themeButton.clicked.connect(self.change_theme)
        self.layout.addWidget(self.themeButton)

        # Button to toggle search engine
        self.searchEngineButton = QPushButton("Toggle Search Engine", self)
        self.searchEngineButton.clicked.connect(self.toggle_search_engine)
        self.layout.addWidget(self.searchEngineButton)

        self.setLayout(self.layout)

    def change_theme(self):
        if self.browser.is_light_theme:
            self.browser.setStyleSheet("QWidget { background-color: white; }")
            self.browser.is_light_theme = False
        else:
            self.browser.setStyleSheet("QWidget { background-color: darkgray; }")
            self.browser.is_light_theme = True

    def toggle_search_engine(self):
        self.browser.use_duckduckgo = not self.browser.use_duckduckgo
        if self.browser.use_duckduckgo:
            self.browser.default_search_engine = "https://www.duckduckgo.com/?q="
        else:
            self.browser.default_search_engine = "http://www.google.com/search?q="


class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.browser = QWebEngineView()
        self.default_search_engine = "http://www.google.com/search?q="
        self.use_duckduckgo = False
        self.is_light_theme = True
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl("http://www.google.com"))
        self.initUI()

    def initUI(self):
        # Toolbar
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        # Back button
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # Forward button
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navtb.addAction(forward_btn)

        # Refresh button
        refresh_btn = QAction('Refresh', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navtb.addAction(refresh_btn)

        # Home button
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # URL bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        # Update URL bar
        self.browser.urlChanged.connect(self.update_urlbar)

        # Settings button
        settings_btn = QAction('Settings', self)
        settings_btn.triggered.connect(self.open_settings)
        navtb.addAction(settings_btn)

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url.startswith('http'):
            url = self.default_search_engine + url
        self.browser.setUrl(QUrl(url))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())

    def open_settings(self):
        self.settingsDialog = SettingsDialog(self)
        self.settingsDialog.show()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url.startswith('http'):
            url = self.default_search_engine + url
        self.browser.setUrl(QUrl(url))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())

    def open_settings(self):
        self.settingsDialog = SettingsDialog(self)
        self.settingsDialog.show()


app = QApplication(sys.argv)
QApplication.setApplicationName('My Browser')
window = Browser()
window.show()
app.exec_()
