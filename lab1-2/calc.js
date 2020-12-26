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

 //Находит близость расположения объектов к объекту x и записывает в лист
 function differences_list(x, tree, list){

   let t = tree;
   if(Array.isArray(t.children))
    for (let i = 0; i < t.children.length; i++)
     differences_list(x, t.children[i], list);
   else{
    list.push({name: t.data.name, val: count_differences(x, t)});
   }
   //console.log(list.sort(byField('differences_count')));
 }



 /*Количество отличий*/
 //Находит количество отличий между объектами x и y
  function count_differences(x, y){
  let features_x = get_features(x);
  let features_y = get_features(y);

  let diff_sum =
      count_one_side_differences(x, y, features_x) + count_one_side_differences(y, x, features_y);

  for(let i=0; i<features_x.length; i++)
   if(y[features_x[i]] && !_.isEqual(y[features_x[i]], x.data[features_x[i]]))
    diff_sum++;

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

 //Получает список объектов, сортированных по количеству отличий для каждого листа
/* function call_differences_list(tree){
  let t=tree;
  let list = [];

  if(Array.isArray(t.children))
   for(let i=0; i<t.children.length; i++)
    call_differences_list(t.children[i]);
  else{
   differences_list(t, root, list);
   console.log(t.data.name, list);
  }
 }*/

 //Получает список объектов, сортированных по близости для каждого листа
/*  function call_proximity_list(tree){
  let t=tree;
  let list = [];

  if(Array.isArray(t.children))
   for(let i=0; i<t.children.length; i++)
    call_proximity_list(t.children[i]);
  else{
   proximity_list(t, list, 0);
   console.log(t.data.name, list);
  }
 }*/


  //Выводит список объектов с коэффициентами корелляций для каждого листа
/*  function call_correlation_list(tree){
  let t=tree;
  let list = [];

  if(Array.isArray(t.children))
   for(let i=0; i<t.children.length; i++)
    call_correlation_list(t.children[i]);
  else{
   correlation_list(t, root, list);
   console.log(t.data.name, list);
  }
 }*/


/*Корреляция*/
 function correlation_list(x, tree, root, list){
  let t = tree;

   if(Array.isArray(t.children))
    for (let i = 0; i < t.children.length; i++)
     correlation_list(x, t.children[i], list);
   else{
    list.push({name: t.data.name, val: correlation(x, t, root)});
   }
 }

 function correlation(x, y, tree){
  let f_x = get_features(x);
  let avg, x_i, y_i;
  let sum_num = 0;
  let sum_den_1 = 0;
  let sum_den_2 = 0;
  let coef = 0;

  //Для каждого признака
  for(let i=0; i<f_x.length; i++){

   x_i = x[f_x[i]];
   y_i = y[f_x[i]];

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

 //Находит значения поля в дереве и записывает в лист
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