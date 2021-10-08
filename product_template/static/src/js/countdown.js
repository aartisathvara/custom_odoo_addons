$(document).ready(function () {
    console.log("=====call function=====")

    setInterval(function(){
        var countDate = new Date("Oct 10 2021 12:00:00").getTime()
        console.log("count date====",countDate)

        var now = new Date().getTime()
        console.log("now=====",now)

        var distance = countDate - now;
        console.log('=====distance====',distance)

        var second = 1000;
        var minute = second * 60;
        var hour = minute * 60;
        var day = hour * 24;

        var textDays = Math.floor(distance / day);
        console.log('=====textDay====',textDays)

        var textHours = Math.floor((distance % day) / hour);
        console.log('=====textHour====',textHours)

        var textMinutes = Math.floor((distance % hour) /minute);
        console.log('=====textMinute====',textMinutes)

        var textSeconds = Math.floor((distance % minute) / second);
        console.log('=====textSecond====',textSeconds)

        if(document.querySelector('.count_days') && document.querySelector('.count_hours') &&
            document.querySelector('.count_minutes') && document.querySelector('.count_seconds'))
        {
            document.querySelector('.count_days').innerText = textDays;
            document.querySelector('.count_hours').innerText = textHours;
            document.querySelector('.count_minutes').innerText = textMinutes;
            document.querySelector('.count_seconds').innerText = textSeconds;
        }
    },1000);
});