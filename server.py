from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

from scripts.commandline_functions import run_command
result_code = run_command(["python3 --version"])
if result_code == 0:
    python_command = 'python3'
else:
    python_command = 'python'

@app.route('/')
def index():
    from scripts.global_variables.user_specific import USER_DEFINED_GLOBAL_VARS_PROJECT
    return render_template('index.html', global_variables=USER_DEFINED_GLOBAL_VARS_PROJECT)

@app.route('/globalVarsRefresh/')
def refreshGlobalVars():
    from scripts.global_variables.user_specific import USER_DEFINED_GLOBAL_VARS_PROJECT
    data = f"Virtual Environment Name: <i>{USER_DEFINED_GLOBAL_VARS_PROJECT['VIRTUAL_ENV_NAME']}</i><br>Camera Number: <i>{USER_DEFINED_GLOBAL_VARS_PROJECT['CAMERA_NUMBER']}</i><br>Camera Feed Window Name: <i>{USER_DEFINED_GLOBAL_VARS_PROJECT['WINDOW_NAME']}</i><br>Camera Exit Character: '<i>{USER_DEFINED_GLOBAL_VARS_PROJECT['CAMERA_FEED_EXIT_CHAR']}</i>'<br>"
    return data

@app.route('/run_project_setup/')
def run_project_setup():
    process = subprocess.Popen([python_command, 'project_setup.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f"An error occurred: {error.decode()}"
    else:
        return '<br>'.join(output.decode().splitlines())
    
@app.route('/run_integrity_check/')
def run_integrity_check():
    process = subprocess.Popen([python_command, 'project_integrity_check.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f"An error occurred: {error.decode()}"
    else:
        return '<br>'.join(output.decode().splitlines())
    
@app.route('/run_camera_check/')
def run_camera_check():
    from scripts.commandline_functions import success, failure
    from scripts.camera_feed_testing import main
    ret_code = main()
    if ret_code == 0:
        return "Camera feed accessibility: " + success()
    else:
        return "Camera feed accessibility: " + failure()

@app.route('/create_new_scenario/', methods=['POST'])
def create_new_scenario():
    scenario_name = request.form['scenario_name']
    scenario_gestures = request.form['scenario_gestures'].split('\r\n')
    print(scenario_name)
    print(scenario_gestures)
    return "Scenario name and gestures received. Go back to collect training data for this scenario and train an LSTM Neural Network for the same."

if __name__ == '__main__':
    app.run(debug=True)
