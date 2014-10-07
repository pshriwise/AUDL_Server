getScoreboard = function( data ) {
	var parsedData = jQuery.parseJSON(data)
	var home_img = new Image();
	home_img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + parsedData["hteam_id"] + ".png";
	var away_img = new Image();
	away_img.src = "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + parsedData["ateam_id"] + ".png";
	
	var table = "";
	table += "<table>";
	table += "<tr>";
	table += "<th class=status colspan='2'>" + parsedData["status"];
	table += "</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th><th>T</th></tr>";
	table += "<tr>"
	table += "<td><img src='http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + parsedData["hteam_id"] + ".png'></td>";
	table += "<td>" + parsedData["hteam"]  + "</td>";
	table += "<td>0</td><td>0</td><td>0</td><td>0</td>";
	table += "<td>" + parsedData["hscore"]  + "</td>";
	table += "</tr><tr>"
	table += "<td><img src='http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Logos/" + parsedData["ateam_id"] + ".png'></td>";
	table += "<td>" + parsedData["ateam"]  + "</td>";
	table += "<td>0</td><td>0</td><td>0</td><td>0</td>";
	table += "<td>" + parsedData["ascore"]  + "</td>";
	table += "</tr>";
	table += "</table>";
	$( window ).load(function() { 
		$(".scoreboard").append(table);
	});
};

scoreboard = function( teamID ) 
{
	$(document).ready(function() {
		$.ajax({
			url: "http://ec2-54-86-111-95.compute-1.amazonaws.com:4000/Web/Score",
			jsonp: "callback",
			dataType : "jsonp",
			jsonpCallback : "getScoreboard",
			data : {"id" : teamID}
		});
	});
};