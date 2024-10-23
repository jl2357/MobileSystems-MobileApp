var video, ctx, canvas, context;

canvas = document.createElement('canvas');
context = canvas.getContext('2d');

console.log("in js")
if(navigator && navigator.mediaDevices){
    //get the camera stream of the front facing camera
    const options = { audio: false, video: { facingMode: "user", width: 300, height: 300  } }

    navigator.mediaDevices.getUserMedia(options)

    .then(function(stream) {
        video = document.querySelector('video');

        //these three atributes are required to work on ios
        video.setAttribute('autoplay', '');
        video.setAttribute('muted', '');
        video.setAttribute('playsinline', '')
        video.srcObject = stream;
        video.onloadedmetadata = function(e) {
          video.play();
        };
        

        
    })
    //error handling
    .catch(function(err) {
        console.log("caught an error")
        console.log(err)
    });

    //if the browser does not support the camera use
    
}else{
    console.log("camera API is not supported by your browser")
}

function sendFrames() {
    canvas.width = 640;
    canvas.height = 480;
    context.drawImage(video,0,0,canvas.width,canvas.height);

    const b64img = canvas.toDataURL('image/jpeg');

    fetch('http://192.168.1.150:5500/process_frames', {
        method: 'POST',
        body: JSON.stringify({ image: b64img }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    }).then(response => response.text()) 
    .then(data => console.log('Processed!'))
    .catch(err => console.error(err));
}

setInterval(sendFrames, 2000);
//note to self: in safari, go into dev mode and enable media capture on insecure sites
//on ios, connect phone to mac. open safari, develop, iphone, and enable the cam use there