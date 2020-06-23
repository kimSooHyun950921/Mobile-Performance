var buttonRecord = document.getElementById("record");
var buttonStop = document.getElementById("stop");
var buttonanalysis = document.getElementById("analysis")
//buttonStop.disasbled = true;

buttonRecord.onclick = function(){
    buttonRecord.disabled = true;
    buttonStop.disabled = false;
    var filename = document.getElementById("filename").value;
    alert(filename)
    var url = "http://localhost:8090/record_status"

    makeCorsRequest(url, "true", filename)
    alert('start recording')
}

buttonStop.onclick = function(){
    buttonRecord.disabled = false;
    buttonStop.disabled = true;
    var filename = document.getElementById("filename").value;
    alert(filename)
    var url = "http://localhost:8090/record_status"
    makeCorsRequest(url, "false",filename);
    alert("Saved file:"+filename)

    if(buttonanalysis.style.visibility == "hidden"){
        buttonanalysis.style.visibility = "visible";
    }
}

buttonanalysis.onclick = function(){
    var url = "http://localhost:8888/"

    location.href = "/analysis"
    $.ajax({
        accepts: {
            type: "POST",
            url:"/home/kimsoohyun/00-Research/02-Graph/ios/ios-app_analyze/01-performance_calculator/speedindex_a5_mp4.py",
            data: {param: '-d ios'}
            }}.done(function(o){
            }));
}

function createCORSRequest(method, url, filenmae){
    var xhr = new XMLHttpRequest();
    if("withCredential" in xhr){
        xhr.open(method, url, true);
        }
    else if(typeof XDomainRequest != "undefined"){
        xhr = new XDomainRequest();
        xhr.open(method, url);
    }
    else{
        xhr.open(method, url);
    }
    return xhr;
}

function makeCorsRequest(url, bool, filename){
    var xhr = new createCORSRequest("POST", url);
    if(!xhr) {
        alert("error occur");
        throw new Error('CROS not supported');
        return;
    }

    xhr.onload = function(){
        console.log('xhr is loading...');
    };

    xhr.onerror = function(){
        alert('Woops, there was an error making the request.');
    };

    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            console.log('act correct');
       }
    };

    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    var json = JSON.stringify({'status':bool, 'filename':filename});
    console.log('SEND:'+json);
    xhr.send(json);
}

