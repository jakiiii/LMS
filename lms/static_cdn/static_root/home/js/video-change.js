function changeVideo(x) {
    var rootfolder = "/media/"     ;
    var newvideo = rootfolder+""+x;
    var iframe = document.getElementById("episode-video-frame");
    document.getElementById('episode-video-frame').src = newvideo;
}

 /* function ShowVideo() {
    
      var modal = document.getElementById("videoModal");

       // Get the button that opens the modal
         var btn = document.getElementById("myBtn");

      //  Get the <span> element that closes the modal
      var span = document.getElementsByClassName("close")[0];

      //  When the user clicks the button, open the modal
       
      modal.style.display = "block";
       
//
      ////  When the user clicks on <span> (x), close the modal
      span.onclick = function () {
          modal.style.display = "none";
      }
//
      //  When the user clicks anywhere outside of the modal, close it
      window.onclick = function (event) {
          if (event.target == modal) {
              modal.style.display = "none";
          }
      }
  }*/
