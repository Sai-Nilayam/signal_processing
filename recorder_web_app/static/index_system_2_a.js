// Testing
// function test() {
// 	alert("test")
// }

// test()

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
	url = '/system_2_a/process_audio'

 	xhttp = new XMLHttpRequest();
 	xhttp.onload = function() {
		response_text = this.responseText;
		response_json = JSON.parse(response_text);

		document.getElementById("unique_word_count").innerHTML = " " + response_json.unique_word_count + " ";
		document.getElementById("no_of_takes").innerHTML = " " + response_json.no_of_takes + " ";
		document.getElementById("estimated_recording_time").innerHTML = " " + response_json.estimated_recording_time + " "; 
		document.getElementById("total_no_of_takes").innerHTML = "/" + " " + response_json.no_of_takes + " ";  
	}
	
	vv_set = document.getElementById("system_2_a_vv_set").value;
	vv_notation = document.getElementById("system_2_a_vv_notation").value;

	if (vv_set == "Select a Vyanjana Varna Set" || vv_notation == "" || demo_clip_selected_s == false || demo_clip_selected_e == false) {
		alert("Please select a Vyanjana Varan Set, put a Vyanjana Varna Notation, select two Vyanjana Varan Starting and Ending sounds at repective fields.")
		return;
	}

	vv_s_audio = new Audio(demo_clip_url_s);
	vv_e_audio = new Audio(demo_clip_url_e);

	form_data = new FormData();
 	form_data.append('vv_set', vv_set);
	form_data.append('vv_notation', vv_notation);
	form_data.append('vv_s_audio', vv_s_audio);
	form_data.append('vv_e_audio', vv_e_audio);

	xhttp.open("POST", url);
	xhttp.send(form_data)

}
