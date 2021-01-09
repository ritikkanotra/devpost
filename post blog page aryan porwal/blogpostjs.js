function check1(){
		var field=document.getElementById("fn").value;

		if(field!=""){
			document.getElementById("message1").innerHTML="Accepted";
		    document.getElementById("message1").style.color="green";}
		else{
			document.getElementById("message1").innerHTML="invalid";
			document.getElementById("message1").style.color="red";
		}

	}function check2(){
		var field=document.getElementById("ln").value;

		if(field!=""){
			document.getElementById("message2").innerHTML="Accepted";
		    document.getElementById("message2").style.color="green";}
		else{
			document.getElementById("message2").innerHTML="invalid";
			document.getElementById("message2").style.color="red";
		}

	}

	function check3(){
		var field=document.getElementById("pw").value;

		if(field!=""){
			document.getElementById("message3").innerHTML="Accepted";
		    document.getElementById("message3").style.color="green";}
		else{
			document.getElementById("message3").innerHTML="invalid";
			document.getElementById("message3").style.color="red";
		}

	}

