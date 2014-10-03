$(document).ready(function() {
	$.ajax({
		url: "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Web/Standings",
		jsonp: "callback",
		dataType : "jsonp",
		jsonpCallback : "getStandings"
	});
});
var standingsTable = "";
getStandings = function( data ) {
	var parsedData = jQuery.parseJSON(data)
	$.each( parsedData, function( divisionName, divisionArray ) {
		if (standingsTable != "") standingsTable += "<br><br>";
		standingsTable += "<table id=" + divisionName + " >";
		standingsTable += "<tr>";
		standingsTable += "<th colspan=2>" + divisionName + "</th>";
		standingsTable += "<th>W</th>";
		standingsTable += "<th>L</th>";
		standingsTable += "<th>PD</th>";
		standingsTable += "</tr>";
		
		$.each( divisionArray, function( j, teamArray ) {
			var img = new Image();
			img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + teamArray["id"] + ".png";
			
			standingsTable += "<tr class='" + teamArray["name"].replace(/\s/g, '') + "'>";
			standingsTable += "<td><img src='http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + teamArray["id"] + ".png'></td>";
			standingsTable += "<td>" + teamArray["name"] + "</td>";
			standingsTable += "<td>" + teamArray["wins"] + "</td>";
			standingsTable += "<td>" + teamArray["losses"] + "</td>";
			standingsTable += "<td>" + teamArray["plmn"] + "</td>";
			standingsTable += "</tr>";
		})
		standingsTable += "</table>";
	})
};
$( window ).load(function() { 
	$(".standings").append(standingsTable);
});