## Тестовое задание

# Простой веб-магазин на фреймворке Django с подключенной платежной системой "Stripe" (`stripe.com`)

Текст ТЗ указан в файле: [ТЗ для Python разработчика.docx](%D2%C7%20%E4%EB%FF%20Python%20%F0%E0%E7%F0%E0%E1%EE%F2%F7%E8%EA%E0.docx)

__Доступные адреса (эндпоинты) и функции:__

* "/admin/" - адрес административной панели
* "/buy/<int:id>r/" - адрес перенаправления на платежную систему "Stripe" для единичного товара
* "/item/<int:id>/" - адрес отображения информации о товаре
* "/buy_order/<int:order_id>/" - адрес перенаправления на платежную систему "Stripe" для заказа нескольких товаров
* "/order/<int:order_id>/" - адрес отображения информации о заказе нескольких товаров

## Примеры:

* ### _Административная панель - Основная страница:_
* ![admin.JPG](README%2Fadmin.JPG)
* ### _Административная панель - Вкладка товаров:_
* ![admin_items.JPG](README%2Fadmin_items.JPG)
* ### _Административная панель - Вкладка заказов:_
* ![admin_orders.JPG](README%2Fadmin_orders.JPG)
* ### _Административная панель - Вкладка товаров в заказах:_
* ![admin_order_items.JPG](README%2Fadmin_order_items.JPG)
* ### _Сайт - вкладки информации о товаре и заказе товаров соответственно:_
* ![site_item.JPG](README%2Fsite_item.JPG)
* ![site_order.JPG](README%2Fsite_order.JPG)
* ### _Страница платежной системы "Stripe" - покупка единичного товара:_
* ![stripe_item.JPG](README%2Fstripe_item.JPG)
* ### _Страница платежной системы "Stripe" - покупка нескольких товаров в заказе:_
* ![stripe_order.JPG](README%2Fstripe_order.JPG)

## Запуск сервера:

### Вариант 1
1. Соберите и запустите контейнеры:
`docker-compose up --build`
2. Подключитесь к контейнеру с приложением:
`docker exec -it stripe_app bash`
3. Внутри контейнера выполните команду для применения миграций:
`python manage.py migrate`
4. Создайте суперпользователя (опционально, если вам нужен доступ к админке):
`python manage.py createsuperuser`
5. Создайте тестовые данные (опционально, если вам нужен готовый набор тестовых товаров и заказов):
`python manage.py createtestitems`

### Вариант 2
1.	Скачайте образы из DockerHub:
`docker pull ildarius116/payment_system-web`
2. Создайте файл `docker-compose.yml` и заполните его следующим кодом:
```yaml
version: '3.8'

services:
  web:
    image: ildarius116/payment_system-web:latest
    build: .
    container_name: stripe_app
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    networks:
      - app-network

  db:
    image: postgres:13
    container_name: stripe_db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```
3. Запустите контейнеры:
`docker-compose up`
4. Подключитесь к контейнеру с приложением:
`docker exec -it stripe_app bash`
5. Внутри контейнера выполните команду для применения миграций:
`python manage.py migrate`
6. Создайте суперпользователя (опционально, если вам нужен доступ к админке):
`python manage.py createsuperuser`
7. Создайте тестовые данные (опционально, если вам нужен готовый набор тестовых товаров и заказов):
`python manage.py createtestitems`


### Внимание !!!
Текущий сервер (http://92.255.111.22:8000) запущен (оплачен) до 10.03.2025 (максимум)

_Суперюзер для админки:_
```
login: test_admin
password: admin1234
```