function updateClock ( )
    {
    var currentTime = new Date ( );
    var currentHours = currentTime.getHours ( );
    var currentMinutes = currentTime.getMinutes ( );
    var currentSeconds = currentTime.getSeconds ( );
    var currentDate = currentTime.getDate ( );
    var currentDay = currentTime.getDay ( );
    var currentMonth = currentTime.getMonth ( );
    var currentYear = currentTime.getFullYear ( );

    // Pad the minutes and seconds with leading zeros, if required
    currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
    currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;

    // Choose either "AM" or "PM" as appropriate
    var timeOfDay = ( currentHours < 12 ) ? "AM" : "PM";

    // Convert the hours component to 12-hour format if needed
    currentHours = ( currentHours > 12 ) ? currentHours - 12 : currentHours;

    // Convert an hours component of "0" to "12"
    currentHours = ( currentHours == 0 ) ? 12 : currentHours;

    // Convert day to name
    daysOfWeek = ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"];
    currentDay = daysOfWeek[currentDay];

    // Convert month to name
    months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];
    currentMonth = months[currentMonth];

    // Compose the string for display
    var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds;
    var currentDateString = currentDay + ", " + currentDate + " " + currentMonth + " " + currentYear;
    
    
    $("#clock").html(currentTimeString);
    $("#date").html(currentDateString);
        
 }

function updateBiclooStation(id, name, element) {
    $.getJSON("/bicloo", {id: id, name: name})
    .done(function(station){
        $('#bicloo').show();
        $(element).html(station.name + " " + station.available + "D " + station.free + "L");
    });
}

function updateTANStation(code, direction, element) {
    $.getJSON("/tan", {code: code, direction: direction})
    .done(function(station){
        $(element).show();
        $(element).html("<h3>TAN</h3>");
        $.each(station.slots, function(i, item){
            if (i == 0) {
                $(element).append("<h1>" + item.terminal + " " + item.time +"</h1>");
            } else {
                $(element).append("<h3>" + item.terminal + " " + item.time +"</h3>");
            }
        });
    });
}

$(document).ready(function()
{
    updateClock();
    setInterval('updateClock()', 1000);

    updateBiclooStation(18, "Place Viarme", "#bicloo-1");
    setInterval('updateBiclooStation(18, "Place Viarme", "#bicloo-1")', 30000);

    updateBiclooStation(17, "Sainte Elisabeth", "#bicloo-2");
    setInterval('updateBiclooStation(17, "Sainte Elisabeth", "#bicloo-2")', 30000);

    updateTANStation("VIAR", 2, "#tan");
    setInterval('updateTANStation("VIAR", 2, "#tan")', 30000);
});

