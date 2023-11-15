import sys

from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtWidgets import *


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print("hello world")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://www.duckduckgo.com"))
        self.setStyleSheet("background-color: #aaaaaa;")

        self.setCentralWidget(self.browser)

        # Create navigation bar
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Back button
        back_btn = QAction("<-", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("->", self)
        forward_btn.setStatusTip("Forward to next page")
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        # Home button
        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # Separate the navigation buttons from the URL bar
        navbar.addSeparator()

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Search button
        search_btn = QAction("Search", self)
        search_btn.setStatusTip("Search the web")
        search_btn.triggered.connect(self.navigate_to_url)
        navbar.addAction(search_btn)

        # Settings button
        settings_btn = QAction("Settings", self)
        settings_btn.setStatusTip("Open settings")
        settings_btn.triggered.connect(self.open_settings)
        navbar.addAction(settings_btn)

        # Update URL bar
        self.browser.urlChanged.connect(self.update_urlbar)

        # Handle settings window
        self.settings_window = SettingsWindow(self)

        self.showMaximized()

    def navigate_home(self):
        self.browser.setUrl(QUrl("http://www.duckduckgo.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.browser.setUrl(q)

    def update_urlbar(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.setCursorPosition(0)

    def open_settings(self):
        self.settings_window.show()

    def set_default_search_engine(self, engine):
        search_settings = QWebEngineSettings.globalSettings()
        if engine == "google":
            search_settings.setDefaultSearchEngine("https://www.google.com/search?q={}")
        elif engine == "duckduckgo":
            search_settings.setDefaultSearchEngine("https://duckduckgo.com/?q={}")


# New window
class SettingsWindow(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.setGeometry(parent.x() + 50, parent.y() + 50, 300, 200)
        self.setWindowTitle("Settings")

        # Theme button
        theme_btn = QPushButton("Change Theme", self)
        theme_btn.clicked.connect(self.change_theme)
        theme_btn.setGeometry(10, 10, 150, 30)

        search_label = QLabel("Default Search Engine:", self)
        search_label.setGeometry(10, 50, 150, 30)

        self.search_combo = QComboBox(self)
        self.search_combo.addItems(["Google", "DuckDuckGo"])
        self.search_combo.setGeometry(160, 50, 120, 30)

        search_btn = QPushButton("Apply", self)
        search_btn.clicked.connect(self.apply_search_engine)
        search_btn.setGeometry(10, 90, 100, 30)

    def change_theme(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()};")

    def apply_search_engine(self):
        selected_engine = self.search_combo.currentText().lower()
        self.parent().set_default_search_engine(selected_engine)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Simple Browser")
    main_window = BrowserWindow()
    app.exec_()