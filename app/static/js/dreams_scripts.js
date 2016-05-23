$(document).ready(function() {
  var $TABLE = $('#table');

    $('.table-add').click(function () {
        var $rowCount = $TABLE.find('tr').length;
        if($rowCount < 5) {
            var $clone = $TABLE.find('tr.hide').clone(true).removeClass('hide table-line');
            $TABLE.find('table').append($clone);
        }
        else {
            alert("You can have only 3 dreams for one month, sorry =(")
        }
    });
});