// variables
var video, ctx, canvas, context;
var detected;
var counter = 5;
var retrievedhours, retrievedmins;

canvas = document.createElement('canvas');
context = canvas.getContext('2d');

// get media capture (Camera stream)
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

    //if the browser does not support the camera use: 
}else{
    console.log("camera API is not supported by your browser")
}

// send camera frames every second to the backend model
function sendFrames() {
    // draw the frame on a canvas
    canvas.width = 640;
    canvas.height = 480;
    context.drawImage(video,0,0,canvas.width,canvas.height);

    //convert frame to a b64img
    const b64img = canvas.toDataURL('image/jpeg');

    //send post request to send frame to backend
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

setInterval(sendFrames, 1000);

//note to self: in safari, go into dev mode and enable media capture on insecure sites
//on ios, connect phone to mac. open safari, develop, iphone, and enable the cam use there


//get the result of frame detection 
function getDetect() {
    var detectCounter = setInterval(function() {
        //send get request to the getDetect URL
    url = 'http://192.168.1.150:5500/getDetect'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        //testing
        console.log(json)
        //if item is detected update view and start timer
        if (json.value==true) {
            console.log(json.item)
            if (counter != 0) {
                counter--;
                document.getElementById('detected_object').innerHTML='Warning! ' +json.item+ ' detected! Rocket destruction in ' + counter.toString() + ' seconds';
            }
            //if item in frame for longer than 5 seconds, route to failed page
            else {
                window.location.href = "http://192.168.1.150:5500/sessionFailed";
            }
        }
        // if item is no longer detected, restart counter at 5 and update view
        if (json.value==false) {
            counter=5;
            document.getElementById('detected_object').innerHTML='';
        }
    })
        
    }, 1000);
}

//get the hours and minutes inputted by user
function getCustomHoursMinutes() {
    url = 'http://192.168.1.150:5500/getDuration'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        retrievedhours = json.hours;
        
        retrievedmins = json.minutes;
        
    })
}

//timer countdown
function timer() {
    var timer = setInterval(function() {
        document.getElementById('countdownTimer').innerHTML=retrievedhours+' hours, '+retrievedmins+' minutes ';

        // if the user inputs 0 minutes:
        if (retrievedmins==0) {
            // if the user does not input 0 hours, then the minute will change to 59 (eg going from 1h0m to 0h59m)
            if (retrievedhours!=0) {
                retrievedmins = 59;
                retrievedhours--; //decrease hours for js update
            }
            else {
                // if hour and min are both 0, route to session success page
                clearInterval(timer)
                console.log("Finished")
                window.location.href = "http://192.168.1.150:5500/sessionSuccess";
            }
        }
        else {
            // decrease min (every second for testing, every minute in deployment)
            retrievedmins--;
        }
    }, 1000); //for deployment this will be changed to 60000 for one minute

}

//when session page loads, run functions
window.onload = function () {
    getDetect();
    getCustomHoursMinutes();
    timer();
}

