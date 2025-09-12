@echo off
title HRMS - Keep Localhost Alive
color 0A

echo.
echo ======================================================================
echo 🌐 HRMS LOCALHOST KEEPER - DUY TRI SERVER
echo ======================================================================
echo 💡 Script này sẽ tự động duy trì localhost:8501
echo 🔄 Tự động restart nếu server bị dừng
echo ⚠️  Nhấn Ctrl+C để dừng hoàn toàn
echo ======================================================================
echo.

:start
echo [%date% %time%] 🚀 Đang kiểm tra HRMS server...

REM Kiểm tra port 8501 có đang hoạt động không
netstat -ano | findstr :8501 >nul
if %errorlevel%==0 (
    echo [%date% %time%] ✅ Server đang hoạt động tốt trên localhost:8501
) else (
    echo [%date% %time%] ❌ Server không phản hồi, đang khởi động lại...
    echo [%date% %time%] 🔄 Restarting HRMS Modern...
    
    REM Kill any remaining processes
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq HRMS*" >nul 2>&1
    
    REM Restart server
    start /MIN "HRMS Server" python run.py
    
    echo [%date% %time%] ⏳ Chờ 10 giây để server khởi động...
    timeout /t 10 >nul
)

echo [%date% %time%] 💤 Chờ 30 giây trước khi kiểm tra lại...
timeout /t 30 >nul
goto start
