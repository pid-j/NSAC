# modified from https://github.com/ProgrammingHero1/my_cool_browser
from requests import get
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

PAGE_URL = "https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/%s"

page_cache = {}

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)
        self.navigate_home()

    def navigate_home(self):
        self.navigate_to_url("nsac://example.nsac")

    def navigate_to_url(self, url: str = None):
        if url is None:
            url = self.url_bar.text()
        if url.startswith("nsac://"):
            ourl = url
            url = url.replace("nsac://", "", 1)
            if len(url.split("/")) <= 2: url += "/"
            if url.endswith("/"): url += "index.html"
            url = PAGE_URL % url
            if url in page_cache.keys():
                self.browser.setHtml(page_cache[url], QUrl(ourl))
            else:
                r = get(url).text
                self.browser.setHtml(r, QUrl(ourl))
                page_cache[url] = r
        else:
            self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        url = q.toString()
        url = url.replace("https://raw.githubusercontent.com/pid-j/NSAC/refs/heads/main/web/",
                          "nsac://", 1)
        url = url.removesuffix("index.html")
        self.url_bar.setText(url)


app = QApplication([])
QApplication.setApplicationName("NSAC Browser")
window = MainWindow()
app.exec_()