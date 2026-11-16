@echo off
chcp 65001 >nul
REM 第一步：登录 4A 系统测试脚本
REM 使用 Playwright CLI 进行浏览器自动化

setlocal

REM 设置路径
set SKILL_ROOT=C:\Users\Administrator\.fxz\skills\nip_inout_list
set PLAYWRIGHT_CLI=C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe

REM 检查 Playwright CLI 是否存在
if not exist "%PLAYWRIGHT_CLI%" (
    echo [错误] 找不到 Playwright CLI
    echo 预期路径: %PLAYWRIGHT_CLI%
    pause
    exit /b 1
)

REM 设置会话名称
set SESSION=nip_test1

echo ========================================
echo 第一步测试：登录 4A 系统
echo ========================================
echo.

echo [步骤 1/5] 关闭可能存在的旧会话...
"%PLAYWRIGHT_CLI%" -s=%SESSION% close 2>nul

echo [步骤 2/5] 打开 4A 系统登录页面...
"%PLAYWRIGHT_CLI%" -s=%SESSION% open "https://4a.fjit.cmcc:30002/" --browser=chrome --headed
if errorlevel 1 (
    echo [错误] 打开页面失败
    pause
    exit /b 1
)

echo [步骤 3/5] 等待页面加载...
timeout /t 5 /nobreak >nul

echo [步骤 4/5] 获取页面快照以识别元素...
"%PLAYWRIGHT_CLI%" -s=%SESSION% snapshot

echo [步骤 5/5] 截图保存当前状态...
"%PLAYWRIGHT_CLI%" -s=%SESSION% screenshot --filename=C:\Users\Administrator\.fxz\skills\nip_inout_list\step1_screenshot.png

echo.
echo ========================================
echo 第一步测试完成！
echo 请查看浏览器窗口和截图确认页面已打开
echo 截图路径: C:\Users\Administrator\.fxz\skills\nip_inout_list\step1_screenshot.png
echo ========================================
pause