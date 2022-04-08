// Now here we are going to write the logic for System 2.
// Testing.
// function test() {
// 	alert("test");
// }

// test()

// Writing out the function for Play Metronome.
function system_2_play_metronome() {
	// First we will make the Play Metrronome button invisible and Stop metronome button visible.
	document.getElementById("system_2_play_metronome").style.display = "none";
	document.getElementById("system_2_stop_metronome").style.display = "inline-block";

	// From here the codes start for 
	document.getElementById("tik_1").style.color = "#008cff";
	document.getElementById("metronome_number").innerHTML = "1";
	
	setTimeout(
		function() {
			document.getElementById("tik_1").style.color = "#ededed";
			document.getElementById("tik_2").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "2";
		}, 500);

	setTimeout(
		function() {
			document.getElementById("tik_2").style.color = "#ededed";
			document.getElementById("tik_3").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "3";
		}, 1000);

	setTimeout(
		function() {
			document.getElementById("tik_3").style.color = "#ededed";
			document.getElementById("tik_4").style.color = "#00b324";
			document.getElementById("metronome_number").innerHTML = "4";
		}, 1500);

	metronomeInterval = setInterval(
		function() {
			document.getElementById("tik_4").style.color = "#ededed";
			document.getElementById("tik_1").style.color = "#008cff";
			document.getElementById("metronome_number").innerHTML = "1";
			setTimeout(
				function() {
					document.getElementById("tik_1").style.color = "#ededed";
					document.getElementById("tik_2").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "2";
				}, 500);
			setTimeout(
				function() {
					document.getElementById("tik_2").style.color = "#ededed";
					document.getElementById("tik_3").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "3";
				}, 1000);

			setTimeout(
				function() {
					document.getElementById("tik_3").style.color = "#ededed";
					document.getElementById("tik_4").style.color = "#00b324";
					document.getElementById("metronome_number").innerHTML = "4";
				}, 1500);
		}, 2000)
}

// Writing out the function for stop metronome.
function system_2_stop_metronome() {
	clearInterval(metronomeInterval);
	setTimeout(function() {
		document.getElementById("tik_4").style.color = "#ededed";
		document.getElementById("metronome_number").innerHTML = "0";
	} , 2000)
	document.getElementById("system_2_stop_metronome").style.display = "none";
	document.getElementById("system_2_play_metronome").style.display = "inline-block";
}