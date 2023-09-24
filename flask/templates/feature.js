const videoElement = document.getElementById('live-camera');
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Request access to the user's webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            // Set the webcam stream as the source for the video element
            videoElement.srcObject = stream;
        })
        .catch(function (error) {
            console.error('Error accessing webcam:', error);
        });
} else {
    console.error('getUserMedia is not supported in this browser');
}