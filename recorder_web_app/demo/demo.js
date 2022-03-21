function test() {
	alert('This is for testing.')
}

// test()

// Now here we are going to put all the logics
// The first thing to do is to take data from the select_voice and all_texts field and send it to the backend. 
// In return we are going to get the Number of Unique Words in the text, Number of Takes and Estimated Recording Time.
function analyse() {
 	let voice = document.getElementById("select_voice").value;
 	let all_texts = document.getElementById("all_texts").value;

 	let url = "/system_1/get_unique_words"
 	// Now it's time to use fetch api to do a post request in an Ajax way to send the data to the backend and put the returned data to the respective html containers.
 	fetch(url)
	.then(data => {
	    // Do some stuff here
	})
	.catch(err => {
	    // Catch and display errors
	})

 	alert(all_texts) 
}

