@echo off
REM Cloudflare Video - 素材设置脚本 (Windows)

echo 🎬 Cloudflare Video - 素材设置
echo ================================
echo.

REM 检查是否在 remotion 目录下
if not exist package.json (
    echo ❌ 错误：请在 remotion 目录下运行此脚本
    exit /b 1
)

REM 创建 public 目录
echo 📁 创建 public 目录...
if not exist public mkdir public

REM 检查素材源目录
set ASSETS_SOURCE=..\..\.clawdcut\assets
if not exist "%ASSETS_SOURCE%" (
    echo ❌ 错误：找不到素材目录 %ASSETS_SOURCE%
    exit /b 1
)

REM 创建符号链接（需要管理员权限）
echo 🔗 创建素材符号链接...
if exist public\assets (
    echo ⚠️  public\assets 已存在，跳过
    echo    如果需要重新创建，请先删除该目录
) else (
    mklink /D "public\assets" "..\..\.clawdcut\assets"
    if errorlevel 1 (
        echo ❌ 创建符号链接失败
        echo    请以管理员身份运行此脚本
        echo    或者手动复制素材：xcopy /E /I ..\..\.clawdcut\assets public\assets
        exit /b 1
    ) else (
        echo ✅ 符号链接创建成功
    )
)

echo.
echo 📦 安装依赖...
call npm install

echo.
echo ✨ 设置完成！
echo.
echo 🚀 下一步：
echo    npm run start    # 启动预览
echo    npm run build    # 渲染视频
echo.
