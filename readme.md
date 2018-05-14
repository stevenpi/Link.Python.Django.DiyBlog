## Setting up the project
The following steps will show you how you can setup the project on your local machine using only the command line. All the commands assume that they will be called from the project folder.

### Download the project
The first thing you obviously should do is to download the project. Either clone it or download the zip file.  

### Install the requirements
For this step you should consider to use a venv (Virutal Environment). `Python3` is required.  
To create a venv using the tool `venv` you first should navigate to the path where the project is stored. Now you can type in:  

```
python3 -m venv venv
```
**NOTE:** The first `venv` is the tool `venv`, the second is the folder `venv`.

This command will create a virtual environment in a new folder called `venv`. To finally use the virtual environment you should use the tool `source`. Type `source` and then provide the path to the `activate` script of the virtual environment.  
Example:  

```
source venv/bin/activate
```

Now you can install the requirements using `pip`. The requirements are in a file called `requirements.txt`. You can use `pip` to install all those requirements by passing the textfile to the `pip` tool.

```
pip install -r requirements.txt
```

After a little loading the requirements are installed.

### Run the project
Before running the project the first time, you should first migrate the database. This can be done with the Python class `manage.py`.
```
python manage.py migrate
```
**NOTE:** This will create a local sqlite3 database which stores your data. 

Now you can run the project using the same class:
```
python manage.py runserver
```

The webapp can now be reached under `localhost:8000`.


## Maintaining the WebApp

### Updating the Index of the Searchengine

The Webapp is using Haystack with the Whoosh backend to provide proper searching functionality.
To get the searchengine to work, the index of the searchengine must be updated regularly.  
This can be done easily with one simple function in manage.py:

```
python manage.py rebuild_index
```  

This commands loads every single entity into the searchindex of the searchengine
