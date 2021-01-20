//Ранжированный поиск                             //false если только без визы
function range_search(tree, t1, t2, cost1, cost2, visa, days, season) {
  let list=[];
  let toRemove=['Хибины'];//здесь должен быть список от пользователя того, что нужно не показывать.

  list_prepare(tree, list, t1, t2, cost1, cost2, visa, days, season);
  //console.log('range_search');

  list.sort((a, b) => a.range>b.range ? 1 : -1);
  
  let res = list.filter( el => toRemove.findIndex(function (element, index, array) {
                                return (element == el.name)
                              }));
  return res;

}


function get_cost(x, days)
{
  return x.tickets + x.hotel*days;
}

function list_prepare(tree, list, t1, t2, cost1, cost2, visa, days, season)
{
 let t=tree;
 let range_diff, cost; // накапливаем здесь баллы НЕсоответствия с поисковым запросом

 if(Array.isArray(t.children))
    for(let i=0; i<t.children.length; i++)
      list_prepare(t.children[i], list, t1, t2, cost1, cost2, visa, days, season);
 else{
  range_diff=0;
  cost = t.data.tickets + t.data.hotel*days;

  if(!(visa^t.data.visa))
    range_diff+=100000;

  if (!((cost >= cost1) && (cost <= cost2))) {
    range_diff+=Math.min(Math.abs(cost1 - cost), Math.abs(cost2 - cost))
  }
  if (!((t.data.temperature >= t1) && (t.data.temperature <= t2))) {
    range_diff+=(Math.min(Math.abs(t1 - t.data.temperature), Math.abs(t2 - t.data.temperature))*100); 
    //*100 для того чтобы выровнять влияние на выдачу со стоимостью, т.к. порядки чисел очень разные
  }
  if (!(month[t.data.season] == season)) {
    range_diff+=(Math.abs(season - month[t.data.season])*1000); 
  }

  range_diff+=((10-t.data.rating)*100);
  //console.log(range_diff);
  list.push({name:t.data.name, range:range_diff});
  }  
}
 //Получает список всех листьев
  function get_all(tree, list){
  let t=tree;

  if(Array.isArray(t.children))
   for(let i=0; i<t.children.length; i++)
    get_all(t.children[i], list);
  else{
   list.push(t.data.name);
  }
 } 

// Поиск по листьям по имени - возвращает лист дерева(структурой), если он найден
function find_by_name(name, tree_root) {
  let t = tree_root;
  let res;

  if (Array.isArray(t.children)){
    for (let i = 0; i < t.children.length; i++)
      if(res === undefined)
        res = find_by_name(name, t.children[i]);
  }
  else {
    if (name === t.data.name){ 
      res = t;
    }
  }
  return(res);
}
// Для сортировки
function byField(field) {
  return (a, b) => a[field] < b[field] ? -1 : 1;
 }

/* Эвклид */
//Поиск эвклидова расстояния между двумя листьями
function evklid(x, y){
  let res=0;

  //по всем числовым атрибутам
  res+=Math.pow(x.temperature - y.temperature, 2);
  res+=Math.pow(x.hotel - y.hotel, 2);
  res+=Math.pow(x.tickets - y.tickets, 2);
  res+=Math.pow(x.rating - y.rating, 2);
  return Math.sqrt(res);
 }

 //Поиск эвклидова расстояния от листа х до всех остальных листьев дерева и формирование cписка
 function evklid_list(x, tree, list){
 let leave = {name:"", val:0};
 let t=tree;

 if(Array.isArray(t.children))
    for(let i=0; i<t.children.length; i++)
      evklid_list(x, t.children[i], list);
 else{
  leave.name = t.data.name;
  leave.val = evklid(x, t.data);
  list.push(leave);
  }
 }

 /* Близость по дереву */
 //Находит список объектов, сортированных по удаленности от одного объекта d
 function proximity_list(d, list, proximity_it) {

  let p = d.parent;

  proximity_it++;

   if(p && Array.isArray(p.children)){

    for(let i=0; i<p.children.length; i++) {
     let child = p.children[i];
     if(d.data.name != child.data.name){
      near(p.children[i], list, proximity_it);
     }
    }
   }

   if (p)
    proximity_list(p, list, proximity_it);
 }

 //Идет в глубину дерева, записывает удаленность листов к объекту в список
 function near(child, list, proximity_it){

  if(Array.isArray(child.children)){
   proximity_it++;
   for(let j=0; j<child.children.length; j++)
    near(child.children[j], list, proximity_it);
  }
  else
     list.push({name:child.data.name, val:proximity_it});
 }

