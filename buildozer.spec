[app]
title = Морской Бой
package.name = seabattle
package.domain = com.game
source.dir = .
source.main = main.py
version = 1.0

# ВАЖНО: Правильные зависимости для PyGame на Android
requirements = python3, kivy==2.1.0, pyjnius, android, sdl2_ttf==2.0.15, sdl2_image==2.0.5, sdl2_mixer==2.0.4, pygame

orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 23b
android.archs = arm64-v8a

android.accept_sdk_license = True

# Отключаем ненужные функции для упрощения
android.allow_backup = False
android.wakelock = False

[buildozer]
log_level = 2
warn_on_root = 1