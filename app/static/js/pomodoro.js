var count = 0;
var work_time = 1000;
var relax_time = 1000;
var state = 0;
var active = false;
var work_color = "rgba(235, 100, 84,";
var relax_color = "rgba(100, 235, 84,";
var bar_color = work_color;
var interval_Id = 0;
var start_time = 0;
var max_time = work_time;
var canvas = 0;
var ctx = 0;
var count_text = 0;
var dream_selector = 0;

$(window).resize(function() {
     canvas.height = window.innerWidth/2;
    canvas.width = window.innerWidth/2;
    InitCanvasSize();
    DrawEmptyCircle(canvas.width);
});

$(document).ready(function() {
    canvas = document.getElementById("timer_canvas");
    ctx = canvas.getContext('2d');
    count_text = document.getElementById("timer_current_count");
    dream_selector = document.getElementById("timer_current_dream");

    InitCanvasSize();
    DrawEmptyCircle(canvas.width);
    var CSRF_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_token)
            }
        }
    })
});

function InitCanvasSize() {
    var max_size = 800;
    if(window.innerWidth < max_size) {
        max_size = window.innerWidth;
    }
    canvas.height = max_size * 0.7;
    canvas.width = max_size * 0.7;
}

function DrawEmptyCircle(width)
{
    ctx.clearRect(0, 0, width, width);
    ctx.beginPath();
    var watch_center_w = width/2;
    var watch_center_h = width/2; // not copypaste
    ctx.fillStyle = '#171717';
    ctx.arc(watch_center_w, watch_center_h, 0.35 * width, 0, 2 * Math.PI, true);
    ctx.fill();

    ctx.beginPath();
    ctx.fillStyle = "#DDDDE2";
    ctx.arc(watch_center_w, watch_center_h, 0.40 * width, Math.PI * 2, 0, false);
    ctx.arc(watch_center_w, watch_center_h, 0.3 * width, 0, Math.PI * 2, true);
    ctx.fill();
}
function StartTimer() {
    if(!active) {
        active = true;
        start_time = Date.now();
        interval_Id = setInterval(function () {
            Update(canvas.width, ctx);
        }, 10);

    } else {
        active = false;
        clearInterval(interval_Id);
        DrawEmptyCircle(canvas.width);
    }
}



function Update(width, ctx, start_time) {
    DrawWatch(width, ctx);
}

function DrawWatch(width, ctx) {
    var current_time = Date.now();
    var diff = current_time - start_time;
    var percent = 1-(max_time-diff)/max_time;
    var watch_center_w = width/2;
    var watch_center_h = width/2; // not copypaste
    DrawEmptyCircle(width);

    ctx.beginPath();
    ctx.fillStyle = bar_color + "1.0)";
    ctx.arc(watch_center_w, watch_center_h, 0.40 * width, Math.PI*1.5, Math.PI*1.5 + 2 * percent * Math.PI, false);
    ctx.arc(watch_center_w, watch_center_h, 0.3 * width, Math.PI*1.5 + 2 * percent * Math.PI, Math.PI*1.5, true);

    if(max_time-diff < 1000)
    {
        ctx.fillStyle = bar_color + String((max_time-diff)/1000) + ")";
    }
    if(max_time < diff)
    {
        if(state == 0) {
            state = 1;
            max_time = relax_time;
            start_time = current_time;
            count += 1;
            bar_color = relax_color;
            count_text.innerHTML = count;
            var dream_id = dream_selector.options[dream_selector.selectedIndex].value;
            add_half_hour(dream_id);
        } else {
            state = 0;
            max_time = work_time;
            start_time = current_time;
            bar_color = work_color;

        }
    }
    ctx.fill();
    ctx.beginPath();
    ctx.fillStyle = '#AAAAB2';
    var time = diff/1000;
    if (time > 60)
    {
        time = Math.floor(time/60) + ':' + (time % 60).toFixed(0);
    }
    else
    {
        time = time.toFixed(1);

    }
    ctx.textAlign="center";
    ctx.textBaseline = "middle";
    ctx.font='50px Arial';
    ctx.fillText(time,watch_center_w,watch_center_h);
}