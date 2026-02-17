#!/bin/bash

# 验证素材链接脚本

echo "🔍 验证 Remotion 素材链接"
echo "=========================="
echo ""

# 检查符号链接
if [ -L "public/assets" ]; then
    echo "✅ 符号链接已创建"
    echo "   链接目标: $(readlink public/assets)"
elif [ -d "public/assets" ]; then
    echo "⚠️  public/assets 是目录（不是符号链接）"
else
    echo "❌ 符号链接未创建"
    echo ""
    echo "请运行以下命令创建："
    echo "  ln -s ../../.clawdcut/assets public/assets"
    exit 1
fi

echo ""
echo "📊 素材统计："

# 统计图片
IMAGE_COUNT=$(find public/assets/images -name "*.jpg" -o -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
echo "   图片素材: $IMAGE_COUNT 个"

# 统计视频
VIDEO_COUNT=$(find public/assets/videos -name "*.mp4" 2>/dev/null | wc -l | tr -d ' ')
echo "   视频素材: $VIDEO_COUNT 个"

# 统计音频
AUDIO_COUNT=$(find public/assets/audio -type f 2>/dev/null | wc -l | tr -d ' ')
echo "   音频素材: $AUDIO_COUNT 个"

echo ""

# 验证数量
if [ "$IMAGE_COUNT" -ge 18 ] && [ "$VIDEO_COUNT" -ge 17 ]; then
    echo "✅ 素材验证通过！"
    echo ""
    echo "🚀 可以开始预览了："
    echo "   npm run start"
else
    echo "⚠️  素材数量不足"
    echo "   预期: 18+ 图片, 17+ 视频"
    echo "   请检查 .clawdcut/assets 目录"
fi

echo ""
