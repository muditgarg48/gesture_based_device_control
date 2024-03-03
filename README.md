# GESTURE RECOGNITION BASED DEVICE CONTROL

## INTRODUCTION 

description

###### Note: The project was developed with Python v3.11.5 and Pip version 24.0. 


## PROJECT SETUP

This project involves a lot of moving parts but fear not. The project also includes several Python scripts to make sure you dont have to setup anything manually if those scripts are run before starting the project.

Follow the following steps to setup the project suitable for running:

1. Download Python from [here](https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe) and install it. 
    * Ensure that it is added to the environment variables. 
    * The python setup has an option to check if you want the setup to directly add Python to the environment variables.
    * Mediapipe, a Google developed library used in this project, requires:
        - Python version 3.8 to 3.11
        - Pip version 20.3+

2. Run _project_setup.py_ script by either one of this command in the terminal:
    ```
    python project_script.py
    ```
    (or)
    ```
    python3 project_script.py
    ```

3. Activate the virtual environment using this command in the terminal. Note, the quotation marks (" ") are necessary because the command is running the virtual environment activatation script in another folder directly without traversing to it.
    
    For Windows:
    ```
    "{name of virtual env}/Scripts/activate.bat"
    ```
    
    For other OS:
    ```
    "{name of virtual env}/Scripts/activate"
    ```

4. Run _project_integrity_check.py_ script to check the health of the project workspace and if it is ready to run the project, by either one of this command in the terminal:
    ```
    python project_integrity_check.py
    ```
    (or)
    ```
    python3 project_script.py
    ```


## FILES and FOLDERS DESCRIPTIONS

#### project_setup.py

The _project_setup.py_ script handles all the project setup steps that are required before successfully running the script. Please ensure to run it first after cloning this repository to ensure all the dependencies are satisfied. The steps included in this file are:

1. Checks for Python >=3.9 or <=3.11.
2. Checks for the availability of _requirements.txt_ file to get the list of all the dependencies of this project.
3. Checks for Pip installation. It downloads and installs Pip if not found. The link used by the script to download pip is [this](https://bootstrap.pypa.io/get-pip.py).
4. Checks for the availability of _venv_ Python package for creating and usage of virtual environment for this project. It is installed using the following command globally if not found: 
    ```
    pip install venv
    ```
5. Checks for the presence of the project's virtual environment. The default name of this project's virtual environment is _"my-project-env"_ and the name is stored in the _global_variables.py_ for every script to access. 
    * If the script doesn't find the virtual environment it was looking for, it creates the virtual environment and activates it using:
        ```
        python -m venv {name of virtual env}
        ```

6. Checks if the virtual environment is active or not. If yes, proceed to the next step. Else, it activates the virtual environment using:

    For Windows:
    ```
    "{name of virtual env}/Scripts/activate.bat"
    ```
    
    For other OS:
    ```
    "{name of virtual env}/Scripts/activate"
    ```

###### Note: The quotation marks (" ") are necessary because the command is running the virtual environment activatation script in another folder directly without traversing to it.

7. Once the virtual environment is created and activated, it installs all the dependencies for the project using Pip and _requirements.txt_ using:
    ```
    pip install -r requirements.txt
    ```

8. Once all the steps are completed, the script adds the project's virtual environment in the list of compatible kernels for the main Jupyter notebook to use.

###### Note: 

* The virtual environment is only activated for the duration of the script to install the dependencies. Please reactivate the virtual environment using the aforementioned command (also mentioned at the end of execution of this script) if you intend to run the project through the terminal.
* Remember to change the kernel for the Jupyter notebook to the project's virtual environment. The option is available at the top right corner for Visual Studio Code once you open the notebook.

#### project_integrity_check.py

The _project_integrity_check.py_ script checks if the project workspace is ready before successfully running the project. Please ensure to run it after running _project_setup.py_ and activating the virtual environment first to ensure that the project will not have a setup issue during execution. The steps included in this file are:

1. Check Python version >=3.9 or <=3.11
2. Check the availability of the virtual environment and if it is activated.
3. Checks if all the necessary packages are accessible by the project.
4. Checks if the camera feed is accessible by the OpenCV library for the project.

###### Note: 
This script does not perform any task but only is responsible for doing checks. Run the _project_setup.py_ script again to redo the setup process if any checks fail.

#### commandline_functions.py

The _commandline_functions.py_ python file only contains some functions that help other scripts during their execution in the command line.

#### global_variables.py

The _global_variable.py_ python file contains all the necessary global variables in one place that are necessary for the project to run. There are two types of global variables in this file,
    - the ones which need to be fixed and should be not touched
    - the ones which are flexible for the user to change according to his needs

###### Note: Be very careful while modifying contents of this file. Unnecessary alterations to this file might break the project.

#### requirements.txt

The _requirements.txt_ file contains all the dependencies that are required by this project to run successfully. This file is auto generated using Pip by the following command:
```
pip freeze > requirements.txt
```

#### gesture_functions.py

The _gesture_functions.py_ python scripts contains all the necessary functions required for various actions related to the list of gestures compatible by this project for recognition. The script runs in an infinite loop to ask for which function you want to perform by a switch case till you stop it. These include:

* Reset the compatible gesture list to
    - Toggle Lights
    - Increase their brightness
    - Decrease their brightness

* Load gestures from _available_gestures.npy_
* Save the modified gesture list back to _available_gestures.npy_
* Show available gestures stored in _available_gestures.npy_
* Add a gesture to _available_gestures.npy_ list.

#### available_gestures.npy

The _available_gestures.npy_ file is the stored version of a Numpy array which stores all the gestures compatible by the project.

#### tensorboard_training_monitor.py

The _tensorboard_training_monitor.py_ Python script is responsible for activating the Tensorboard which is a interactive and useful dashboard that shows all the stats while training of the model.

###### Note: This script should only be run when training the model or else it might break.

#### .gitignore

The _.gitignore_ file has been custom created for this project to add all the files and folders that do not need to be tracked by Git. These include:
- The training data folder
- The virtual environment folder
- The Python cache
- The Pip installation python script which is downloaded if the user doesn't have Pip

#### /my-project-env

The default virtual environment folder which stores all the packages locally which are required by the project without globally installing them in your system and slowing it down. To activate it, go to the Scripts folder inside it and run _activate.bat_ (for Windows) or _activate_ (for others)

#### /models

The _models_ folder is intended to be the one stop folder to save all the models that will be trained during the development of the project.

#### /training-action-data

The _training-action-data_ folder is intended to store all the videos broken down into frames that will be used to train the model for recognising gestures stored in the _available_gestures.npy_

