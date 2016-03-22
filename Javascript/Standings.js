getStandings = function( data ) {
	var parsedData = jQuery.parseJSON(data)
	var table = "";
	$.each( parsedData, function( divisionName, divisionArray ) {
		if (table != "") table += "<br><br>";
		table += "<table id=" + divisionName + " >";
		table += "<tr>";
		table += "<th colspan=2>" + divisionName + "</th>";
		table += "<th>W</th>";
		table += "<th>L</th>";
		table += "<th>PD</th>";
		table += "</tr>";
		
		$.each( divisionArray, function( j, teamArray ) {
			var img = new Image();
			img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4002/Logos/TeamIcons_" + teamArray["nm"] + ".png";
			
			table += "<tr class='" + teamArray["name"].replace(/\s/g, '') + "'>";
			table += "<td><img src='http://ec2-54-86-111-95.compute-1.amazonaws.com:4002/Logos/TeamIcons_" + teamArray["nm"] + ".png'></td>";
			table += "<td>" + teamArray["name"] + "</td>";
			table += "<td>" + teamArray["wins"] + "</td>";
			table += "<td>" + teamArray["losses"] + "</td>";
			table += "<td>" + teamArray["plmn"] + "</td>";
			table += "</tr>";
		})
		table += "</table>";
	})
	$( window ).load(function() { 
		$(".standings").append(table);
	});
};

standings = function( division ) 
{
	$(document).ready(function() {
		$.ajax({
			url: "http://ec2-54-86-111-95.compute-1.amazonaws.com:4002/Web/Standings",
			jsonp: "callback",
			dataType : "jsonp",
			jsonpCallback : "getStandings",
			data : {"division" : division}
		});
	});
};
