function test() {
	alert('This is for testing.')
}

// test()

// Now here we are going to put all the logics
// The first thing to do is to take data from the select_voice and all_texts field and send it to the backend. 
// In return we are going to get the Number of Unique Words in the text, Number of Takes and Estimated Recording Time.
function analyse() {
	url = '/system_1/get_unique_words'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		document.getElementById("unique_word_count").innerHTML = this.responseText;       
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	all_texts = document.getElementById("all_texts").value;
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
	form_data.append('all_texts', all_texts)

	xhttp.send(form_data)

 	// alert(all_texts);
}

