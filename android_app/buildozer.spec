[app]
title = DocuVoice
package.name = docuvoice
package.domain = org.docuvoice

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

requirements = python3,kivy,requests,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MICROPHONE

# Architecture
android.archs = arm64-v8a

# Api level
android.api = 31
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 31.0.0


# Bootstrap
p4a.bootstrap = sdl2

# App icon
#android.icon = data/icon.png
#android.presplash = data/presplash.png

# Features
android.features = android.hardware.microphone

# Gradle dependencies
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Java classes
#android.add_src = 

log_level = 2
warn_on_root = 1
