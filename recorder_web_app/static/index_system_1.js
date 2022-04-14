// Now here we are going to put all the logics
// The first thing to do is to take data from the select_voice and all_texts field and send it to the backend. 
// In return we are going to get the Number of Unique Words in the text, Number of Takes and Estimated Recording Time.
function analyse() {
	url = '/system_1/get_unique_words'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		document.getElementById("unique_word_count").innerHTML = response_json.unique_word_count;
		document.getElementById("no_of_takes").innerHTML = response_json.no_of_takes;
		document.getElementById("estimated_recording_time").innerHTML = response_json.estimated_recording_time; 
		document.getElementById("total_no_of_takes").innerHTML = "/" + " " + response_json.no_of_takes;  
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	all_texts = document.getElementById("all_texts").value;

 	// Now here we would be putting promts for vacant fields.
 	if (voice == "Select a Voice" || all_texts == "") {
 		alert("Please select a voice and put some texts in respective fields.")
 	}
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
	form_data.append('all_texts', all_texts)

	xhttp.send(form_data)
}

// Now we need to write a funciton to get the texts for each takes.
function get_take_words() {
	url = '/system_1/get_take_words'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);
		
		document.getElementById("take_words").innerHTML = response_json.take_words; 
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	take_no = document.getElementById("take_no").value;

 	// Now here we would be putting promts for vacant fields.
 	if (voice == "Select a Voice" || take_no == "") {
 		alert("Please select a voice and put a take number in respective fields.")
 	}
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('take_no', take_no)

	xhttp.send(form_data)
}

// Now we need to add some functionality for the start recording button.
function start_rec() {
	voice = document.getElementById("select_voice").value;
 	words = document.getElementById("take_words").innerHTML;
 	crop_amp_threshold = document.getElementById("crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("analysis_time_gap").value;

	// Now here we would be putting promts for vacant fields.
 	if (voice == "Select a Voice" || words == "word_0 word_1 word_2 word_3 word_4 word_5 word_6 word_7" || crop_amp_threshold == "Select a Cropping Amp. Threshold" || analysis_time_gap == "Select a Sample Analysis Time Gap") {
 		alert("Please select a voice, get a take, select a Cropping Amp. Threshold and select a Analysis Time Gap in respective fields. The optimal value for Cropping Amp. Threshold is 4 and Analysis Time Gap is 64 if you are using a Studio quality Microphone. In a normal recording set up the optimal values are 16 and 256.")
 		return;
 	}

	// alert('test')
	document.getElementById("rec_animation").style.visibility = "visible";
	document.getElementById("start_rec").style.display = "none";
	document.getElementById("stop_rec").style.display = "inline-block";
	document.getElementById("stop_rec").style.visibility = "visible"

	// Starting the recording process.
	navigator.mediaDevices.getUserMedia({ audio: true })
		.then(stream => {
		    mediaRecorder = new MediaRecorder(stream);

		    // Starts the audio recording proecess.
		    mediaRecorder.start();

		    // Saving the audio data in chunks while recording.
		    const audioChunks = [];

		    mediaRecorder.addEventListener("dataavailable", event => {
		      audioChunks.push(event.data);
		    });

		    // Converting the mdedia recorder object to a blob object with the event listener stop
		    // and then creating an audio url for that blob.
		    mediaRecorder.addEventListener("stop", () => {
		      audioBlob = new Blob(audioChunks, {type: "audio/wav"});
		      audioUrl = URL.createObjectURL(audioBlob);
		    });

	  	});
}

// Now we need to write some functionality for stop recording button.
// This function is very sophisticated to be used.
function stop_rec() {
	// Stopping the Media Recorder.
 	mediaRecorder.stop()

	// Hiding the entire recording components.
	document.getElementById("stop_rec").style.visibility = "hidden";
	document.getElementById("rec_animation").style.visibility = "hidden";
	document.getElementById("please_wait").style.visibility = "visible";

	// Playing the Audio. Before doing anything to the audio, we need to set a Time out so that 
	// it would get some time to do some sort of pre-processing and making ready the audio file.

	// It is important to play the audio after geing recorded instantly so that the user would knwo the take he has just given.
	setTimeout(() => {
     	audio = new Audio(audioUrl);
    	audio.play();
    }, 200);

 	// We don't actually need to play the audio here. Instead we need to send the audio file 
 	// to the server. Here are the codes to send the audio file to the server.
 	url = '/system_1/process_audio'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);
		// alert(response_json.processing_status)
		if (response_json.processing_status == "failed") {
			document.getElementById("please_wait").style.visibility = "hidden";
			document.getElementById("processing_status").innerHTML = "Processing failed. Please try out with different Cropping Amp. Threshold and Analysis Time Gap or use a more noise less microphone.";
			document.getElementById("processing_status").style.color = "#ff4f42";
			document.getElementById("processing_status").style.visibility = "visible";
			document.getElementById("done").style.display = "none";
			document.getElementById("post_operations").style.visibility = "visible";
		};

		if (response_json.processing_status == "success") {
			document.getElementById("please_wait").style.visibility = "hidden";
			document.getElementById("processing_status").innerHTML = "Success . . ! Please listen to all the clips below and verify that all the words have been cropped successfully and click on done. Else do a retake.";
			document.getElementById("processing_status").style.color = "#f58742";
			document.getElementById("processing_status").style.visibility = "visible";
			document.getElementById("done").style.display = "inline-block";
			document.getElementById("post_operations").style.visibility = "visible";
			document.getElementById("word_clips").style.visibility = "visible";
		}
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	words = document.getElementById("take_words").innerHTML;
 	crop_amp_threshold = document.getElementById("crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("analysis_time_gap").value;

 	form_data = new FormData()

 	form_data.append('voice', voice);
 	form_data.append('words', words);
 	form_data.append('crop_amp_threshold', crop_amp_threshold);
 	form_data.append('analysis_time_gap', analysis_time_gap);

 	setTimeout(() => {
 		// Creating an audio file from audio blog. This takes time so in the time_out scope.
     	audio_file = new File([audioBlob], "audio.wav"); 
    }, 200);

    setTimeout(() => {
	 	// Appending the file object to the form data after being created. The creation takes some time. 
		// form_data.append('audio', audio_file);
		form_data.append('audio', audioBlob);
		// alert(audioBlob);
		// Sending the form data after every required elelment is added to the form data.
		xhttp.send(form_data);
    }, 400);
 		
}

// Now we need to write a funciton for retake.
function retake() {
	document.getElementById("post_operations").style.visibility = "hidden";
	document.getElementById("word_clips").style.visibility = "hidden";
	document.getElementById("processing_status").style.visibility = "hidden";
	document.getElementById("stop_rec").style.display = "none";
	document.getElementById("start_rec").style.display = "inline-block";
	document.getElementById("start_rec").style.visibility = "visible";
}

// Now here writing a bunch of functions to play the clip audios.
function clip_0() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_0_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_0_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "0";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function clip_1() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_1_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_1_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "1";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function clip_2() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_2_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_2_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "2";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)	
}

