#!/bin/bash

# Cloudflare Video - 素材设置脚本

echo "🎬 Cloudflare Video - 素材设置"
echo "================================"
echo ""

# 检查是否在 remotion 目录下
if [ ! -f "package.json" ]; then
    echo "❌ 错误：请在 remotion 目录下运行此脚本"
    exit 1
fi

# 创建 public 目录
echo "📁 创建 public 目录..."
mkdir -p public

# 检查素材源目录
ASSETS_SOURCE="../.clawdcut/assets"
if [ ! -d "$ASSETS_SOURCE" ]; then
    echo "❌ 错误：找不到素材目录 $ASSETS_SOURCE"
    exit 1
fi

# 创建符号链接
echo "🔗 创建素材符号链接..."
if [ -L "public/assets" ]; then
    echo "⚠️  符号链接已存在，跳过"
elif [ -d "public/assets" ]; then
    echo "⚠️  public/assets 是一个目录，是否删除并创建符号链接？(y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf public/assets
        ln -s ../../.clawdcut/assets public/assets
        echo "✅ 符号链接创建成功"
    else
        echo "⏭️  跳过符号链接创建"
    fi
else
    ln -s ../../.clawdcut/assets public/assets
    echo "✅ 符号链接创建成功"
fi

# 验证素材
echo ""
echo "🔍 验证素材..."
IMAGES=$(find public/assets/images -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l)
VIDEOS=$(find public/assets/videos -name "*.mp4" 2>/dev/null | wc -l)

echo "   图片素材：$IMAGES 个"
echo "   视频素材：$VIDEOS 个"

if [ "$IMAGES" -lt 18 ] || [ "$VIDEOS" -lt 17 ]; then
    echo ""
    echo "⚠️  警告：素材数量不足"
    echo "   预期：18 个图片 + 17 个视频"
    echo "   请检查 .clawdcut/assets 目录"
else
    echo "✅ 素材验证通过"
fi

echo ""
echo "📦 安装依赖..."
npm install

echo ""
echo "✨ 设置完成！"
echo ""
echo "🚀 下一步："
echo "   npm run start    # 启动预览"
echo "   npm run build    # 渲染视频"
echo ""
