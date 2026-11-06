# Json To SqLite🔥



**This project allows to import files with arrays of json files into a table in a [SQLite](https://www.sqlite.org/) database created by the scope.
The project provides a graphical interface that facilitates operation.
The program also allows you to import json array files into your persistent [SQLite](https://www.sqlite.org/) database and allows you to export the database table into json array files.**

**🔸 Example of a json array contained in a file.**
```
[
    {
      "city": "Napoli",
      "address" : "Via delle rose 8",
      ...  
    },
    {
      "city": "Roma",
      "address" : "Via dei gerani 9",
      ...  
    }
    ...
]

```
**🔸 To read the data imported in the database created, you could use [sqlitebrowser](https://sqlitebrowser.org/)   
## 📌Built with

<code><img height="30" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"></code>

## 📚 Requirment
- The project requires a python enviroment 3.14 or higher
- [ijson>=3.6.0](https://pypi.org/project/ijson/) - Iterative JSON parser with standard Python iterator interfaces. Supports string literals in JSON.
- [PySimpleGUI>=6.4](https://pypi.org/project/PySimpleGUI/) - Python GUIs for Humans. (free version) Compatible with Python 3.14.
- [pyinstaller>=6.22.3](https://pypi.org/project/pyinstaller/) - PyInstaller bundles a Python application and all its dependencies into a single package.

## 📌Features

It can do a lot of cool things, some of them being:

- Import array file json in new database 
- Import array file json in existing database
- Export data from table on file

## 📌Installation

- First **Fork** this repo by clicking button on top right corner
- Then **Clone** the repo in your local machine
- Navigate to the directory of your project
- Create and activate a new python virtual environment:
  ```
    python -m venv jsontosqlite_env
    source jsontosqlite_env/bin/activate
    ```
  Install all dependency in the requirements file given in **[requirements.txt](https://github.com/MessaGGiero/jsontosqlite/blob/main/requirement.txt)**
- Only for Linux ditribuition Debian/Ubuntu install the package: sudo apt-get install python3-tk
- Run the python script named as ```jsontosqlitegui.py``` which is in Jarvis Directory.
  ```python3 jsontosqlitegui.py```
- Optionally you can follow the steps in the section "📌Executable Windows/linux creation" to create a binary executable that is easier to use


## 📌Executable Windows/Linux creation

- First step open a command shell
- Second step into the project's ./bin directory run the script:
  
    for Windows.
    ```
    compilegui.bat
    ```
    for Linux (install the package python3-tk first:  ```sudo apt-get install python3-tk```)
    ```
    compilegui.sh
    ``` 
   
## 📌Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📌Author

👤 **Massimo Iannuzzi**

- Github: [@MessaGGiero](https://github.com/MessaGGiero)
- LinkedIn: [@massimoiannuzzi](https://www.linkedin.com/in/massimoiannuzzi)

## 📌Show your support

Please ⭐️ this repository if this project helped you!

## 📌License
This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.