function clip_3() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_3_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_3_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "3";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function clip_4() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_4_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_4_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "4";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function clip_5() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_5_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_5_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "5";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)	
}

function clip_6() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_6_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_6_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "6";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)	
}

function clip_7() {
	url = '/system_1/send_clip_url'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		// Alert word does not exist when the response is failed.
		if (response_json.file_url == "not_available") {
			alert("Word does not exist.");
			return;
		}

		clip_url = response_json.file_url;

		audio = new Audio(clip_url);

	 	audio.onended = function() {
	 		document.getElementById("clip_7_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("clip_7_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	clip_no = "7";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)	
}

// Now writing the function for done.
function done() {
	url = '/system_1/done'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		// response_text = this.responseText;
		// response_json = JSON.parse(response_text);

		document.getElementById("retake").click();
		current_take_no = document.getElementById("take_no").value;
		current_take_no = parseInt(current_take_no)
		document.getElementById("take_no").value = current_take_no + 1;
		document.getElementById("get_take_words").click();
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("select_voice").value;
 	words = document.getElementById("take_words").innerHTML;
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('words', words)

	xhttp.send(form_data)
}

// Now here we need to write a function for testing play.
function testing_play() {
	url = '/system_1/testing_play'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		if (response_json.processing_status == "success") {
			// Here there should be a slight change.
			// In order to get he updated url for creating the Audio object we need to request to a backend endpoint.
			// We are going to give the name of the backend function as get_final_output
			url = '/system_1/get_final_output_url'

		 	xhttp = new XMLHttpRequest();
		 	xhttp.onload = function() {
				response_text = this.responseText;
				response_json = JSON.parse(response_text);
				clip_url = response_json.file_url;

				audio = new Audio(clip_url);

			 	audio.onended = function() {
			 		document.getElementById("testing_play_animation").style.visibility = "hidden";
			 	}

			 	document.getElementById("testing_play_animation").style.visibility = "visible";
				audio.play()
			}

		 	xhttp.open("POST", url);
		 	// Preparing the data
		 	testing_voice = document.getElementById("testing_voice").value;
		 	
		 	form_data = new FormData()
		 	form_data.append('testing_voice', testing_voice)
		 	
			xhttp.send(form_data)
		};

		if (response_json.processing_status == "failed") {
			alert("A few words are not recorded. Please use the Word Concatination Recording Section for recording those words.")
		};
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	testing_voice = document.getElementById("testing_voice").value;
 	testing_words = document.getElementById("testing_words").value;

 	// Now here we would be putting promts for vacant fields.
 	if (testing_voice == "Select a Voice" || testing_words == "") {
 		alert("Please select a voice and put some texts in respective fields.");
 		return;
 	}
 	
 	form_data = new FormData()
 	form_data.append('testing_voice', testing_voice)
 	form_data.append('testing_words', testing_words)

	xhttp.send(form_data)
}

// Here is the function call to the backend to clear all data in the backend generated by app use so that user could start a 
// recording process with a fresh backend folder structure with no previous garbage.  
function reset_backend() {
	url = '/system_1/reset_backend'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		if (response_json.processing_status == 'success') {
			alert('The backend folder structure for System_1 - Word Concatenation has been reset. Now you could start with a fresh backend for your testing.')
		}

	}

 	xhttp.open("POST", url);
 	// No data Preparation neede here.

	xhttp.send()
}

// From here we are going to start working for system_2.
// In system 2 we would be doing class based code organised so that our functions of system 2 would be put together in a class itself
// and it won't create conflict to the system 1 functions. 



