[app]
# App name
title = DocuVoice
package.name = docuvoice
package.domain = org.docuvoice

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

# Requirements
requirements = python3,kivy,requests,pyjnius

# Screen orientation
orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET,RECORD_AUDIO,MICROPHONE

# Architecture
android.archs = arm64-v8a

# Android API levels
android.api = 33
android.minapi = 21

# NDK & License
android.ndk = 25.2.9519653
android.accept_sdk_license = True

# Bootstrap
p4a.bootstrap = sdl2

# Features
android.features = android.hardware.microphone

# Gradle dependencies
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Logging
log_level = 2
warn_on_root = 1
