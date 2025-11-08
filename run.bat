@echo off
chcp 65001 >nul

REM Kiểm tra Python đã cài đặt chưa
python --version >nul 2>&1
if errorlevel 1 (
    echo LỖI: Python chưa được cài đặt!
    echo Vui lòng tải và cài đặt Python từ: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Chạy ứng dụng
python tts_gui.py

REM Nếu có lỗi, hiển thị thông báo
if errorlevel 1 (
    echo.
    echo Đã xảy ra lỗi khi chạy chương trình!
    echo Vui lòng chạy file "install.bat" trước để cài đặt các thư viện cần thiết.
    pause
)
