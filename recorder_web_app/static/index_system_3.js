// Testing
// function test() {
// 	alert("test")
// }

// test()

// We will start our logic from here. 
// Gobal variables
demo_clip_selected = false;

// The first thing to do here is to grab the file as soon as the file selection event takes place. 
function grab_audio_url(event) {
	demo_clip_url = URL.createObjectURL(event.target.files[0]);
	demo_clip_selected = true;
	// alert(demo_clip_url);
}

// For Playing the demo clip.
function system_3_play_demo_clip() {
	// Check if the demo clip has been selected or not. 
	if (demo_clip_selected == false) {
		alert("Please select a demo audio clip.");
		return;
	}

	document.getElementById("system_3_demo_clip_animation").style.visibility = "visible";
	audio = new Audio(demo_clip_url);
	audio.onended = function() {
	 		document.getElementById("system_3_demo_clip_animation").style.visibility = "hidden";
	 	}
	audio.play();	
}

// For getting different take characters
function system_3_get_take_sv() {
	voice = document.getElementById("system_3_select_voice").value;
	take_no = document.getElementById("system_3_take_no").value;

	if (voice == "Select a Voice" || take_no == "") {
		alert("Please select a voice and put a take number in respective fields.");
		return;
	}

	if (take_no == 0) {
		take_sv = "a a a";
	} else if (take_no == 1) {
		take_sv = "aa aa aa";
	} else if (take_no == 2) {
		take_sv = "i i i";
	} else if (take_no == 3) {
		take_sv = "u u u";
	} else if (take_no == 4) {
		take_sv = "e e e";
	} else if (take_no == 5) {
		take_sv = "o o o";
	}

	document.getElementById("system_3_take_characters").innerHTML = take_sv;
}

