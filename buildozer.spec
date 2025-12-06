[app]

# Название приложения (будет на экране телефона)
title = Морской Бой

# Имя пакета (уникальное, обычно домен наоборот)
package.name = seabattle

# Домен (любой)
package.domain = com.game

# Путь к основному файлу
source.dir = .

# Главный скрипт
source.main = main.py

# Включаемые файлы
source.include_exts = py,png,jpg,kv,atlas,ttf

# Версия приложения
version = 1.0

# Требования (минимальный набор)
requirements = python3,pygame,kivy

# Разрешения Android
android.permissions = 

# Характеристики устройства
android.features = 

# API Android (можно поставить пониже для совместимости)
android.api = 30
android.minapi = 21
android.sdk = 24

# Архитектура
android.arch = armeabi-v7a

# Ориентация экрана
orientation = landscape

# Полноэкранный режим
fullscreen = 1

# Иконка (опционально)
# icon.filename = %(source.dir)s/icon.png

# Заставка (опционально)
# presplash.filename = %(source.dir)s/presplash.png

# Bootstrap (обязательно sdl2 для pygame)
android.bootstrap = sdl2

# Разрешить изменение размера
android.allow_resize = 0

# Тип активности
android.entrypoint = org.kivy.android.PythonActivity

# Паковать все .py файлы
android.pack_py = 1

# Логирование
log_level = 2

# Автоматически принимать лицензии SDK
android.accept_sdk_license = True