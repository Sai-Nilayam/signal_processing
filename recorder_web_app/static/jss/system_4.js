// The first thing to do is to put the html content to a the system_4 div.
function system_4_put_html() {
	url = '/static/htmls/system_4.html';
	xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		html_content = this.responseText;
		document.getElementById("system_4").innerHTML = html_content; 
	}
	xhttp.open("GET", url);
	xhttp.send()

}

system_4_put_html()