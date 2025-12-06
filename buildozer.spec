[app]
title = Sea Battle
package.name = seabattle
package.domain = com.game
source.dir = .
source.main = main.py
version = 1.0

requirements = python3,kivy,pygame

orientation = landscape
fullscreen = 1

android.api = 30
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.ndk_api = 21
android.arch = arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2