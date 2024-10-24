var video, ctx, canvas, context;
var detected;
var counter = 5;
var retrievedhours, retrievedmins;

canvas = document.createElement('canvas');
context = canvas.getContext('2d');

console.log("testing: in js")
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

setInterval(sendFrames, 1000);
//note to self: in safari, go into dev mode and enable media capture on insecure sites
//on ios, connect phone to mac. open safari, develop, iphone, and enable the cam use there


//detection functions
function getDetect() {
    var detectCounter = setInterval(function() {
    url = 'http://192.168.1.150:5500/getDetect'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        console.log(json)
        if (json.value==true) {
            console.log(json.item)
            if (counter != 0) {
                counter--;
                console.log(counter)
                document.getElementById('detected_object').innerHTML='Warning! ' +json.item+ ' detected! Rocket destruction in ' + counter.toString() + ' seconds';
            }
            else {
                window.location.href = "http://192.168.1.150:5500/sessionFailed";
            }
        }
        if (json.value==false) {
            counter=5;
            document.getElementById('detected_object').innerHTML='';
        }
    })
        
    }, 1000);
}

//timer functions
function getCustomHoursMinutes() {
    url = 'http://192.168.1.150:5500/getDuration'
    fetch(url)
    .then(response => response.json())
    .then(json => {
        retrievedhours = json.hours;
        console.log(retrievedhours)
        retrievedmins = json.minutes;
        console.log(json)
    })
}

function timer() {
    var timer = setInterval(function() {
        document.getElementById('countdownTimer').innerHTML=retrievedhours+' hours, '+retrievedmins+' minutes ';
        if (retrievedmins==0) {
            if (retrievedhours!=0) {
                retrievedmins = 59;
                retrievedhours--;
            }
            else {
                clearInterval(timer)
                console.log("Finished")
                window.location.href = "http://192.168.1.150:5500/sessionSuccess";
            }
        }
        else {
            retrievedmins--;
        }
    }, 1000);

}

//when session page loads, run functions
window.onload = function () {
    getDetect();
    getCustomHoursMinutes();
    timer();
}

