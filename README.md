# GESTURE RECOGNITION-BASED DEVICE CONTROL

## INTRODUCTION 

description

###### Note: The project was developed with Python v3.11.5 and Pip version 24.0. 

## INDEX

#### PROJECT SETUP [here](#project-setup)

#### FILES AND FOLDERS DESCRIPTION [here](#files-and-folders-descriptions)

- [project_setup.py](#project_setuppy)
- [project_integrity_check.py](#project_integrity_checkpy)
- [requirements.txt](#requirementstxt)

#### data/

This folder contains all the necessary data required by the project to run

- [models/](#datamodels)
- [training_action_data/](#datatraining-action-data)
- [available_gestures.npy](#dataavailable_gesturesnpy)

#### global_variables/ [here](#global_variables)

This folder includes all the global variables used by various scripts within the project

#### my-project-env/ [here](#my-project-env)

This folder denotes the virtual environment of the project. This is usually generated for the user by the _project_setup.py_ script when the user runs it for the first time after cloning the repository.

#### scripts/

This folder contains all the scripts required to do various tasks. Particular care has been taken to name them to describe their purpose. A more detailed explanation is also present in this README. 

###### Note:

Remember to run the scripts from within the folder as they are configured to find the relative path that way. Running them from another location might affect the scripts' ability to search for necessary files and folders.

- [camera_feed_testing.py](#scriptscamera_feed_testingpy)
- [commandline_functions.py](#scriptscommandline_functionspy)
- [dataset_functions.py](#scriptsdataset_functionspy)
- [gestures_functons.py](#scriptsgesture_functionspy)
- [mediapipe_functions.py](#scriptsmediapipe_functionspy)
- [model_functions.py](#scriptsmodel_functionspy)
- [tensorboard_training_monitor.py](#scriptstensorboard_training_monitorpy)

#### tensorboard-logs/ [here](#tensorboard_logs)

This folder contains all the files necessary for Tensorboard.

## PROJECT SETUP

This project involves a lot of moving parts but fear not. The project also includes several Python scripts to ensure the user doesn't have to set up anything manually if those scripts are run before starting the project.

Follow the following steps to set the project suitable for running:

1. Download Python from [here](https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe) and install it. 
    * Ensure that it is added to the environment variables. 
    * The Python setup has an option to check if you want the setup to directly add Python to the environment variables.
    * Mediapipe, a Google-developed library used in this project, requires:
        - Python version 3.8 to 3.11
        - Pip version 20.3+

2. Run the _project_setup.py_ script by either one of these commands in the terminal:
    ```
    python project_script.py
    ```
    (or)
    ```
    python3 project_script.py
    ```

3. Activate the virtual environment using this command in the terminal. Note, that the quotation marks (" ") are necessary because the command is running the virtual environment activation script in another folder directly without traversing to it.
    
    For Windows:
    ```
    "{name of virtual env}/Scripts/activate.bat"
    ```
    
    For other OS:
    ```
    "{name of virtual env}/Scripts/activate"
    ```

4. Run _project_integrity_check.py_ script to check the health of the project workspace and if it is ready to run the project, by either one of these commands in the terminal:
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
4. Checks for the availability of _venv_ Python package for creating and usage of a virtual environment for this project. It is installed using the following command globally if not found: 
    ```
    pip install venv
    ```
5. Checks for the presence of the project's virtual environment. The default name of this project's virtual environment is _"my-project-env"_ and the name is stored in the _global_variables.py_ for every script to access. 
    * If the script doesn't find the virtual environment it was looking for, it creates the virtual environment and activates it using:
        ```
        python -m venv {name of virtual env}
        ```

6. Check if the virtual environment is active or not. If yes, proceed to the next step. Else, it activates the virtual environment using:

    For Windows:
    ```
    "{name of virtual env}/Scripts/activate.bat"
    ```
    
    For other OS:
    ```
    "{name of virtual env}/Scripts/activate"
    ```

###### Note: The quotation marks (" ") are necessary because the command is running the virtual environment activation script in another folder directly without traversing to it.

7. Once the virtual environment is created and activated, it installs all the dependencies for the project using Pip and _requirements.txt_ using:
    ```
    pip install -r requirements.txt
    ```

8. Once all the steps are completed, the script adds the project's virtual environment in the list of compatible kernels for the main Jupyter Notebook to use.

###### Note: 

* The virtual environment is only activated for the duration of the script to install the dependencies. Please reactivate the virtual environment using the aforementioned command (also mentioned at the end of the execution of this script) if you intend to run the project through the terminal.
* Remember to change the kernel for the Jupyter Notebook to the project's virtual environment. The option is available at the top right corner for Visual Studio Code once you open the notebook.

#### project_integrity_check.py

The _project_integrity_check.py_ script checks if the project workspace is ready before successfully running the project. Please ensure to run it after running _project_setup.py_ and activating the virtual environment first to ensure that the project will not have a setup issue during execution. The steps included in this file are:

1. Check Python version >=3.9 or <=3.11
2. Check the availability of the virtual environment and if it is activated.
3. Check if all the necessary packages are accessible by the project.
4. Check if the camera feed is accessible by the OpenCV library for the project.

###### Note: 
This script does not perform any task but only is responsible for doing checks. Run the _project_setup.py_ script again to redo the setup process if any checks fail.

#### requirements.txt

The _requirements.txt_ file contains all the dependencies that are required by this project to run successfully. This file is auto-generated using Pip by the following command:
```
pip freeze > requirements.txt
```

#### .gitignore

The _.gitignore_ file has been custom-created for this project to add all the files and folders that do not need to be tracked by Git. These include:
- The training data folder
- The virtual environment folder
- The Python cache
- The Pip installation Python script which is downloaded if the user doesn't have Pip

#### data/models/

The _models_ folder is intended to be the one-stop folder to save all the models that will be trained during the development of the project.

#### data/training-action-data/

The _training-action-data_ folder is intended to store all the videos broken down into frames stored in NumPy arrays that will be used to train the model for recognizing gestures stored in the _available_gestures.npy_

#### data/available_gestures.npy

The _available_gestures.npy_ file is the stored version of a Numpy array which stores all the gestures compatible with the project.

#### global_variables/

The _global_variables_ folder contains all the necessary global variables in one place that are necessary for the project to run. There are two types of global variables in this folder,
    - _fixed.py_ are the ones that need to be fixed and should be not touched
    - _user_specific.py_ are the ones that are flexible for the user to change according to his needs

###### Note: Be very careful while modifying contents of _user_specific.py_ file. Unnecessary alterations not according to the default values of this file might break the project.

#### /my-project-env

The default virtual environment folder which stores all the packages locally which are required by the project without globally installing them in your system and slowing it down. To activate it, go to the Scripts folder inside it and run _activate.bat_ (for Windows) or _activate_ (for others)

#### scripts/camera_feed_testing.py

The _camera_feed_testing.py_ python script is used to test if the project can open up the camera in the user's system and access the camera feed.

#### scripts/commandline_functions.py

The _commandline_functions.py_ python file only contains some functions that help other scripts during their execution in the command line.

#### scripts/dataset_functions.py

The _dataset_functions.py_ python scripts contain all the necessary functions required for various actions related to the datasets stored in this project for training the models. The script runs in an infinite loop to ask for which function you want to perform by a switch case till you stop it. These include:

* Print the dataset details which include:
    - The gestures included
    - The number of video folders present in the dataset available to train

* Add onto the already present dataset and if not present, create one
* Completely clean and erase the _training_action_data_ folder with _data_ folder

#### scripts/gesture_functions.py

The _gesture_functions.py_ python scripts contain all the necessary functions required for various actions related to the list of gestures compatible with this project for recognition. The script runs in an infinite loop to ask for which function you want to perform by a switch case till you stop it. These include:

* Reset the compatible gesture list to
    - Toggle Lights
    - Increase their brightness
    - Decrease their brightness

* Load gestures from _available_gestures.npy_
* Save the modified gesture list back to _available_gestures.npy_
* Show available gestures stored in _available_gestures.npy_
* Add a gesture to _available_gestures.npy_ list.

#### scripts/mediapipe_functions.py

The _mediapipe_functions.py_ python script contains all the necessary functions developed using Mediapipe by Google to recognize key points in both hands and draw them on the receiving camera feed.

#### scripts/model_functions.py

The _model_functions_ python scripts contain all the necessary functions required for various actions related to the models created within this project for gesture recognition. The script runs in an infinite loop to ask for which function you want to perform by a switch case till you stop it. These include:

* Print the list of all the pretrained models present in the storage
* Train a new model based on the dataset present in the _data/training_action_data/_
* Test an existing model from the _data/training_action_data/_

#### scripts/tensorboard_training_monitor.py

The _tensorboard_training_monitor.py_ Python script is responsible for activating the Tensorboard which is an interactive and useful dashboard that shows all the stats while training of the model.

###### Note: This script should be run before starting the training of the model.

#### tensorboard_logs/

The _tensorboard_logs_ folder contains the autogenerated files by Tensorboard to monitor the training of any model using Tensorflow. These files are utilised by the _tensorboard_training_monitor.py_ python script in _scripts/_ folder to launch an interactive web application to monitor the training of the model.
