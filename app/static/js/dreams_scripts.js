$(document).ready(function() {
    var $SLOGAN_EDIT = $('#slogan_text');
    $SLOGAN_EDIT.focusout(function() {
    var CSRF_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_token)
            }
        }
    })
     $.ajax({
            url: '/change_slogan',
            data: {'slogan_value': $SLOGAN_EDIT.val()},
            type: 'POST',
            success: function(response) {
                 console.log(response);
            },
            error: function(error) {
                 console.log(error);

            }
        });
    });

});

function add_half_hour(dream_id) {
    var $TABLE = $('#dream_table');
    var $week_number = $('#week_number');
    var $TABLE_DAYS = $('#day_table');
    var $TABLE_WEEK = $('#dream_table_week_' + $week_number.html());
    var CSRF_token = $('meta[name=csrf-token]').attr('content');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_token)
            }
        }
    })
    $.ajax({
            url: '/add_half_hour',
            data: {'dream_id': dream_id},
            type: 'POST',
            success: function(response) {
                 var $tr = $TABLE.find('tr.' + dream_id);
                 var $td_cur = $tr.find('td.index_dream_current_time');
                 var $td_est = $tr.find('td.index_dream_estimated_time');
                 var $td_percent = $tr.find('td.index_dream_percent');
                 var $week_tr = $TABLE_WEEK.find('tr.' + dream_id);
                 var $week_td_cur = $week_tr.find('td.index_dream_current_time');
                 var $tr_day = $TABLE_DAYS.find('tr.day_table_days')
                 var $td_day = $tr_day.find('td.day_table_' + response.day_number)
                 $td_cur.html(parseInt($td_cur.html(), 10) + 1);
                 $td_day.html(parseInt($td_day.html(), 10) + 1);
                 $week_td_cur.html(parseInt($week_td_cur.html(), 10) + 1);
                 $td_percent.html((parseInt($td_cur.html(), 10) / parseInt($td_est.html(), 10) * 100).toFixed(2) + '%' );
                 console.log(response);
            },
            error: function(error) {
                 console.log(error);

            }
        });
    };
