# Описание

Тестовое задание на позицию Python Backend Developer в отдел аналитики ДВФУ. 

Необходимо реализовать сервис который сохранял бы в себе данные из нескольких наукометрических 
баз данных и позволял проводить аналитические расчеты над ними

Техническое Задание можно найти [здесь](https://github.com/FEFU-Analytics-Sector/backend-task)

Задание было выполнено с помощью Python 3.10, FastAPI, PostgreSQL, sqlalchemy, и обернуто в docker. 
При сборке docker-compose файла, приложение будет доступно на порту 80, а база данных на порту 29170


# Допущения:

* Мета
    * Количество публикаций автора (document_count) было переименовано в publication_count для 
      большей конкретики
    * Id профилей из датасета были изменены чтобы соответствовать UUID4
* [Модель Profile](##профиль-profilemodel)
    * Также содержит creation_date
* [Метод создания профиля автора](##метод-создания-профиля-автора)
    * Также принимает scientometric_database в параметре пути
    * Если профиль существует - перезаписывает его. Было сделано так для облегчения способа работы,
      так как теперь этот метод еще и обновляет профиль
* [Метод получения списка профилей](##метод-получения-списка-профилей)
    * Для каждого объекта также возвращает profile_id


# Модели в базе данных

## Профиль (Profile):
* profile_id - уникальный UUID4 идентификатор научного сотрудника;
* creation_date - дата создания профиля в БД;
* full_name - ФИО научного сотрудника;
* scientometric_database - источник данных (Scopus, WOS, RISC);
* publication_count - количество публикаций автора;
* citation_count - количество цитирований автора;
* h_index - индекс Хирша, рассчитанный НБД;
* url - ссылка на профиль автора в НБД.


# Методы

## Метод получения профиля сотрудника
```
GET /profiles/{scientometric_database}/{profile_id}

path_params:
* scientometric_database: string enum [Scopus, WOS, RISC]
* profile_id

query_params:
* fields: array of string [publication_count, citation_count] or null

returns:
* Profile:
    * full_name
    * h_index
    * url
    * if specified in fields:
        * publication_count
        * citation_count
```


## Метод получения списка профилей
```
GET /profiles/{scientometric_database}

path_params:
* scientometric_database: string enum [Scopus, WOS, RISC]

query_params:
* page: int (10 elements per page)
* sort_by: string enum [*creation_date*, h_index]
* sort_order: string enum [*ascending*, descending]

returns:
* list of Profiles:
    * profile_id
    * full_name
    * h_index
    * url
```


## Метод создания профиля автора:
```
POST /profiles/{scientometric_database}

path_params:
* scientometric_database: string enum [Scopus, WOS, RISC]

body_params:
* profile_id
* full_name
* publication_count
* citation_count
* h_index
* url

returns:
* profile_id
```


## Метод подсчета статистики публикационной активности
```
GET /analytics/publication_activity

returns:
* scientometric_database: 
    * total_publication_count
    * total_citation_count
    * average_h_index
```
