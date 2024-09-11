var startDate = new Date('2018-10-12');
var timer;

timer = setInterval(function() {
  updateTime(startDate);
}, 1000);

function updateTime(startDate) {
  var now = new Date();
  var difference = now - startDate;

  var seconds = Math.floor(difference / 1000);
  var minutes = Math.floor(seconds / 60);
  var hours = Math.floor(minutes / 60);
  var days = Math.floor(hours / 24);

  var years = now.getFullYear() - startDate.getFullYear();
  var months = now.getMonth() - startDate.getMonth();
  days = now.getDate() - startDate.getDate();

  if (days < 0) {
    var lastMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    days += lastMonth.getDate();
    months--;
  }

  if (months < 0) {
    years--;
    months += 12;
  }

  hours %= 24;
  minutes %= 60;
  seconds %= 60;

  document.getElementById("years").innerText = years;
  document.getElementById("months").innerText = months;
  document.getElementById("days").innerText = days;
  document.getElementById("hours").innerText = hours;
  document.getElementById("minutes").innerText = minutes;
  document.getElementById("seconds").innerText = seconds;
}