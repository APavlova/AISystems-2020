
$(document).ready(function() {

  $('#go_collab').click(function () {
    var a=$('#hist-list input:checked'); //Выбираем все отмеченные checkbox
    var checked=[];
    for (var x=0; x<a.length;x++){
      checked.push(a[x].value);
    }
    //console.log(checked);

    //Собираем массив массивов рекомендаций для каждого выделенного объекта
    var list_of_lists=[];

    for (let i=0; i<checked.length; i++){
       let list=[];
       let wrk_leave = find_by_name(checked[i], root);
       recommendation_list(wrk_leave, root, list);
       list.sort((a, b) => a.val > b.val ? 1 : -1);
       list_of_lists.push(list);
    }
    var recom_list=get_common_recomendations(list_of_lists); //рекомендации без учета удаленных

    var d=$('#del-list input:checked'); //Выбираем все отмеченные checkbox
    var del=[];
    for (var x=0; x<d.length;x++){
      del.push(d[x].value);
    }
    for (let i=0; i<del.length; i++){
        recom_list = del_el(recom_list, del[i]);
    }
    recom_list.slice(10);
    //console.log(recom_list); //рекомендации с учетом удаленных

    var txt="<b>Результат для";
    checked.forEach(function(item, i, arr){
      txt = txt + ' ' + item + ',';
    });

    txt = txt.substr(0, txt.length-1) + ':</b>' + '<br/>';

    recom_list.forEach(function(item, i, arr){
      txt = txt+'<br/>'+ (i+1) + '. ' + item.name;
    });

    $('#res3').html(txt);
   });

  //Параметрический поиск
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
        txt = txt+'<br/>'+ (i+1) + '. ' + item.name;
      });
      $('#res2').html(txt);
  });

  //Поиск расстояний
  $("#go_button").click(function(){
    var method = $('input[name="method"]:checked').val();
    var name = $('input[name="leave"]').val();
    //name = name.charAt(0).toUpperCase() + name.slice(1);
    
    let e_list = [];
    let wrk_leave = {};
    wrk_leave = find_by_name(name, root);

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

  //Движочки для поиска
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

  });

  //Чекбоксы для коллаб поиска
  $( function(){
      let list = [];
      get_all(root, list);

      let txt='';
      //console.log(list);

      list.forEach(function(item, i, arr){
        //console.log(item);
        txt = txt + 
            '<div>' +
            '  <input class="hist-check" type="checkbox" value="' + item + '">'+
            '  <label class="hist-check-label">' + item + '</label>'+
            '</div>';
      });

      $('#hist-list').html('<b>Выберите элементы для истории:</b>' + txt);
      $('#del-list').html('<b>Выберите нежелательные элементы:</b>' + txt);
   });

  $("#calc_btn").click(function(){
    $("#calc").css('display', 'flex');
    $("#search").hide();
    $("#collab").hide();
    $("#content").hide();
  });

  $("#search_btn").click(function(){
    $("#calc").hide();
    $("#search").css('display', 'flex');
    $("#collab").hide();
    $("#content").hide();
  });

  $("#collab_btn").click(function(){
    $("#calc").hide();
    $("#search").hide();
    $("#collab").css('display', 'flex');
    $("#content").hide();
  });

  $("#cont_btn").click(function(){
    $("#calc").hide();
    $("#search").hide();
    $("#collab").hide();
    $("#content").css('display', 'flex');
  });
});