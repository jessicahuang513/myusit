function loadAnalystDocument() {
	var files = [{{ ', '.join(URLs) }}]
	var selectedFileIndex = document.getElementById('analystGroupFileSelect').selectedIndex
	document.getElementById('analystGroupFile').src = files[selectedFileIndex]
}