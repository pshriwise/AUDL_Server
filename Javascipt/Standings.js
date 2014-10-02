$(document).ready(function() {
	$.ajax({
		url: "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Web/Standings",
		jsonp: "callback",
		dataType : "jsonp",
		jsonpCallback : "getStandings",
		cache : "true"
	});
});
getStandings = function( data ) {
		var parsedData = [];
		var table = "";
		parsedData=jQuery.parseJSON(data)
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
				table += "<tr>";
				table += "<td><img src='http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + teamArray["id"] + ".png'></td>";
				table += "<td>" + teamArray["name"] + "</td>";
				table += "<td>" + teamArray["wins"] + "</td>";
				table += "<td>" + teamArray["losses"] + "</td>";
				table += "<td>" + teamArray["plmn"] + "</td>";
				table += "</tr>";
			})
			table += "</table>";
		})
		$(".standings").append(table);
};