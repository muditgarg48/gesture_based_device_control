from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_project_setup')
def run_project_setup():
    process = subprocess.Popen(['python', 'project_setup.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f"An error occurred: {error.decode()}"
    else:
        return '<br>'.join(output.decode().splitlines())
    
@app.route('/run_integrity_check')
def run_integrity_check():
    process = subprocess.Popen(['python', 'project_integrity_check.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        return f"An error occurred: {error.decode()}"
    else:
        return '<br>'.join(output.decode().splitlines())
    
@app.route('/run_camera_check')
def run_camera_check():
    from scripts.commandline_functions import success, failure
    from scripts.camera_feed_testing import main
    ret_code = main()
    if ret_code == 0:
        return "Camera feed accessibility: " + success()
    else:
        return "Camera feed accessibility: " + failure()

if __name__ == '__main__':
    app.run(debug=True)
