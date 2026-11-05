[app]

# (str) Title of your application
title = DLS Auto Bot

# (str) Package name
package.name = dlsbot

# (str) Package domain (needed for android packaging)
package.domain = org.flex

# (list) Source files to include (let it include py files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Source directory where the application files are located
source.dir = .

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3,kivy,requests

# (str) Explicitly set Python version to avoid python 3.14 errors
p4a.python_version = 3.10

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (bool) Use the Android SDK license agreement
android.accept_sdk_license = True

# (str) Supported orientations
orientation = portrait

# (bool) Indicate whether the application should be fullscreen or not
fullscreen = 0
