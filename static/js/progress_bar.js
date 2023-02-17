window.onload = function() {
    function updateProgress(percent) {
      document.querySelector("#progress").style.width = percent + "%";
      document.querySelector("#progress").innerHTML = percent + "%";
    }

    document.querySelector("#start-button").addEventListener("click", function() {
      var percent = 0;
      var interval = setInterval(function() {
        percent += 10;
        updateProgress(percent);
        if (percent >= 100) {
          clearInterval(interval);
        }
      }, 1000);
    });
  }