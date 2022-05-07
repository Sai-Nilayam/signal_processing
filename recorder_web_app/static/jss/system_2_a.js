// The first thing to do is to put the html content to a the system_2_a div.
function system_2_a_put_html() {
	url = '/static/htmls/system_2_a.html';
	xhttp = new XMLHttpRequest();
	xhttp.onload = function() {
		html_content = this.responseText;
		document.getElementById("system_2_a").innerHTML = html_content; 
	}
	xhttp.open("GET", url);
	xhttp.send()

}

system_2_a_put_html()

demo_clip_selected_s = false;
demo_clip_selected_e = false;

// The first thing to do here is to grab the file as soon as the file selection event takes place. 
function system_2_a_grab_audio_url_s(event) {
	demo_clip_url_s = URL.createObjectURL(event.target.files[0]);
	demo_clip_selected_s = true;
	// alert(demo_clip_url);
}

// For Playing the demo clip.
function system_2_a_play_demo_clip_s() {
	// Check if the demo clip has been selected or not. 
	if (demo_clip_selected_s == false) {
		alert("Please select a demo audio clip.");
		return;
	}

	document.getElementById("system_2_a_demo_clip_animation_s").style.visibility = "visible";
	audio = new Audio(demo_clip_url_s);
	audio.onended = function() {
	 		document.getElementById("system_2_a_demo_clip_animation_s").style.visibility = "hidden";
	 	}
	audio.play();	
}

demo_clip_selected_e = false;

// The first thing to do here is to grab the file as soon as the file selection event takes place. 
function system_2_a_grab_audio_url_e(event) {
	demo_clip_url_e = URL.createObjectURL(event.target.files[0]);
	demo_clip_selected_e = true;
	// alert(demo_clip_url);
}

// For Playing the demo clip.
function system_2_a_play_demo_clip_e() {
	// Check if the demo clip has been selected or not. 
	if (demo_clip_selected_e == false) {
		alert("Please select a demo audio clip.");
		return;
	}

	document.getElementById("system_2_a_demo_clip_animation_e").style.visibility = "visible";
	audio = new Audio(demo_clip_url_e);
	audio.onended = function() {
	 		document.getElementById("system_2_a_demo_clip_animation_e").style.visibility = "hidden";
	 	}
	audio.play();	
}

// Writing a function for system_2_a test.
function system_2_a_test() {
	vv_set = document.getElementById("system_2_a_vv_set").value;
	vv_notation = document.getElementById("system_2_a_vv_notation").value;

	if (vv_set == "Select a Vyanjana Varna Set" || vv_notation == "" || demo_clip_selected_s == false || demo_clip_selected_e == false) {
		alert("Please select a Vyanjana Varan Set, put a Vyanjana Varna Notation, select two Vyanjana Varan Starting and Ending sounds at repective fields.")
		return;
	}

	document.getElementById("system_2_a_test").style.visibility = "hidden";
	document.getElementById("system_2_a_please_wait").style.visibility = "visible";

	url = '/system_2_a/process_audio'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		document.getElementById("system_2_a_please_wait").style.visibility = "hidden";
		document.getElementById("system_2_a_processing_status").innerHTML = "Success . . ! Please listen to the clip below and verify that the Vyanja Vaarna sound chunk is properly aligning with other differnt sounds and click on done. Else do a retake.";
		document.getElementById("system_2_a_processing_status").style.color = "#f58742";
		document.getElementById("system_2_a_processing_status").style.visibility = "visible";
		document.getElementById("system_2_a_done").style.display = "inline-block";
		document.getElementById("system_2_a_post_operations").style.visibility = "visible";
		document.getElementById("system_2_a_audio_clip").src = response_json.file_url;
		document.getElementById("system_2_a_audio_clip").style.visibility = "visible";	 
	}

	vv_s_audio = document.getElementById("system_2_a_vv_s").files[0];
	vv_e_audio = document.getElementById("system_2_a_vv_s").files[0];

	form_data = new FormData();
 	form_data.append('vv_set', vv_set);
	form_data.append('vv_notation', vv_notation);
	form_data.append('vv_s_audio', vv_s_audio);
	form_data.append('vv_e_audio', vv_e_audio);

	xhttp.open("POST", url);
	xhttp.send(form_data)

}

// For reupload.
function system_2_a_reupload() {

	document.getElementById("system_2_a_post_operations").style.visibility = "hidden";
	document.getElementById("system_2_a_audio_clip").style.visibility = "hidden";
	document.getElementById("system_2_a_processing_status").style.visibility = "hidden";
	document.getElementById("system_2_a_vv_s").value = null;
	document.getElementById("system_2_a_vv_e").value = null;
	document.getElementById("system_2_a_test").style.visibility = "visible";
}

// For done
function system_2_a_done() {
	url = '/system_2_a/done'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		// response_text = this.responseText;
		// response_json = JSON.parse(response_text);

		document.getElementById("system_2_a_post_operations").style.visibility = "hidden";
		document.getElementById("system_2_a_audio_clip").style.visibility = "hidden";
		document.getElementById("system_2_a_processing_status").style.visibility = "hidden";
		document.getElementById("system_2_a_vv_s").value = null;
		document.getElementById("system_2_a_vv_e").value = null;
		document.getElementById("system_2_a_vv_notation").value = null;
		document.getElementById("system_2_a_test").style.visibility = "visible";
	}

 	xhttp.open("POST", url);
 	// Preparing the data
 	vv_set = document.getElementById("system_2_a_vv_set").value;
 	
 	form_data = new FormData()
 	form_data.append('vv_set', vv_set)

	xhttp.send(form_data)
}

// Writing the function for the testing play
function system_2_a_testing_play() {
	vv_set = document.getElementById("system_2_a_vv_set_test").value;
	characters = document.getElementById("system_2_a_testing_characters").value;

	if (vv_set == "Select a Vyanjana Varna Set" || characters == "") {
 		alert("Please select a voice and put some characters in the respective fields.")
 		return;
 	}

	url = '/system_2_a/testing_play';

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		if (response_json.processing_status == "failed") {
			alert("A few Vyanja Varnas are not uploaded. Please upload the Vyanjana Varna Chunks using the Name Entity Pronounciation Alternate Module.");
			return;
		}

		file_url = response_json.file_url;

		audio = new Audio(file_url);

	 	audio.onended = function() {
	 		document.getElementById("system_2_a_testing_play_animation").style.visibility = "hidden";
	 	}

	 	document.getElementById("system_2_a_testing_play_animation").style.visibility = "visible";
		audio.play()
	}

	xhttp.open("POST", url);

 	// Preparing the data
 	form_data = new FormData()
 	form_data.append('vv_set', vv_set)
 	form_data.append('characters', characters)

	xhttp.send(form_data)
}

// Reset backend.
function system_2_a_reset_backend() {
	alert("This button is disabled for this module as it's hard to upload all the Vyanja Varna sounds once deleted.")
}