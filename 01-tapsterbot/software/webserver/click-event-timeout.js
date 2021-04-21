var bot = require('../src/bot.js');  
var waitSync = require('wait-sync');  
move = function(x, y, z, when=0){
  setTimeout(function() {bot.moveServosTo(x, y, z)}, when);
}

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


function click(x, y, z = -1, when=0){
     if(z == -1){z = -135;}
     move(x, y, -120,when);
     move(x, y, -138, when+250);
     back(x, y,when+500);
     console.log("CLICK BYE");
 }


function back(x, y, when=0){
    move(x, y, -120, when);
    move(0, 0, -120, when+200);
}


function swipe_right(x, y, when){
    click(x+3, y, when);
    move(x, y, -143, when+250);
    back(x, y, when+250)
}


function swipe_left(x, y){
    click(x-3, y);
    move(x, y, -143);
    move(x, y);
}


function swipe_up(x, y){
    click(x, y+3);
    move(x, y, -143);
    back(x, y);
}


function swipe_down(x, y){
    click(x, y-3);
    move(x, y, -143)
    back(x, y);
 }


function long_click(x, y){
    click(x, y);
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
