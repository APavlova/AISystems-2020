const month = Object.freeze({"январь":1, "февраль":2, "март":3, "апрель":4, "май":5, "июнь":6, "июль":7,
  "август":8, "сентябрь":9, "октябрь":10, "ноябрь":11, "декабрь":12});

let treedata = {
  name: "Направления",
  children: [
  	{
  		name:"Активный отдых",
  		children:[
  			{
        name:"Походы по России", 
        children:[
          {
          name:"Горные походы", 
          children:[
            {
              name:"Хибины",
              visa:false,
              temperature:-20,
              hotel:2000,
              tickets:5000,
              rating: 7.5,
              season:"март"
            },
            {
              name:"Эльбрус",
              visa:false,
              temperature:-25,
              hotel:3000,
              tickets:6000,
              rating: 7,
              season:"июнь"
            },
          ]},
          {
          name:"Водные походы",
          children:[
            {
              name:"Шуя",
              visa:false,
              temperature:10,
              hotel:0,
              tickets:3000,
              rating: 7.5,
              season:"май"
            },
            { 
              name:"р. Катунь",
              visa:false,
              temperature:-25,
              hotel:0,
              tickets:4000,
              rating: 7.5,
              season:"июнь"
            },
            {
              name:"р. Уксанйоки",
              visa:false,
              temperature:8,
              hotel:0,
              tickets:3000,
              rating: 8,
              season:"май"
            },
            {
              name:"р. Мста",
              visa:false,
              temperature:12,
              hotel:0,
              tickets:1000,
              rating: 6.5,
              season:"май"
            },
            {
              name:"р. Кереть",
              visa:false,
              temperature:11,
              hotel:0,
              tickets:800,
              rating: 7,
              season:"июнь"
            },
            {
              name:"р. Тверца",
              visa:false,
              temperature:11,
              hotel:0,
              tickets:800,
              rating: 6,
              season:"май"
            },
            {
              name:"Белое Море",
              visa:false,
              temperature:15,
              hotel:0,
              tickets:3500,
              rating: 9,
              season:"июль"
            },
            {
              name:"Ладожское озеро",
              visa:false,
              temperature:19,
              hotel:0,
              tickets:3000,
              rating: 9,
              season:"август"
            },
          ]},/*
          {
          name:"Пешие походы",
          children:[
            {name:"Байкал"},
            {name:"Камчатка"},
            {name:"Алтай"},
            {name:"Ергаки"},
            {name:"Колвицкие тундры"},
            {name:"Паанаярви"}
          ]},
        ]},
  			{
        name:"Горные лыжи/Сноуборд",
        children:[
            {
            name:"Россия",
            children:[
              {name:"Роза Хутор (Сочи)"},
              {name:"Бобровый лог (Красноярск)"},
              {name:"Сорочаны (Московская область)"},
              {name:"Игора (Ленинградская область)"},
              {name:"Большой Вудъявр (Мурманская область)"},
              {name:"Домбай (Кавказ)"}
            ]},
            {
            name:"Финляндия",
            children:[
              {
                name:"Рука",
                visa:true,
                temperature:-1,
                hotel:4000,
                tickets:12000,
                rating: 9,
                season:"март"
              },
            ]},
            {
            name:"Швеция",
            children:[
              {name:"Оре"},
            ]},
            {
            name:"Франция",
            children:[
              {name:"Шамони"},
              {name:"Аворья"},
              {name:"Ливиньо"},
              {name:"Сен-Жерве-ле-Бен"}
            ]},
            {
            name:"Италия",
            children:[
              {name:"Ливиньо"}
            ]},
            {
            name:"Швейцария",
            children:[
              {name:"Церматт"},
              {name:"Санкт-Мориц"}
            ]}
          ]},
        {
        name:"Трофи",
        children:[
            {
            name:"Россия",
            children:[
              {name:"п-ов Рыбачий"}
            ]},
          ]},
  	]},
  	{
      name:"Пляжный отдых",
      children:[
          {
          name:"Россия", 
          children:[
            {
            name:"Сочи",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Крым",
            children:[
              {name:"Алушта"},
              {name:"Евпатория"},
              {name:"Ялта"},
              {name:"Гурзуф"},
              {name:"Коктебель"},
              {name:"Балаклава"},
              {name:"Керчь"}
            ]},
            {
            name:"Краснодарский край",
            children:[
              {name:"Анапа"},
              {name:"Ейск"},
              {name:"Небуг"},
              {name:"Лазаревское"},
              {name:"Новороссийск"},
              {name:"Геленджик"},
            ]},
          ]},
          {
          name:"Тропические страны",
          children:[
            {
            name:"Мальдивы",
            children:[
              {name:"Южный Мале"},
              {name:"Маафуши"},
              {name:"Атол Ваадху"},
              {name:"Атолл Ари"},
              {name:"Атолл Лавиани"},
              {name:"Атолл Раа"},
            ]},
            {
            name:"Филлипины",
            children:[
              {name:"Эль-Нидо"},
              {name:"Боракай"},
              {name:"Себу и Бохол"},
            ]},
            {
            name:"Шри-Ланка",
            children:[
              {name:"Тринкомале"},
              {name:"Унаватуна"},
              {name:"Хиккадува"},
            ]},
            {
            name:"Куба",
            children:[
              {name:"Гавана"},
              {name:"Варадеро"},
            ]},
            {
            name:"Доминикана",
            children:[
              {name:"Пунта Кана"},
              {name:"Бока-Чика"},
              {name:"Ла Романа"},
              {name:"Санто-Доминго"},
              {name:"Кап Кана"}
            ]},
            {
            name:"Гавайи",
            children:[
              {name:"Оаху"},
              {name:"Молокаи"},
            ]}
          ]},/*
          {
          name:"Европейские страны",
          children:[
            {
            name:"Испания",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Португалия",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Греция",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Черногория",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Италия",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]},
            {
            name:"Франция",
            children:[
              {name:"Сочи"},
              {name:"Адлер"},
              {name:"Дагомыс"},
              {name:"Лазаревское"}
            ]}*/
          ]}
    ]}
  ]
}