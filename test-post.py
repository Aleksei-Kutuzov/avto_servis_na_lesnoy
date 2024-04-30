import smtplib
from smtp_password import smtp_password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# # Настройки SMTP сервера
# # smtp_server = 'mail.hosting.reg.ru'  # SMTP сервер вашего почтового домена
# smtp_server = 'mail.hosting.reg.ru'  # SMTP сервер вашего почтового домена
# smtp_port = 587  # Порт SMTP сервера
# smtp_username = 'oauth@avtoservisnalesnoj-post.ru'  # Пользователь вашего почтового ящика
# smtp_password =   # Пароль от почтового ящика
#
# # Адрес получателя
# to_email = 'allekskutuzov@gmail.com'
#
# # Создание письма
# msg = MIMEMultipart()
# msg['From'] = smtp_username
# msg['To'] = to_email
# msg['Subject'] = 'Тема вашего письма'
#
# # Текст письма
# body = 'Текст вашего письма'
# msg.attach(MIMEText(body, 'plain'))
#
# # Создание SMTP объекта
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()  # Шифрование для безопасной передачи пароля
#
# # Аутентификация
# server.login(smtp_username, smtp_password)
#
# # Отправка письма
# server.send_message(msg)
#
# # Закрытие соединения
# server.quit()
smtp_server = 'smtp.gmail.com'  # SMTP сервер вашего почтового домена
smtp_port = 587  # Порт SMTP сервера
smtp_username = "allekskutuzov@gmail.com"  # Пользователь вашего почтового ящика
smtp_password = smtp_password  # Пароль от почтового ящика
#
# # Адрес получателя
to_email = 'allekskutuzov@gmail.com'
#
# # Создание письма
msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = to_email
msg['Subject'] = 'Тема вашего письма'
#
# # Текст письма
body = 'Текст вашего письма'
msg.attach(MIMEText(body, 'plain'))
#
# # Создание SMTP объекта
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()  # Шифрование для безопасной передачи пароля
#
# # Аутентификация
server.login(smtp_username, smtp_password)
#
# # Отправка письма
server.send_message(msg)
#
# # Закрытие соединения
server.quit()