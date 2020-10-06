import ctypes, sys
from .ratConvert import ratConvertClass
from PySide2.QtWidgets import QApplication
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')

def main():
    app = QApplication(sys.argv)
    window=ratConvertClass()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
