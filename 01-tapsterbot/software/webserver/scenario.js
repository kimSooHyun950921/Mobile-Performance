var http = require('http');
var url = require('url');
var fs = require('fs');
var path = require('path');
var bot = require('../src/bot.js');
var waitSync = require('wait-sync');
var csv_writer = require('csv-writer');
var bot_move = require('./click-event.js');
const { parse } = require('querystring');
const { cors } = require('cors');
http.createServer(onRequest).listen(8888);
console.log('another server opened');

var csv_data = [];
var starttime = 0;
var data = 'data';
var contentMap = {
    '/': 'scene.html',
    '/scenario.js': 'scene.html',
    '/recorder.js': 'recorder.js',
    '/analysis': 'analysis.html'
    }
var options = {                                                                 
    host: "localhost",
    port: 8090,
    path: "/recording",                                                                   
    method: "GET",                                                             
    headers: {                                                                  
        "Content-Type": "applciation/x-www-form-urlencoded",
        'Content-Length': Buffer.byteLength(data)
        }                                                                       
 };   


var req = http.request(options, function(res) {
    res.setEncoding('utf8')
    var responseString = "";

    res.on("data", function (data) {
        responseString += data;
    });
    res.on("end", function (){
        //console.log("responseString: "+responseString)
        //#res.send('ok')
    });

});


function collectRequestData(request, callback) {
    //console.log(request)
    const FORM_URLENCODED = 'application/x-www-form-urlencoded';
    if(request.headers['content-type'] === FORM_URLENCODED){
        let body = '';
        request.on('data', chunk => {
            body += chunk.toString();
            //console.log("body: "+body)
            });
        request.on('end', () => {
            callback(parse(body));
            });
       }
       else{
            callback(null);
       }
   }


function onRequest(request, response){
    var pathName = url.parse(request.url).pathname;

    if(request.method == 'POST'){
        data = 'recording'
        req.write(data)

        collectRequestData(request, result => {
               
                var post_data_key = Object.keys(result);
                for(var item of post_data_key){
                    console.log("[MID DEBUG] "+item.toString())
                    if(item.toString() == 'count'){
                        //랜덤 값으로 전송
                        count = result['count']
                        control_robot(result)}
                    else if (item.toString() == 'xy-axis'){
                        value = parse_json(result)
                        console.log('[DEBUG] value', value)
                        control_robot_xy(value.appname, value.x, value.y)
                        //console.log("BOT MOVE BYE");
                        send_msg(response, 200,  "OK");}
                    else if(item.toString() == 'starttime'){
                        starttime = parseFloat(result['starttime'])
                        console.log("[GET STARTTIME]starttime: "+starttime)
                        send_msg(response, 200, "OK")}

                }
            });
        }
    else{
        showPage(response, pathName)
        }
    }


function parse_json(json_format){
    json_xy = json_format['xy-axis']                             
                                                                            
    xy = JSON.parse(json_xy)                                
    appname = xy.appname                                    
    x_axis = parseInt(xy.x, 10)                             
    y_axis = parseInt(xy.y, 10)                                                                                           
    //console.log("[AppName]"+appname+"[x_axis]"+x_axis+"[y_axis]"+ y_axis)

    return {'x': x_axis, 'y':y_axis, 'appname':appname}
}


function time(){
    //console.log("DATE TIME: "+parseFloat(Date.now())/1000)
    return parseFloat(Date.now())/1000
}


function push_data(data, x, y, curtime, loadtime){
    data.push({'x-axis': x, 'y-axis': y, 'curtime': curtime, 'load-time':loadtime})
    return data
}


function control_robot_xy(appname, x, y){
    //console.log(starttime)
    //console.log("[DEBUG] x: "+x+ " y:"+y)
    if(x < -100 && y < -100){
        write_csv(appname, csv_data)
    }
    else if(x > 20 && y > 50){
        //starttime = time()
        console.log("starttime : ", starttime)
    }
    else{
        var start_loadtime = time()
        bot_move.click(x, y) 
        var endtime = time()

        var curtime = endtime - starttime
        var loadtime = endtime - start_loadtime
        console.log("starttime: "+starttime+", endtime: "+endtime+", curtime: "+ curtime+", loadtime: "+loadtime)
        csv_data = push_data(csv_data, x, y, curtime, loadtime)
        }

}


//TODO bot control app server를 따로 만들어야함!
function control_robot(result){ 
    start_time = parseFloat(Date.now())
    for(i = 0; i <  result['count']; i++){

        load_start_time = parseFloat(Date.now())

        bot_move.move()
        waitSync(1)

        curtime = (parseFloat(Date.now()) - start_time)/1000

        load_end_time = parseFloat(Date.now()) 
        load_time = (load_end_time - load_start_time)/1000

        //console.log("load_time: "+load_time)
        //console.log("curtime:"+curtime)
        csv_data.push({'x-axis': x, 'y-axis': y, 'curtime': curtime, 'load-time':load_time})

        waitSync(2)}

        //write_csv(csv_data)
}




function write_csv(csv_name, csv_data){
    var csv_filename = 'ios_'+csv_name + '.csv'
    var csv_path = path.join('/','home', 'kimsoohyun', '00-Research', '02-Graph',
                             '05-data', 'cut_point', csv_filename)
      
    var createCsvWriter = csv_writer.createObjectCsvWriter; 
    var csvWriter = createCsvWriter({
    
    path: csv_path, 
    header: [                                                                   
        {id: 'x-axis', title: 'x-axis'},                                        
        {id: 'y-axis', title: 'y-axis'},                                         
        {id: 'curtime',    title: 'cur_time'},                                  
        {id: 'load-time', title: 'load-time'}                                   
    ]                                                                           
    });
    csvWriter
        .writeRecords(csv_data)
        .then(()=> console.log('The CSV file was written successfully'));
}

//TODO ??
function working(page){
    if(page == 'scene.html'){
    }
    else if(page == 'analysis'){

    }
}


function showPage(response, pathName){
    if(contentMap[pathName]){
        //console.log('LOG'+contentMap[pathName]);
        fs.readFile(contentMap[pathName], function(err, data){
                working(pathName)
                send_msg(response, 200, data);
        });
    }
    else{
        send_msg(response, 404, '404 Page not found');
    }
  }


function send_msg(response, status_code, data){
    response.writeHead(status_code, {'Content-Type': 'text/html'});         
    //console.log(data);                                              
    response.write(data);                                           
    response.end(); 
}
