@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo  携号转网查询自动化技能 - 完整执行脚本
echo ========================================
echo.

REM 设置环境变量
set PLAYWRIGHT_DAEMON_SESSION_DIR=C:\temp\pw-daemon
set PLAYWRIGHT_SERVER_REGISTRY=C:\temp\pw-server
set PLAYWRIGHT_BROWSERS_PATH=C:\temp\pw-browsers
set PLAYWRIGHT_CLI_ONEFILE_ROOT=C:\temp\pw-runtime

REM 获取当前日期
for /f "tokens=1-3 delims=-/" %%a in ('date /t') do (
    set YEAR=%%a
    set MONTH=%%b
    set DAY=%%c
)
set TODAY=%YEAR%-%MONTH%-%DAY%
set MONTH_FIRST_DAY=%YEAR%/%MONTH%/01

echo 当前日期：%TODAY%
echo 月第一天：%MONTH_FIRST_DAY%
echo.

REM 第一步：打开浏览器并处理证书
echo [步骤 1/7] 打开 4A 登录页面...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test open "https://4a.fjit.cmcc:30002/" --browser=chrome --headed
if errorlevel 1 (
    echo 错误：浏览器打开失败
    exit /b 1
)

echo.
echo [步骤 1/7] 处理 SSL 证书警告...
ping 127.0.0.1 -n 5 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "高级"
ping 127.0.0.1 -n 2 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "继续前往"

echo.
echo [步骤 1/7] 切换到 SIM KEY 登录...
ping 127.0.0.1 -n 3 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "SIM KEY"

echo.
echo [步骤 1/7] 填写手机号并登录...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "手机号" "13850686599"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "登录"

echo.
echo 等待 SIM 认证完成（约 15 秒）...
ping 127.0.0.1 -n 16 >nul

echo.
echo [步骤 2/7] 导航到 IBOP-OA...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "IBOP_OA"
ping 127.0.0.1 -n 5 >nul

echo.
echo [步骤 3/7] 点击"携号转网申请查询"...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "携号转网申请查询"
ping 127.0.0.1 -n 3 >nul

echo.
echo [步骤 3/7] 设置查询条件...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "归属地市" "龙岩"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "归属区县" "永定"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "申请类型" "所有"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "申请状态" "所有"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "起始时间" "%TODAY% 00:00:00"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "截至时间" "%TODAY% 23:59:59"

echo.
echo [步骤 4/7] 执行查询并导出...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "查询"
ping 127.0.0.1 -n 5 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "导出"

echo.
echo 等待导出处理完成...
ping 127.0.0.1 -n 30 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "刷新"
ping 127.0.0.1 -n 10 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "确认"

echo.
echo [步骤 5/7] 下载文件完成...
ping 127.0.0.1 -n 5 >nul

echo.
echo [步骤 6/7] 携号转网号码查询...
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "携号转网号码查询"
ping 127.0.0.1 -n 3 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test fill "起始时间" "%MONTH_FIRST_DAY%"
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "查询"
ping 127.0.0.1 -n 5 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "导出"
ping 127.0.0.1 -n 30 >nul
"C:\Users\Administrator\.fxz\skills\playwright-cli\assets\playwright-cli.exe" -s=nip_test click "确认"

echo.
echo [步骤 7/7] 生成 Excel 比对报告...
python "%~dp0process_compare_excel.py"

echo.
echo ========================================
echo  全部步骤执行完成！
echo ========================================
echo.
echo 生成文件：
echo   - CocExportMnpindex-*.xls (申请查询)
echo   - np 号码信息*.xls (号码查询)
echo   - 当日携转查询清单.xlsx (比对报告 - 桌面)
echo.
pause