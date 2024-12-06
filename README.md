## Модуль реализующий клиент для работы с api сервиса kaspersky antivirus multiscaner

## Установка модуля

Установка осуществляется ввиде whl-пакета
*pip install pykavms --extra-index-url http://**token**:<your\_personal\_token>@gitlab.cloud.gcm/api/v4/projects/549/packages/pypi/simple*

* При использовании как зависимость в *requirements.txt* необходимо добавить в него

```
--trusted-host gitlab.cloud.gcm
--extra-index-url http://gitlab.cloud.gcm/api/v4/projects/549/packages/pypi/simple
pykavms>=1.0.0
```

## Модуль состоит из:

* AVMScaner - клиентский класс для работы с мультисканером
* AVMSAnalize - класс для работы с результатом сканирования
* AVMSSummaryReport - класс для работы с кратким отчетом
* AVMSFullReport - класс для работы с полным отчетом

## Пример испольования

```

```

Чтобы протестировать наглядно результат работы с api нужно запустить файл main.py

## Просмотр документации к модулю после его локальной установки

python -m pydoc

## Сборка и выпуск новой версии 
python3 setup.py  bdist_wheel
python3 -m twine upload --verbose --config-file ./.pypirc -r gitlab dist/*