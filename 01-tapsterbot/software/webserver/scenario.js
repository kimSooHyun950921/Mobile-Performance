var http = require('http');
var url = require('url');
var fs = require('fs');
var bot = require('../src/bot.js');
var waitSync = require('wait-sync');
var csv_writer = require('csv-writer');
var bot_move = require('./click-event-timeout.js');
var bot_move_time = 0
const { parse } = require('querystring');
const { cors } = require('cors');

http.createServer(onRequest).listen(8888);
console.log('another server opened');


var csv_data = [];
let rcindex = 0;
let start_time = 0;
let is_going = false
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

var predict_options = {
    host: "localhost",
    port: 8889,
    path: "/predict",
    method: "GET",
};


predict_callback = function(response){
  var str = ''
  console.log("REQUEST START")
  response.on('data', function(chunk){
    str += chunk
  });
  response.on('end', function(){
    console.log(str);
    var obj = JSON.parse(str);
    var box_list = obj.box;

      rcindex += 1
   // for(i = 0; i<box_list.length; i++){
    if (box_list.length > 0){
      
      i = getRandomInt(box_list.length)
      console.log("RANDOM:"+i)
      console.log("list: "+box_list[i])
      elem = box_list[i]

      elem_x = Number(((elem[0] + elem[2]) / 2).toFixed(2));
      elem_y = Number(((elem[1] + elem[3]) / 2).toFixed(2));
      console.log(elem_x, elem_y)
      robot_control(elem_x, elem_y);
      curtime = (parseFloat(Date.now()/1000) - start_time)
      console.log("[ROBOT COUNT INDEX] index + 1")
      csv_data.push({'x-axis': elem_x, 'y-axis': elem_y, 'curtime': curtime})
     }
    //waitSync(2);
    console.log("END");  
});
 }
//var predict_req = http.request(predict_options, predict_callback);


//var req = http.request(options, function(res) {
 //   res.setEncoding('utf8')
 //   var responseString = "";

//    res.on("data", function (data) {
//        responseString += data;
//    });
//    res.on("end", function (){
//        console.log("TEST!");
//        console.log(responseString)
//    });

//});


function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}


function collectRequestData(request, callback) {
    const FORM_URLENCODED = 'application/x-www-form-urlencoded';
    if(request.headers['content-type'] === FORM_URLENCODED){
        let body = '';
        request.on('data', chunk => {
            body += chunk.toString();
            console.log(body)
            });
        request.on('end', () => {
            callback(parse(body));
            });
       }
       else{
            callback(null);
       }
   }


function start_experiment(start_time, count, filename){
  while(rcindex < count){

    console.log("[ROBOT COUNT INDEX] "+ rcindex)
    http.request(predict_options, predict_callback).end();
    waitSync(10)
  }
  splitStr = filename.split('_')
  device = splitStr[0]
  appname = splitStr[1]
  //write_csv(device, appname);
  waitSync(2);
  console.log("DONE");
}

