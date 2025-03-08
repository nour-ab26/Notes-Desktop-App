import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from threading import Thread
from website import create_app  # Import the create_app function

# Create the Flask app
app = create_app()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:5000"))
        self.setCentralWidget(self.browser)
        self.setWindowTitle("Note-Taking App")
        self.show()
        
            # Add system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # Add an icon file (place icon.png in the root folder)
        self.tray_icon.setVisible(True)

        # Add a context menu to the tray icon
        tray_menu = QMenu()
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        self.tray_icon.setContextMenu(tray_menu)    

    def closeEvent(self, event):
        # Shut down the Flask server when the window is closed
        import requests
        requests.post('http://127.0.0.1:5000/shutdown')  # Call the shutdown endpoint
        event.accept()

def run_flask_app():
    app.run(use_reloader=False)  # Run your Flask app

if __name__ == "__main__":
    # Start Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the PyQt application
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(qt_app.exec_())