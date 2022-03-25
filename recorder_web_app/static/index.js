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
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('take_no', take_no)

	xhttp.send(form_data)
}

// Now we need to add some functionality for the start recording button.
function start_rec() {
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
		      audioBlob = new Blob(audioChunks, {type: "audio/ogg"});
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
			document.getElementById("processing_status").innerHTML = "Processing failed. Please try out with different Cropping Amp. Thresholds or use a more noise less microphone.";
			document.getElementById("processing_status").style.color = "#ff4f42";
			document.getElementById("processing_status").style.visibility = "visible";
			document.getElementById("done").style.display = "none";
			document.getElementById("post_operations").style.visibility = "visible";
		};

		if (response_json.processing_status == "success") {
			document.getElementById("please_wait").style.visibility = "hidden";
			document.getElementById("processing_status").innerHTML = "Success . . !";
			document.getElementById("processing_status").style.color = "#00c76a";
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

 	form_data = new FormData()

 	form_data.append('voice', voice);
 	form_data.append('words', words);
 	form_data.append('crop_amp_threshold', crop_amp_threshold);

 	setTimeout(() => {
 		// Creating an audio file from audio blog. This takes time so in the time_out scope.
     	audio_file = new File([audioBlob], "audio.mp3"); 
    }, 200);

    setTimeout(() => {
	 	// Appending the file object to the form data after being created. The creation takes some time. 
		form_data.append('audio', audio_file);
		// Sending the form data after every required elelment is added to the form data.
		xhttp.send(form_data)
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
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/0.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_0_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_0_animation").style.visibility = "visible";
	audio.play()	
}

function clip_1() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/1.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_1_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_1_animation").style.visibility = "visible";
	audio.play()	
}

function clip_2() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/2.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_2_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_2_animation").style.visibility = "visible";
	audio.play()	
}

function clip_3() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/3.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_3_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_3_animation").style.visibility = "visible";
	audio.play()	
}

function clip_4() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/4.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_4_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_4_animation").style.visibility = "visible";
	audio.play()	
}

function clip_5() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/5.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_5_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_5_animation").style.visibility = "visible";
	audio.play()	
}

function clip_6() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/6.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_6_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_6_animation").style.visibility = "visible";
	audio.play()	
}

function clip_7() {
	clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/inst_words/7.wav"
 	audio = new Audio(clip_url);

 	audio.onended = function() {
 		document.getElementById("clip_7_animation").style.visibility = "hidden";
 	}

 	document.getElementById("clip_7_animation").style.visibility = "visible";
	audio.play()	
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
			clip_url = "http://127.0.0.1:8000/static/system_1/voice_0_0/testing_words/final_output.wav"
		 	audio = new Audio(clip_url);

		 	audio.onended = function() {
		 		document.getElementById("testing_play_animation").style.visibility = "hidden";
		 	}

		 	document.getElementById("testing_play_animation").style.visibility = "visible";
			audio.play()	
		};

		if (response_json.processing_status == "failed") {
			alert("A few words are not recorded. Please use the Word Concatination Recording Section for recording those words.")
		};
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	testing_voice = document.getElementById("testing_voice").value;
 	testing_words = document.getElementById("testing_words").value;
 	
 	form_data = new FormData()
 	form_data.append('testing_voice', testing_voice)
 	form_data.append('testing_words', testing_words)

	xhttp.send(form_data)
}


