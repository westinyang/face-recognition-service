title=build face-recognition-service
@echo off
pyinstaller -F main.spec
copy config.ini dist
pause
exit