function onRequest(request, response){
    var pathName = url.parse(request.url).pathname;
    console.log('method: ')
    console.log(request.method)
    if(request.method == 'POST'){
        data = 'recording'
        //req.write(data)

        collectRequestData(request, result => {
                var post_data_key = Object.keys(result);
                if(post_data_key.includes("source")){
                    source = result['source']
                    if(source == 'recording'){
                      if(result['status'] == 'start'){
                        start_time = result['starttime'];
                        appname = result['appname']
                        count = 5//result['count']
                        send_msg(response, "OK");
                        is_going = true
                        console.log("START EX");
                        rcindex = 0;
                        start_experiment(start_time,count,appname);
                        }
                      else{
                        is_going = false
                        send_json_msg(response, csv_data);
                        csv_data = []
                        console.log('sendOK')
                      }
                    }
                   else if(source == 'recording-passive'){
                      if(result['status'] == 'start'){
                        start_time = result['starttime'];
                        console.log("START TIME: "+ start_time);
                        appname = result['appname']
                        send_msg(response, "OK");
                        is_going = true
                        console.log("START EX");
                        rcindex = 0;
                      }
                      else if(result['status'] == 'appexecute'){
                        console.log("appexecute");
                        appexecute_time = result['execute']
                        csv_data.push({'x-axis': 0, 'y-axis': 0, 'curtime': appexecute_time-start_time, 'load-time':0})
                        console.log('appexecute_time:'+ appexecute_time);
                        appname = result['appname']
                        send_msg(response, "OK")
                      }
                      else if(result['status'] == 'on-going'){
                          x = result['xy-axisx']
                          y = result['xy-axisy']
                          z = result['xy-axisz']
                          //xy = JSON.parse(json_xy)
                          appname = result['appname']
                          console.log("[DEBUG]: ",result)
                          x_axis = parseInt(x, 10)
                          y_axis = parseInt(y, 10)
                          z_axis = parseInt(z, 10)
                          console.log(appname, x_axis, y_axis, z_axis)
                          control_robot(x_axis, y_axis)
                          //bot_move.click(x_axis, y_axis, z_axis)
                          console.log("BOT MOVE BYE");
                          send_msg(response, "OK");
                      }
                     else{
                        send_json_msg(response, csv_data);
                        csv_data = []
                        console.log('sendOK')
                        bot_move_time = 0
                     } 

                   }
                   else if(source == 'click-test'){
                          json_xy = result['xy-axis']
                          xy = JSON.parse(json_xy)
                          appname = xy.appname
                          x_axis = parseInt(xy.x, 10)
                          y_axis = parseInt(xy.y, 10)
                          z_axis = parseInt(xy.z, 10)
                          console.log(appname, x_axis, y_axis, z_axis)
                          control_robot(result)
                          //bot_move.click(x_axis, y_axis, z_axis)
                          console.log("BOT MOVE BYE");
                          send_msg(response, "OK");
                      }
                    else{
                      if(item.toString() == 'count'){
                          count = result['count']
                          control_robot(result)}
                    }
               }
            });
        }
    
    else if(request.method == 'GET') {
        console.log("SHOWPAGE"); 
        showPage(response, pathName)
    }

   }


//TODO bot control app server를 따로 만들어야함!

function control_robot(x, y){
    load_start_time = parseFloat(Date.now())
    setTimeout(function(){bot_move.click(x, y)},1000)
    curtime = parseFloat(Date.now())/1000
    load_end_time = parseFloat(Date.now()) 
    load_time = (load_end_time - load_start_time)
    console.log("load_time: "+load_time)
    console.log("curtime:"+curtime)
    csv_data.push({'x-axis': x, 'y-axis': y, 'curtime': curtime-start_time, 'load-time':load_time})
    bot_move_time += 1000
}

function robot_control(x, y){
  bot_move.click(x, y);


}

String.prototype.format = function(){
  a = this;
  for (k in arguments){
    a = a.replace("{"+k+"}", arguments[k])
    }
  return a
}


function write_csv2(device, appname){
    
    createCsvWriter = csv_writer.createObjectCsvWriter; 

    csvWriter = createCsvWriter({                                       
    path: '/home/kimsoohyun/00-Research/02-Graph/05-data/cut_point/{0}/{1}.csv'.format(device, appname), 
    header: [                                                                   
        {id: 'x-axis', title: 'x-axis'},                                        
        {id: 'y-axis', title: 'y-axis'},                                         
        {id: 'curtime',    title: 'cur_time'},                                  
    ]                                                                           
    });
    csvWriter
        .writeRecords(csv_data)
        .then(()=> console.log('The CSV file was written successfully'));
}


function working(page){
    if(page == 'scene.html'){
    }
    else if(page == 'analysis'){

    }
}


function showPage(response, pathName){
    if(contentMap[pathName]){
        console.log('LOG'+contentMap[pathName]);
        fs.readFile(contentMap[pathName], function(err, data){
                working(pathName)
                send_msg(response, data);
                //response.writeHead(200, {'Content-Type': 'text/html'});
                //console.log(data);
                //response.write(data);
                //response.end();
        });
    }
    else{
        response.writeHead(404, {'Content-Type': 'text/html'})
        response.write('404 Page not found');
        response.end();
        }
  }


function send_msg(response,data){
    response.writeHead(200, {'Content-Type': 'text/html'});         
    console.log(data);                                              
    response.write(data);                                           
    response.end(); 
}


function send_json_msg(response, data){
    response.writeHead(200, {'Content-Type': 'text/html'});         
    console.log("TEST!")
    str_data = JSON.stringify(data)
    console.log(str_data);                                              
    response.write(str_data);                                           
    response.end(); 
}
