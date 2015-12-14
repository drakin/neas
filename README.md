# Neas
Neas is a open source project for JINR.

It's 

- PyQt based GUI
- 3D visualization
- Data manipulation

## Installation Guide
1. Install git 
  - Windows [git]
1. Clone repository

  ```
  git clone https://github.com/drakin/neas.git
  ```
1. Download and install python 2.7 and add it to PATH [python x64] or [python x86]
1. Install requiried python libs
  - Windows
      1. Download and install PyQt [pyqt x64] or [pyqt x86]
      1. Download pyqtgraph and install [pyQtGraph x64] or [pyQtGraph x86] 
      1. Execute
      ```
          pip install PyOpenGL PyOpenGL_accelerate qrangeslider
      ```
1. Check

  ```
  >pip list
  numpy (1.9.3)
  pip (7.1.2)
  PyOpenGL (3.1.0)
  PyOpenGL-accelerate (3.1.0)
  PyQt4 (4.11.4)
  pyqtgraph (0.9.10)
  qrangeslider (0.1.1)
  setuptools (18.2)
  wheel (0.24.0)
  ```
1. Run main or execute

    ```
        python main.py
    ```
[git]: https://git-scm.com/downloads
[python x64]: https://www.python.org/ftp/python/2.7.11/python-2.7.11.amd64.msi
[python x86]: https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi
[pyQt x64]: http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x64.exe
[pyQt x86]: http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe
[pyQtGraph x64]: http://www.pyqtgraph.org/downloads/pyqtgraph-0.9.10.win-amd64.exe
[pyQtGraph x86]: http://www.pyqtgraph.org/downloads/pyqtgraph-0.9.10.win32.exe
