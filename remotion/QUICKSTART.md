# 快速开始指南

## 第一步：创建素材链接

在 `remotion/` 目录下运行：

```bash
cd /Users/zuoc/Documents/clawdcut/remotion

# 创建符号链接（Mac/Linux）
ln -s ../../.clawdcut/assets public/assets

# 或者在 Windows 上（需要管理员权限）
# mklink /D "public\assets" "..\..\.clawdcut\assets"
```

## 第二步：安装依赖

```bash
npm install
```

## 第三步：启动预览

```bash
npm run start
```

浏览器会自动打开 Remotion Studio，你可以实时预览视频！

## 第四步：渲染视频

```bash
npm run build
```

输出文件：`out/video.mp4`

---

## 验证素材链接

运行以下命令检查素材是否正确链接：

```bash
# 检查符号链接是否创建
ls -la public/assets

# 统计素材数量
find public/assets/images -name "*.jpg" | wc -l  # 应该是 18
find public/assets/videos -name "*.mp4" | wc -l   # 应该是 17
```

## 素材路径说明

- **源目录**：`.clawdcut/assets/`
- **链接目录**：`remotion/public/assets/`
- **代码中使用**：`assets/images/xxx.jpg`

所有路径都是相对于 `public/` 目录的，这是 Remotion 的要求。
