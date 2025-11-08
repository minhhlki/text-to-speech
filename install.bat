@echo off
chcp 65001 >nul
echo ========================================
echo Cài đặt Vietnamese Text-to-Speech Tool
echo ========================================
echo.

echo Đang cài đặt các thư viện cần thiết...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo LỖI: Python chưa được cài đặt!
    echo Vui lòng tải và cài đặt Python từ: https://www.python.org/downloads/
    echo Nhớ check "Add Python to PATH" khi cài đặt
    pause
    exit /b 1
)

pip install -r requirements.txt

echo.
echo ========================================
echo Cài đặt hoàn tất!
echo ========================================
echo.
echo Bạn có thể chạy chương trình bằng cách double-click file "run.bat"
echo.
pause
