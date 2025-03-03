import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.addImportPath(sys.path[0])
engine.loadFromModule("qml", "Main")
if not engine.rootObjects():
    sys.exit(-1)
exit_code = app.exec()
del engine
sys.exit(exit_code)