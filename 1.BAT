@echo off
REM Create the main project folder
mkdir word_to_audio

REM Create the subdirectories (templates and static)
mkdir word_to_audio\templates
mkdir word_to_audio\static

REM Create the app.py file
echo # Python application file > word_to_audio\app.py

REM Create the index.html file inside templates folder
echo <!DOCTYPE html>^<html^>^<head^>^<title^>Word to Audio^</title^>^</head^>^<body^>^<h1^>Welcome to Word to Audio^</h1^>^</body^>^</html^> > word_to_audio\templates\index.html

REM Create the styles.css file inside the static folder
echo /* CSS for Word to Audio project */ > word_to_audio\static\styles.css

echo Folder structure created successfully!
pause
