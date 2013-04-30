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

$(document).ready(function()
{
   setInterval('updateClock()', 1000);
});
