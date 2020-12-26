
$(document).ready(function() {
  $("#go_button").click(function(){
    var method = $('input[name="method"]:checked').val();
    var name = $('input[name="leave"]').val();
    //name = name.charAt(0).toUpperCase() + name.slice(1);
    
    let e_list = [];
    let wrk_leave = {};
    wrk_leave = find_by_name(name, root);

    console.log(method);

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
});