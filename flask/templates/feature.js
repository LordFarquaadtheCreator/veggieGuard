const videoElement = document.getElementById('live-camera');
let webcamStream; // Declare a variable to store the webcam stream
var x=0;
videoElement.addEventListener('click', function() {
    x++;
});
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia && x%2==1) {
  // Request access to the user's webcam
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      // Set the webcam stream as the source for the video element
      videoElement.srcObject = stream;
      webcamStream = stream; // Store the stream in the webcamStream variable
    })
    .catch(function (error) {
      console.error('Error accessing webcam:', error);
    });
} else if(x%2==0){
    if (webcamStream) {
    
        // Stop all tracks in the webcam stream
        webcamStream.getTracks().forEach((track) => {
          track.stop();
        });
        videoElement.srcObject = null; // Remove the video source
      }
}
else {
  console.error('getUserMedia is not supported in this browser');
}

// Function to stop the webcam stream
function stopWebcam() {
    x+=1;
  
}