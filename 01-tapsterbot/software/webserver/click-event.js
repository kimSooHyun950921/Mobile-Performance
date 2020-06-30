var bot = require('../src/bot.js');  
var waitSync = require('wait-sync');  


function generate_random_number(max_value){                       
    random = Math.floor(Math.random() * (2*max_value+1)) - max_value  
    return random  
}          


function random_move(x, y){
    x = generate_random_number(20)
    y = generate_random_number(50)
    console.log("좌표: "+x+", "+y)
    click(x, y)
 }


function click(x, y){
     bot.go(x, y, -120);
     waitSync(0.2);
     bot.go(x, y, -143);
     waitSync(0.15);
     back(x, y);
     console.log("CLICK BYE");
 }


function back(x, y){
    bot.go(x, y, -125);
    waitSync(0.15)
    bot.go(0, 0, -125);
}


function swipe_right(x, y){
    click(x+3, y);
    waitSync(0.15);
    bot.go(x, y, -143);
    back(x, y)
}


function swipe_left(x, y){
    click(x-3, y);
    waitSync(0.15);
    bot.go(x, y, -143);
    back(x, y);
}


function swipe_up(x, y){
    click(x, y+3);
    waitSync(0.15);
    bot.go(x, y, -143);
    back(x, y);
}


function swipe_down(x, y){
    click(x, y-3);
    waitSync(0.15);
    bot.go(x, y, -143)
    back(x, y);
 }


function long_click(x, y){
    click(x, y);
    waitSync(4);
    back(x, y);
}


module.exports = {
    move,
    click,
    back,
    swipe_left,
    swipe_right,
    swipe_up,
    swipe_down,
    long_click
}
