# buildozer.spec
[app]
title = Морской Бой
package.name = seabattle
package.domain = com.game
source.dir = .
source.main = main.py
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 1.0

# Важно: kivy должен быть перед pygame
requirements = python3,kivy==2.1.0,pygame

orientation = landscape
fullscreen = 1
android.api = 30
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.ndk_api = 21
android.arch = armeabi-v7a
android.bootstrap = sdl2
android.allow_resize = 0
android.entrypoint = org.kivy.android.PythonActivity
android.pack_py = 1
log_level = 2
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1