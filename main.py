import os
import webbrowser


def launch_external_controller():
    # create the HTML file with the form
    with open("external_controller.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
	<title>External Controller</title>
</head>
<body>
	<h1>External Controller</h1>
	<p>Please connect to the monitors.</p>
	<button type="button">Connect</button>
	<p>Please select a monitor.</p>
	<input type="radio" id="option1" name="monitor" value="1">
	<label for="option1">1</label><br>
	<input type="radio" id="option2" name="monitor" value="2">
	<label for="option2">2</label><br>
	<input type="radio" id="option3" name="monitor" value="3">
	<label for="option3">3</label><br>
	<br>
	<form action="" method="post">
		<button type="button">Power On</button>
		<button type="button">Power Off</button>
		<br>
		<label for="power-status">Power Command Sent:</label>
		<input type="text" id="power-status" name="power-status">
		<br>
		<br>
		<label for="volume">Volume Control:</label>
		<input type="range" id="volume" name="volume" min="0" max="100" oninput="volumeOutput.value = volume.value">
		<span id="volumeOutput">0</span>
		<br>
		<button type="submit">Set Volume</button>
		<br>
	</form>
	<p>Current Power State:</p>
	<input type="text" id="current-state" name="current-state">
	<script>
		// set the initial value of the volume output
		document.getElementById("volumeOutput").innerHTML = document.getElementById("volume").value;
	</script>
</body>
</html>""")
    # open the HTML file in the default web browser
    webbrowser.open(os.path.abspath("external_controller.html"))


launch_external_controller()
