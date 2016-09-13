

function StartTimer() {
    var canvas = document.getElementById("timer"),
        ctx = canvas.getContext('2d');
    canvas.height = 400;
    canvas.width = 400;
    var start_time = Date.now();
    setInterval(function() { Update(canvas.width, ctx, start_time); }, 0);
}


function Update(width, ctx, start_time) {
    DrawWatch(width, ctx, 2*60*1000, start_time);
}

function DrawWatch(width, ctx, max_time, start_time) {
		var current_time = Date.now();
    var diff = current_time - start_time;
    var percent = 1-(max_time-diff)/max_time;
    ctx.beginPath();
    var watch_center_w = width/2;
    var watch_center_h = width/2; // not copypaste
    ctx.fillStyle = '#171717';
    ctx.arc(watch_center_w, watch_center_h, 0.35 * width, 0, 2 * Math.PI, true);
    ctx.fill();

    ctx.beginPath();
    ctx.fillStyle = "rgba(235, 100, 84, 1.0)";
    ctx.arc(watch_center_w, watch_center_h, 0.40 * width, Math.PI*1.5, Math.PI*1.5 + 2 * percent * Math.PI, false);
    ctx.arc(watch_center_w, watch_center_h, 0.3 * width, Math.PI*1.5 + 2 * percent * Math.PI, Math.PI*1.5, true);

    if(max_time-diff < 1000)
    {
        ctx.fillStyle = "rgba(235, 100, 84, " + String((max_time-diff)/1000) + ")";
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