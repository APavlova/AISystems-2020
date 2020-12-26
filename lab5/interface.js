
$(document).ready(function() {
  $("#calc_btn").click(function(){
    $("#calc").show();
    $("#search").hide();
  });

  $("#search_btn").click(function(){
    $("#calc").hide();
    $("#search").show();
  });

  $("#go_search").click(function(){
    let t1 = $( "#temp" ).slider( "values", 0 );
    let t2 = $( "#temp" ).slider( "values", 1 );
    let cost1 = $( "#cost" ).slider( "values", 0 );
    let cost2 = $( "#cost" ).slider( "values", 1 );
    let days = $('input[name="days"]').val();
    
    let visa = false;
    if ($('#visa').is(':checked'))
      visa = true;

    let e_list = range_search(root, t1, t2, cost1, cost2, visa, days, 5);

    let txt="Результат:<br/>";
      e_list.forEach(function(item, i, arr){
        txt = txt+'<br/>'+item.name+': '+item.range;
      });
      $('#res2').html(txt);
  });

  $("#go_button").click(function(){
    var method = $('input[name="method"]:checked').val();
    var name = $('input[name="leave"]').val();
    //name = name.charAt(0).toUpperCase() + name.slice(1);
    
    let e_list = [];
    let wrk_leave = {};
    wrk_leave = find_by_name(name, root);

    //!
    range_search(root, 15, 28, 0, 100000, false, 10, 3);

    if(wrk_leave !== undefined){
      switch(method) {
        case 'evklid': 
          evklid_list(wrk_leave.data, root, e_list);          
        break;
        case 'difference': 
          differences_list(wrk_leave.data, root, e_list);          
        break;
        case 'tree': 
          proximity_list(wrk_leave, e_list, 0);          
        break;
        case 'korrel': 
          correlation_list(wrk_leave, root, root, e_list);          
        break;
      } 

      console.log(e_list);
      
      e_list.sort((a, b) => a.val > b.val ? 1 : -1);

      let txt="Результат:<br/>";
      e_list.forEach(function(item, i, arr){
        txt = txt+'<br/>'+item.name+': '+item.val;
      });
      $('#res').html(txt);
    }
    else
      $('#res').text('Результат: такой лист дерева не найден');
 
  }); 

  $( function() {
    $( "#cost" ).slider({
      range: true,
      min: 0,
      max: 500000,
      values: [ 1000, 30000 ],
      slide: function( event, ui ) {
        $( "#cost_lbl" ).text( "Стоимость отдыха: " + ui.values[ 0 ] + " - " + ui.values[ 1 ] + " руб" );
      }
    });
    $( "#cost_lbl" ).text( "Стоимость отдыха: " + $( "#cost" ).slider( "values", 0 ) + " - " + $( "#cost" ).slider( "values", 1 ) + " руб" );

    $( "#temp" ).slider({
      range: true,
      min: -30,
      max: 40,
      values: [ 15, 28 ],
      slide: function( event, ui ) {
        $( "#temp_lbl" ).text( "Температура: " + ui.values[ 0 ] + " - " + ui.values[ 1 ] + " С" );
      }
    });
    $( "#temp_lbl" ).text( "Температура: " + $( "#temp" ).slider( "values", 0 ) + " - " + $( "#temp" ).slider( "values", 1 ) + " С" );

  } );
});