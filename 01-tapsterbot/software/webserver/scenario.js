var http = require('http');
var url = require('url');
var fs = require('fs');
var bot = require('../src/bot.js');
var waitSync = require('wait-sync');
var csv_writer = require('csv-writer');
var bot_move = require('./click-event.js');
const { parse } = require('querystring');
const { cors } = require('cors');

http.createServer(onRequest).listen(8888);
console.log('another server opened');


var csv_data = [];

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
  response.on('data', function(chunk){
    str += chunk
  });
  response.on('end', function(){
    console.log(str);
    var obj = JSON.parse(str);
    var box_list = obj.box;
    console.log(Array.isArray(box_list))
    for(i = 0; i<box_list.length; i++){
      elem = box_list[i]
      elem_x = (elem[0] + elem[1]) / 2
      elem_y = (elem[2] + elem[3]) / 2
      bot_move.click(0, 0);

    }
  });
}
var predict_req = http.request(predict_options, predict_callback);

var req = http.request(options, function(res) {
    res.setEncoding('utf8')
    var responseString = "";

    res.on("data", function (data) {
        responseString += data;
    });
    res.on("end", function (){
        console.log("TEST!");
        console.log(responseString)
    });

});


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


function onRequest(request, response){
    var pathName = url.parse(request.url).pathname;
    console.log('method: ')
    console.log(request.method)
    if(request.method == 'POST'){
        data = 'recording'
        req.write(data)


        collectRequestData(request, result => {
                var post_data_key = Object.keys(result);
                for(var item of post_data_key){
                    console.log('item'+item.toString())
                    if(item.toString() == 'starttime'){
                      start_time = result['starttime'];
                      send_msg(response, "OK");
                      http.request(predict_options, predict_callback).end()
                      }
                    else if(item.toString() == 'count'){
                        count = result['count']
                        control_robot(result)}

                    else if (item.toString() == 'xy-axis'){
                        json_xy = result['xy-axis']

                        xy = JSON.parse(json_xy)
                        appname = xy.appname
                        x_axis = parseInt(xy.x, 10)
                        y_axis = parseInt(xy.y, 10)

                        console.log(appname, x_axis, y_axis)
                        //control_robot(result)
                        bot_move.click(x_axis, y_axis)
                        console.log("BOT MOVE BYE");
                        send_msg(response, "OK");
                    }
                }
            });
        }
    
    else{
        showPage(response, pathName)
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

        console.log("load_time: "+load_time)
        console.log("curtime:"+curtime)
        csv_data.push({'x-axis': x, 'y-axis': y, 'curtime': curtime, 'load-time':load_time})

        waitSync(2)}

        write_csv()
}




function write_csv(){
    
    var createCsvWriter = csv_writer.createObjectCsvWriter; 
    var csvWriter = createCsvWriter({                                       
    path: '/home/kimsoohyun/00-Research/02-Graph/05-data/cut_point/cut_info.csv', 
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
    console.log("TEST!")
    console.log(data);                                              
    response.write(data);                                           
    response.end(); 
}
