# WebSocket online chat.

Simple example of online chat using WebSocket.

Простой пример использования WebSocket для онлайн чата и историей сообщений. Сообщения хранятся в PostgreSQL. Новым участникам чата показываются последние 10 сообщений, которые достаются из БД. 

Для хранения сообщений выбирал между MongoDB и PostgreSQL. Выбрал последнее изходя из возможности связи с другими таблицами.

Порядок запуска:

  1. Клонировать проект.
  2. Убрать расширение txt у файла ".env.txt" и изменить параметры для Postgres(POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB).
  3. Запустить команду "docker compose up --build" из корня проекта.

Эндпоит всего один: http://0.0.0.0:8000/chat

Пример работы сервиса:

Первый пользователь:

![ALT TEXT](https://github.com/mrPechen/example_online_chat/blob/main/user_1)

Второй пользователь:

![ALT TEXT](https://github.com/mrPechen/example_online_chat/blob/main/user_2)
