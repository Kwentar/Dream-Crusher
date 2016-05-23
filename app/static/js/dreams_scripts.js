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
  $('.table-remove').click(function () {
    $(this).parents('tr').detach();
  });

  $('.table-up').click(function () {
    var $row = $(this).parents('tr');
    if ($row.index() === 1) return; // Don't go above the header
    $row.prev().before($row.get(0));
  });

  $('.table-down').click(function () {
    var $row = $(this).parents('tr');
    $row.next().after($row.get(0));
  });
});