// Now write a function for start recording that will record the audio. 
function system_3_start_rec() {
	voice = document.getElementById("system_3_select_voice").value;
 	characters = document.getElementById("system_3_take_characters").innerText;
 	crop_amp_threshold = document.getElementById("system_3_crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("system_3_analysis_time_gap").value;
 	fine_analysis_time_gap = document.getElementById("system_3_fine_analysis_time_gap").value;

	// Now here we would be putting promts for vacant fields.
 	if (voice == "Select a Voice" || characters == "- - -" || crop_amp_threshold == "Select a Cropping Amp. Threshold" || analysis_time_gap == "Select a Sample Analysis Time Gap" || fine_analysis_time_gap == "Select a Fine Analysis Time Gap") {
 		alert("Please select a voice, get a take, select a Cropping Amp. Threshold and select a Analysis Time Gap in respective fields. The optimal value for Cropping Amp. Threshold is 4 and Analysis Time Gap is 64 if you are using a Studio quality Microphone. In a normal recording set up the optimal values are 16 and 256.")
 		return;
 	}

	// alert('test')
	document.getElementById("system_3_rec_animation").style.visibility = "visible";
	document.getElementById("system_3_start_rec").style.display = "none";
	document.getElementById("system_3_stop_rec").style.display = "inline-block";
	document.getElementById("system_3_stop_rec").style.visibility = "visible"

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

// For stopping the recording.
function system_3_stop_rec() {
	// Stopping the Media Recorder.
 	mediaRecorder.stop()

	// Hiding the entire recording components.
	document.getElementById("system_3_stop_rec").style.visibility = "hidden";
	document.getElementById("system_3_rec_animation").style.visibility = "hidden";
	document.getElementById("system_3_please_wait").style.visibility = "visible";

	// Playing the Audio. Before doing anything to the audio, we need to set a Time out so that 
	// it would get some time to do some sort of pre-processing and making ready the audio file.

	// It is important to play the audio after geing recorded instantly so that the user would knwo the take he has just given.
	setTimeout(() => {
     	audio = new Audio(audioUrl);
    	audio.play();
    }, 200);

 	// We don't actually need to play the audio here. Instead we need to send the audio file 
 	// to the server. Here are the codes to send the audio file to the server.
 	url = '/system_3/process_audio'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);
		// alert(response_json.processing_status)
		if (response_json.processing_status == "failed") {
			document.getElementById("system_3_please_wait").style.visibility = "hidden";
			document.getElementById("system_3_processing_status").innerHTML = "Processing failed. Please try out with different Cropping Amp. Threshold and Analysis Time Gap or use a more noise less microphone.";
			document.getElementById("system_3_processing_status").style.color = "#ff4f42";
			document.getElementById("system_3_processing_status").style.visibility = "visible";
			document.getElementById("system_3_done").style.display = "none";
			document.getElementById("system_3_post_operations").style.visibility = "visible";
		};

		if (response_json.processing_status == "success") {
			document.getElementById("system_3_please_wait").style.visibility = "hidden";
			document.getElementById("system_3_processing_status").innerHTML = "Success . . ! Please listen to all the clips below and verify that all the Swaravarna character sounds have been cropped successfully and click on done. Else do a retake.";
			document.getElementById("system_3_processing_status").style.color = "#f58742";
			document.getElementById("system_3_processing_status").style.visibility = "visible";
			document.getElementById("system_3_done").style.display = "inline-block";
			document.getElementById("system_3_post_operations").style.visibility = "visible";
			document.getElementById("system_3_word_clips").style.visibility = "visible";
		}
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("system_3_select_voice").value;
 	characters = document.getElementById("system_3_take_characters").innerText;
 	crop_amp_threshold = document.getElementById("system_3_crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("system_3_analysis_time_gap").value;
 	fine_analysis_time_gap = document.getElementById("system_3_fine_analysis_time_gap").value;

 	form_data = new FormData()

 	form_data.append('voice', voice);
 	form_data.append('characters', characters);
 	form_data.append('crop_amp_threshold', crop_amp_threshold);
 	form_data.append('analysis_time_gap', analysis_time_gap);
 	form_data.append('fine_analysis_time_gap', fine_analysis_time_gap);

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
function system_3_retake() {
	document.getElementById("system_3_post_operations").style.visibility = "hidden";
	document.getElementById("system_3_word_clips").style.visibility = "hidden";
	document.getElementById("system_3_processing_status").style.visibility = "hidden";
	document.getElementById("system_3_stop_rec").style.display = "none";
	document.getElementById("system_3_start_rec").style.display = "inline-block";
	document.getElementById("system_3_start_rec").style.visibility = "visible";
}

// Now here writing a bunch of functions to play the clip audios.
function system_3_clip_0() {
	url = '/system_3/send_clip_url'

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
	 		document.getElementById("system_3_clip_0_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("system_3_clip_0_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("system_3_select_voice").value;
 	clip_no = "0";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function system_3_clip_1() {
	url = '/system_3/send_clip_url'

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
	 		document.getElementById("system_3_clip_1_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("system_3_clip_1_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("system_3_select_voice").value;
 	clip_no = "1";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

function system_3_clip_2() {
	url = '/system_3/send_clip_url'

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
	 		document.getElementById("system_3_clip_2_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("system_3_clip_2_animation").style.visibility = "visible";
		audio.play()
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("system_3_select_voice").value;
 	clip_no = "2";
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('clip_no', clip_no)
 	
	xhttp.send(form_data)
}

// Now writing the function for done.
function system_3_done() {
	url = '/system_3/done'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		// response_text = this.responseText;
		// response_json = JSON.parse(response_text);

		document.getElementById("system_3_retake").click();
		current_take_no = document.getElementById("system_3_take_no").value;
		current_take_no = parseInt(current_take_no)
		document.getElementById("system_3_take_no").value = current_take_no + 1;
		document.getElementById("system_3_get_take_sv").click();
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	voice = document.getElementById("system_3_select_voice").value;
 	characters = document.getElementById("system_3_take_characters").innerHTML;
 	
 	form_data = new FormData()
 	form_data.append('voice', voice)
 	form_data.append('characters', characters)

	xhttp.send(form_data)
}

// Now writing a function for testing play.
function system_3_testing_play() {
	url = '/system_3/testing_play'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		if (response_json.processing_status == "success") {
			// Here there should be a slight change.
			// In order to get he updated url for creating the Audio object we need to request to a backend endpoint.
			// We are going to give the name of the backend function as get_final_output
			url = '/system_3/get_final_output_url'

		 	xhttp = new XMLHttpRequest();
		 	xhttp.onload = function() {
				response_text = this.responseText;
				response_json = JSON.parse(response_text);
				clip_url = response_json.file_url;

				audio = new Audio(clip_url);

			 	audio.onended = function() {
			 		document.getElementById("system_3_testing_play_animation").style.visibility = "hidden";
			 	}

			 	document.getElementById("system_3_testing_play_animation").style.visibility = "visible";
				audio.play()
			}

		 	xhttp.open("POST", url);
		 	// Preparing the data
		 	testing_voice = document.getElementById("system_3_testing_voice").value;
		 	
		 	form_data = new FormData()
		 	form_data.append('testing_voice', testing_voice)
		 	
			xhttp.send(form_data)
		};

		if (response_json.processing_status == "failed") {
			alert("A few Swaravarna or Vyanjana Varna Sounds are not recorded. Please use the Vocal Tone and Style Transfer Recording Section for recording Swara Varna sounds. For Vyanja Varna sounds upload them in the Name Entity Pronunciaiton Alternate module.")
		};
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	vv_set = document.getElementById("system_3_vv_set_test").value;
 	testing_voice = document.getElementById("system_3_testing_voice").value;
 	testing_characters = document.getElementById("system_3_testing_characters").value;

 	// Now here we would be putting promts for vacant fields.
 	if (testing_voice == "Select a Voice" || testing_characters == "" || vv_set == "Select a Vyanjana Varna Set") {
 		alert("Please select a Vyanja Varna Set, Voice and put some texts in respective fields.");
 		return;
 	}
 	
 	form_data = new FormData()
 	form_data.append('vv_set', vv_set)
 	form_data.append('testing_voice', testing_voice)
 	form_data.append('testing_characters', testing_characters)

	xhttp.send(form_data)
}

// Writing a function to reset backend.
function system_3_reset_backend() {
	url = '/system_3/reset_backend'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		if (response_json.processing_status == 'success') {
			alert('The backend folder structure for System_3 - Vocal Tone and Style Transfer has been reset. Now you could start with a fresh backend for your testing.')
		}

	}

 	xhttp.open("POST", url);
 	// No data Preparation neede here.

	xhttp.send()
}
