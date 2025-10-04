


## Создать Dev App в Telegram

1. Зайти на сайт https://my.telegram.org/ через мобильное устройство (_рекомендуется_)
2. Нажать создать приложение и заполнить форму
```
App title: Demo Message Listener
Short name: demomsglistener
URL: [оставить пустым]
Platform: Desktop
Description: [оставить пустым]
```
3. Нажать "**Create application**" и сохранить `api_id` и `api_hash`



### Узнать `chat_id` для необходимого чата 

1. Найти бота в Telegram `@RawDataBot`.
2. Выбрать в боте личные сообщения или бота
3. Бот вернет `chat_id`



## Создание Shortcut

Запустить приложение `Shortcuts`.

### Шаг 1. Создать новый shortcut
1. В приложении `Shortcuts` нажмите кнопку `+` в верхней панели инструментов 
2. Откроется пустой редактор shortcut с названием "**Untitled Shortcut**"

### Шаг 2. Назвать shortcut
1. Кликните на "**Untitled Shortcut**" или "**Shortcut Name**" вверху окна
2. Введите имя: `Notify Telegram Message`
3. Нажмите _Enter_

### Шаг 3. Настроить прием входящих данных
1. В правой панели найдите иконку ⓘ (Details) и кликните на неё 
2. Включите переключатель "**Use as Quick Action**" (для запуска из других приложений)
3. В разделе "**Receives**" выберите "**Text**" из выпадающего списка 
4. Закройте панель Details


//TODO
Добавить содержание Shortcut