//Находит степень удаленности х от у по дереву
 function count_proximity(x, y){
  var list = [];
  proximity_list(x, list, 0);
  if (list[list.findIndex(el => el.name === y.data.name)] != undefined)
   return list[list.findIndex(el => el.name === y.data.name)].val;
  return 0;
 }

 //Находит близость расположения объектов к объекту x и записывает в лист
 function differences_list(x, tree, list){

   let t = tree;
   if(Array.isArray(t.children))
    for (let i = 0; i < t.children.length; i++)
     differences_list(x, t.children[i], list);
   else{
    list.push({name: t.data.name, val: count_differences(x, t.data)});
   }
 }

 /*Количество отличий*/
 //Находит количество отличий между объектами x и y
  function count_differences(x, y){
    let diff_sum = 0;

    if (x.temperature != y.temperature) diff_sum+=1;
    if (x.visa != y.visa) diff_sum+=1;
    if (x.hotel != y.hotel) diff_sum+=1;
    if (x.tickets != y.tickets) diff_sum+=1;
    if (x.season != y.season) diff_sum+=1;
    if (x.rating != y.rating)diff_sum+=1;

    return diff_sum;
 }

 //Считает признаки, которых нет в y, но есть в x
 function count_one_side_differences(x, y, features_x){
  let diff_sum = 0;

  for(let i=0; i<features_x.length; i++)
   if(y[features_x[i]] == null)
    diff_sum++;

   return diff_sum;
 }

 //Получает характеристики (исключая имя - идентификатор)
 function get_features(x){
    return Object.keys(x).filter((n) => {return n != "name"});
 }

/*Корреляция*/
 function correlation_list(x, tree, root, list){
  let t = tree;

   if(Array.isArray(t.children))
    for (let i = 0; i < t.children.length; i++)
     correlation_list(x, t.children[i], root, list);
   else{
    list.push({name: t.data.name, val: correlation(x, t, root)});
   }
 }

 function correlation(x, y, tree){
  let f_x = get_features(x.data);
  let avg, x_i, y_i;
  let sum_num = 0;
  let sum_den_1 = 0;
  let sum_den_2 = 0;
  let coef = 0;

  //Для каждого признака
  for(let i=0; i<f_x.length; i++){

   x_i = x.data[f_x[i]];
   y_i = y.data[f_x[i]];

   //Если у двоих объектов есть признак - считаем значения для рассчета коэфф корреляции
   if(y_i != null && typeof(y_i) == "number"){

    avg = find_avg(f_x[i], tree);

    sum_num += (x_i - avg)*(y_i - avg);
    sum_den_1 += (x_i - avg)**2;
    sum_den_2 += (y_i - avg)**2;
   }
  }

  //Рассчитываем коэфф корреляции
  coef = sum_num/(Math.sqrt(sum_den_1) * Math.sqrt(sum_den_2));
  return coef;
 }

 //Находит значения поля в дереве и записывает в список
 function count_feature_val(feature, tree, list){
  let t = tree;

  if(Array.isArray(t.children))
   for(let i=0; i<t.children.length; i++){
    count_feature_val(feature, t.children[i], list);
   }

  if(t.data[feature] != null) {
     list.push(t.data[feature]);
  }
 }

 //Находит среднее значение поля во всем дереве
  function find_avg(feature, tree){
   let list = [];
   count_feature_val(feature, tree, list);
   return list.reduce((a, b) => (a + b)) / list.length;
 }

//Находит близость расположения объектов к объекту x и записывает в список
 function recommendation_list(x, tree, list){

   let t = tree;
   if(Array.isArray(t.children))
    for (let i = 0; i < t.children.length; i++)
     recommendation_list(x, t.children[i], list);
   else
    list.push({name: t.data.name, val:recommend_coeff(x,t)});
 }

//Находит список соседних листов (группу)
 function collab_list(x, tree){
  List=[];
  proximity_list(x, List, 0);
  return List.filter(item => item.val == 1);
 }

 function recommend_coeff(x,y){
  return (8*count_differences(x.data,y.data) + 0.0001*evklid(x.data,y.data) + count_proximity(x,y)) + (-10)*correlation(x,y,root);
 }

  function find_common(list1, list2, res){

  //Для каждого элемента первого списка 1
  for(let i = 0; i < list1.length; i++){

   //Если найдено совпадение - добавить в лист результата или увеличить его значение
   let i_2=list2.findIndex(el => el.name === list1[i].name);
   if (list2[i_2]!=undefined){

    let i_r = res.findIndex(el => el.name === list1[i].name)
    if (res[i_r]!=undefined){
     res[i_r].val = (res[i_r].val + list2[i_2].val)/2;
    }
    else{
     res.push({name: list1[i].name, val: (list1[i].val + list2[i_2].val)/2});
    }
   }
  }
 }

  function del_el(list, name){
  return list.filter(item => item.name !== name);
 }

 function get_common_recomendations(list_of_list){
  let top_list=[];
  let bottom_list=[];
  //Для каждого листа из списка
  for(let i=0; i<list_of_list.length; i++){

   //Перебираем все остальные листы, начиная с текущего
   for(let j=i+1; j<list_of_list.length; j++){

    //Ищем одинаковые, составляем верхушку рекомендации
    find_common(list_of_list[i], list_of_list[j], top_list);
   }
   bottom_list = bottom_list.concat(list_of_list[i]);
  }

  //Сортируем пересекающиеся рекомендации в порядке убывания (чем больше значение, тем чаще встр => выше в списке)
  top_list.sort((a, b) => a.val > b.val ? 1 : -1);
  
  //Добавляем к ним остальные списки, в порядке их оценки
  let common=[];

  find_common(bottom_list, top_list, common);
  bottom_list = bottom_list.filter(x => !common.some(y => x.name === y.name));

  bottom_list.sort((a, b) => a.val > b.val ? 1 : -1);
  top_list = top_list.concat(bottom_list);

  return top_list;
 }
