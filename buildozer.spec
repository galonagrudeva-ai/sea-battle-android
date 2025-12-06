[app]
title = Sea Battle
package.name = seabattle
package.domain = com.game
source.dir = .
source.main = main.py
version = 1.0

# САМЫЕ МИНИМАЛЬНЫЕ ЗАВИСИМОСТИ
requirements = python3,pygame==2.5.2

orientation = portrait  # МЕНЯЕМ НА PORTRAIT для простоты
fullscreen = 0  # ВЫКЛЮЧАЕМ полноэкранный режим

android.api = 30
android.minapi = 21
android.ndk = 23b  # БОЛЕЕ СТАРАЯ ВЕРСИЯ
android.ndk_api = 21
android.arch = arm64-v8a  # ТОЛЬКО ОДНА АРХИТЕКТУРА

android.accept_sdk_license = True

# Отключаем все ненужное
android.allow_backup = False
android.wakelock = False

[buildozer]
log_level = 1  # МЕНЬШЕ ЛОГОВ