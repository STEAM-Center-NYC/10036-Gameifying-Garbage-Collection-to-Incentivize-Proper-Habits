window.addEventListener("load", () => {
  clock();
  function clock() {
    const today = new Date();

    // get time components
    const hours = today.getHours();
    const minutes = today.getMinutes();
    const seconds = today.getSeconds();

    // add '0' to minute & second when they are less than 10
    const minute = minutes < 10 ? "0" + minutes : minutes;

    // make clock a 12-hour time clock
    let hour = hours % 12 || 12; // Ensure hour is never 0, use 12 instead

    // assigning 'am' or 'pm' to indicate time of the day
    const ampm = hours < 12 ? " AM" : " PM";

    // get current time
    const time = hour + ":" + minute + ampm;

    // combine current time
    const dateTime = time;

    // print current time to the DOM
    document.getElementById("time").innerHTML = dateTime;
    setTimeout(clock, 1000);
  }
});
