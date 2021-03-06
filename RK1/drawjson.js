 let width = 1500;
 let data = treedata;

//Красивый вывод подписей к узлам диаграммы
function get_atr(d, str){
  let title;

  if (d !== undefined){
   if (typeof(d) == 'boolean'){
    if (d)
      title = str + 'Да';
    else
      title = str + 'Нет';
   }
   else
    title = str + d;
  }
  else 
   title = '';

  return title;
 }

 let tree = data => {
  const root = d3.hierarchy(data);
  root.dx = 120;
  root.dy = width / (root.height+1);
  return d3.tree().nodeSize([root.dx, root.dy])(root);
  }

  const root = tree(data);

  let x0 = Infinity;
  let x1 = -x0;

  root.each(d => {
    if (d.x > x1) x1 = d.x;
    if (d.x < x0) x0 = d.x;
  });

  var bodySelection = d3.select("body");
  var svg = bodySelection.append("svg")
                                 .attr("width", width)
                                 .attr("height", x1 - x0 + root.dx * 2);
  const g = svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("transform", `translate(${root.dy / 3},${root.dx - x0})`);
    
  const link = g.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5)
  .selectAll("path")
    .data(root.links())
    .join("path")
      .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x));
  
  const node = g.append("g")
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
    .selectAll("g")
    .data(root.descendants())
    .join("g")
      .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

  node.append("text")
      .attr("dy", "0.31em")
      .attr("font-weight", "bold")
      .attr("font-size", "12")
      .attr("x", d => d.children ? -6 : 6)
      .attr("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name)
  
  //виза
    node.append("text")
        .attr("dy", "1.91em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.visa, 'Нужна виза: '))
  //температура
    node.append("text")
        .attr("dy", "3.21em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.temperature, 'Температура в высокий сезон: '))
  //стоимость отеля
    node.append("text")
        .attr("dy", "4.51em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.hotel, 'Стоимость отелей(руб/сут): '))
  //билеты
    node.append("text")
        .attr("dy", "5.81em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.tickets, 'Стоимость билетов: '))
  //сезон
    node.append("text")
        .attr("dy", "7.11em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.season, 'Высокий сезон: '))
  //рейтинг
    node.append("text")
        .attr("dy", "8.41em")
        .attr("x", d => d.children ? -6 : 6)
        .attr("text-anchor", d => d.children ? "end" : "start")
        .text(d => get_atr(d.data.rating, 'Рейтинг: '))

    .clone(true).lower()
      .attr("stroke", "white");