
// Collapsible functionality

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}


// Initial Project checks

function formatData(data) {
    data = data.replace(//g, "");
    data = data.replaceAll("[1m", "<span style=\"font-weight:bold\">")
    data = data.replaceAll('[3m', '<span style="font-style:italic">')
    data = data.replaceAll('[4m', '<span style="text-decoration:underline">')
    data = data.replaceAll('[31m', '<span style="color:red">')
    data = data.replaceAll('[32m', '<span style="color:green">')
    data = data.replaceAll('[33m', '<span style="color:yellow">')
    data = data.replaceAll('[0m', '</span>')
    return data
}

function runScript(scriptName) {
    document.getElementById('scriptOutput').innerHTML = "Running the script in background ...";
    fetch('/'+scriptName)
        .then(response => response.text())
        .then(data => {
            data = formatData(data)
            document.getElementById('scriptOutput').innerHTML = data;
        });
}

document.getElementById('runSetup').addEventListener('click', function() {
    document.getElementById('scriptHelp').innerHTML = "This might take a while. Thank you for your patience";
    runScript("run_project_setup")
});
document.getElementById('runIntegrityCheck').addEventListener('click', function() {
    document.getElementById('scriptHelp').innerHTML = "This will check for all dependencies and requirements and whether they are accessible by the project or not.";
    runScript("run_integrity_check")
});
document.getElementById('runCameraCheck').addEventListener('click', function() {
    document.getElementById('scriptHelp').innerHTML = "This will attempt to run an instance of the camera feed. Do look out for any popup window with your camera feed.";
    runScript("run_camera_check")
});
document.getElementById('getVariables').addEventListener('click', function() {
  fetch('/globalVarsRefresh').then(response => response.text()).then(data => {
    document.getElementById('varDisplay').innerHTML = data;
  })
});