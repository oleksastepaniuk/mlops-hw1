29.01.2023 - v2
# Домашнє завдання:

## Рівень 1:

Розширити пакет rest реалізацією. налаштуванами кластер в докер-компоуз для взаємодії з реальною базою та додати вольюм для перзістансу

## Рівень 2:

Розробити 2 сервіси. Один симулює модель, яка стартує обрахунок (блокує потік від 2х до 5 хв) при отриманні запиту на обробку. Після завершення обробки вона кидає повідомлення про це в меседж брокер. Інший сервіс з АПІ отримує синхронний запит на обробку з клієнта і передає через асинхронну чергу задачу на сервіс модель. Також він має надавати АПІ, по якому клієнт може дізнатися статус джоби (завершилася вона чи ні).

## Рівень 3:

Датчики ІоТ (grpc client) стрімлять вимірювання (погоду) на сервер. Сервер отримує стрім і відправляє ковзке вікно (останні 100 записів) повідомлень на симуляцію моделі для виявлення аномалій. Удачі
