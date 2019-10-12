$( document ).ready(function() {
    $.post("/dwell", function(result){
      $("#dwell_time").html(result.dwell_time);
    });
  $.post("/unique_visitors", function(result){
    $("#unique_visitors").html(result.unique_visitor_count);
    });
});

$( document ).ready(function() {
  $("#submit").click(function() {
    $.post("/search",
    {
      data: $("#search").val()
    },
    function(result){
      $("#num_entries").html(result.mac_count);
    });
  });
});

function updateValues() {
  $.post("/current_devices", function(result){
      $("#current_device_count").html(result.current_device_count);
    });
  $.post("/repeat_devices", function(result){
    $("#repeat_device_count").html(result.repeat_device_count);
    });
};

$( document ).ready(function() {
    updateValues();
    setInterval(function() {updateValues()}, 60000);
});
