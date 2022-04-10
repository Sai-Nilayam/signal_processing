// Now here we are going to write the logic for System 2.
// Testing.
// function test() {
// 	alert("test");
// }

// test()

is_on_metronome = false;

// Writing out the function for Play Metronome.
function system_2_play_metronome() {
	// Make is on metronome to True first.
	is_on_metronome = true;

	// First we will make the Play Metrronome button invisible and Stop metronome button visible.
	document.getElementById("system_2_play_metronome").style.display = "none";
	document.getElementById("system_2_stop_metronome").style.display = "inline-block";

	// Now before doing anything, we need to get the sounds of the metronome to play it here.
	tik = new Audio('/static/metronome_sounds/tik.wav');
	tok = new Audio('/static/metronome_sounds/tok.wav');

	// From here the codes start for 
	tik.play();
	document.getElementById("tik_1").style.color = "#008cff";
	document.getElementById("metronome_number").innerHTML = "1";
	
	setTimeout(
		function() {
			tok.play();
			document.getElementById("tik_1").style.color = "#ededed";
			document.getElementById("tik_2").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "2";
		}, 500);

	setTimeout(
		function() {
			tok.play();
			document.getElementById("tik_2").style.color = "#ededed";
			document.getElementById("tik_3").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "3";
		}, 1000);

	setTimeout(
		function() {
			tok.play();
			document.getElementById("tik_3").style.color = "#ededed";
			document.getElementById("tik_4").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "4";
		}, 1500);

	metronomeInterval = setInterval(
		function() {
			tik.play()
			document.getElementById("tik_4").style.color = "#ededed";
			document.getElementById("tik_1").style.color = "#008cff";
			document.getElementById("metronome_number").innerHTML = "1";
			setTimeout(
				function() {
					tok.play();
					document.getElementById("tik_1").style.color = "#ededed";
					document.getElementById("tik_2").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "2";
				}, 500);
			setTimeout(
				function() {
					tok.play();
					document.getElementById("tik_2").style.color = "#ededed";
					document.getElementById("tik_3").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "3";
				}, 1000);

			setTimeout(
				function() {
					tok.play();
					document.getElementById("tik_3").style.color = "#ededed";
					document.getElementById("tik_4").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "4";
				}, 1500);
		}, 2000)
}

// Writing out the function for stop metronome.
function system_2_stop_metronome() {
	// Make is_on_metronome to False frist.
	is_on_metronome = false;

	// Clearing out the metronome loop.
	clearInterval(metronomeInterval);
	setTimeout(function() {
		document.getElementById("tik_4").style.color = "#ededed";
		document.getElementById("metronome_number").innerHTML = "0";
	} , 2000)
	document.getElementById("system_2_stop_metronome").style.display = "none";
	document.getElementById("system_2_play_metronome").style.display = "inline-block";
}

// For tunring off the metronome sound.
function system_2_on_metronome_sound() {
	alert("Turning off metronome sound is not allowed as that could create problems in rythm making while doing recorings. It's reccommeded to use metronome sound while doing the recoridng. Listen to the sound with earphone or headphone and record via a different microphone such that the metronome sound won't record back.")
}

// Now it's time to write the funciton for starting the recoridng. 
function system_2_start_recording() {
	characters = document.getElementById("system_2_characters").innerText;
 	crop_amp_threshold = document.getElementById("system_2_crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("system_2_analysis_time_gap").value;

 	// Now here we would be putting promts for vacant fields.
 	// if (is_on_metronome == false || crop_amp_threshold == "Select a Cropping Amp. Threshold" || analysis_time_gap == "Select a Sample Analysis Time Gap") {
 	// 	alert("Please select a Cropping Amp. Threshold and select an Analysis Time Gap in respective fields. The optimal value for Cropping Amp. Threshold is 4 and Analysis Time Gap is 64 if you are using a Studio quality Microphone. In a normal recording set up the optimal values are 16 and 128. Also turn on the metronome before doing any recording as it's important to utter the charcter chunks on the metronome rythm.")
 	// 	return;
 	// }

 	document.getElementById("system_2_recording_animation").style.visibility = "visible";
	document.getElementById("system_2_start_recording").style.display = "none";
	document.getElementById("system_2_stop_recording").style.display = "inline-block";
	document.getElementById("system_2_stop_recording").style.visibility = "visible"

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

// Writing a funciton for stop recording.
function system_2_stop_recording() {
	// Stopping the Media Recorder.
 	mediaRecorder.stop()

	// Hiding the entire recording components.
	document.getElementById("system_2_stop_recording").style.visibility = "hidden";
	document.getElementById("system_2_recording_animation").style.visibility = "hidden";
	document.getElementById("system_2_please_wait").style.visibility = "visible";

	// Playing the Audio. Before doing anything to the audio, we need to set a Time out so that 
	// it would get some time to do some sort of pre-processing and making ready the audio file.

	// It is important to play the audio after geing recorded instantly so that the user would knwo the take he has just given.
	setTimeout(() => {
     	audio = new Audio(audioUrl);
    	audio.play();
    }, 200);

 	// We don't actually need to play the audio here. Instead we need to send the audio file 
 	// to the server. Here are the codes to send the audio file to the server.
 	url = '/system_2/process_audio'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);
		// alert(response_json.processing_status)
		if (response_json.processing_status == "failed") {
			document.getElementById("system_2_please_wait").style.visibility = "hidden";
			document.getElementById("system_2_processing_status").innerHTML = "Processing failed. Please try out with different Cropping Amp. Threshold and Analysis Time Gap or use a more noise less microphone.";
			document.getElementById("system_2_processing_status").style.color = "#ff4f42";
			document.getElementById("system_2_processing_status").style.visibility = "visible";
			document.getElementById("system_2_done").style.display = "none";
			document.getElementById("system_2_post_operations").style.visibility = "visible";
		};

		if (response_json.processing_status == "success") {
			document.getElementById("system_2_please_wait").style.visibility = "hidden";
			document.getElementById("system_2_processing_status").innerHTML = "Success . . ! Please listen to the clip below and verify that all the character sound chunks have been processed successfully and click on done. Else do a retake.";
			document.getElementById("system_2_processing_status").style.color = "#f58742";
			document.getElementById("system_2_processing_status").style.visibility = "visible";
			document.getElementById("system_2_done").style.display = "inline-block";
			document.getElementById("system_2_post_operations").style.visibility = "visible";
			document.getElementById("system_2_audio_clip").style.visibility = "visible";
		}
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	characters = document.getElementById("system_2_characters").innerText;
 	crop_amp_threshold = document.getElementById("system_2_crop_amp_threshold").value;
 	analysis_time_gap = document.getElementById("system_2_analysis_time_gap").value;

 	form_data = new FormData()

 	form_data.append('characters', characters);
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
function system_2_retake() {
	document.getElementById("system_2_post_operations").style.visibility = "hidden";
	document.getElementById("system_2_audio_clip").style.visibility = "hidden";
	document.getElementById("system_2_processing_status").style.visibility = "hidden";
	document.getElementById("system_2_stop_recording").style.display = "none";
	document.getElementById("system_2_start_recording").style.display = "inline-block";
	document.getElementById("system_2_start_recording").style.visibility = "visible";
}	