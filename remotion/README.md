# Cloudflare - 守护互联网的无形力量

这是一个使用 Remotion 创建的品牌宣传视频项目。

## 项目信息

- **时长**：2分40秒（160秒）
- **分辨率**：1920x1080 (Full HD)
- **帧率**：30 fps
- **镜头数**：25个镜头
- **场景数**：5个场景

## 视频结构

### 场景 1：脆弱的网络世界（0:00 - 0:25）
- 紧张、危机感
- 展现互联网的脆弱性
- 镜头：1-5

### 场景 2：改变，从质疑开始（0:25 - 0:55）
- 振奋、希望萌芽
- Cloudflare 的诞生
- 镜头：6-11

### 场景 3：无形的守护者（0:55 - 1:45）
- 力量感、使命感
- 展现全球网络和影响力
- 镜头：12-19

### 场景 4：更公平的互联网（1:45 - 2:15）
- 坚定、温暖中的力量
- 公平与平等的理念
- 镜头：20-22

### 场景 5：未来已来（2:15 - 2:40）
- 振奋、无限可能
- 未来科技愿景
- 镜头：23-25

## 前置要求

1. **安装 Node.js**（推荐 v18 或更高版本）
2. **准备素材**：创建素材符号链接

## ⚠️ 重要：素材路径说明

**Remotion 的 `staticFile()` 只接受相对于 `public/` 目录的路径。**

### 正确的路径格式

代码中使用的路径格式：

```typescript
// ✅ 正确
image: 'assets/images/global_network_earth.jpg'
overlayVideo: 'assets/videos/earth_globe_rotating_space_4k.mp4'

// ❌ 错误 - 不支持相对路径
image: '../.clawdcut/assets/images/global_network_earth.jpg'
```

所有路径都已更新为正确格式，你只需要创建符号链接即可。

## 素材准备

素材位于项目根目录的 `.clawdcut/assets/` 目录下。需要创建符号链接到 Remotion 的 `public` 目录：

```bash
# 在 remotion 目录下执行
mkdir -p public/assets
cp -r ../.clawdcut/assets/images public/assets/
cp -r ../.clawdcut/assets/videos public/assets/
cp -r ../.clawdcut/assets/audio public/assets/  # 如果有音频文件
```

或者创建符号链接（推荐）：

```bash
# macOS/Linux
ln -s ../../.clawdcut/assets public/assets

# Windows（以管理员身份运行）
mklink /D "public\assets" "..\..\.clawdcut\assets"
```

## 安装依赖

```bash
npm install
# 或
bun install
```

## 开发

启动 Remotion Studio 进行预览和调试：

```bash
npm run start
```

这将在浏览器中打开 Remotion Studio，你可以：
- 实时预览视频
- 调整时间线
- 查看每个镜头
- 调试动画效果

## 渲染视频

渲染最终视频：

```bash
npm run build
```

视频将输出到 `out/video.mp4`。

### 自定义渲染选项

```bash
# 渲染为其他格式
npx remotion render CloudflareVideo out/video.webm --codec vp9

# 渲染为 GIF
npx remotion render CloudflareVideo out/video.gif

# 渲染特定帧范围
npx remotion render CloudflareVideo out/video.mp4 --frames 0-300
```

## 项目结构

```
remotion/
├── src/
│   ├── components/
│   │   ├── ShotComponent.tsx       # 基础镜头组件
│   │   ├── Shot16Multi.tsx         # 三画面切换组件
│   │   ├── Shot20SplitScreen.tsx   # 分屏对比组件
│   │   ├── Shot24Multi.tsx         # 未来科技三画面
│   │   ├── Scene1.tsx              # 场景1
│   │   ├── Scene2.tsx              # 场景2
│   │   ├── Scene3.tsx              # 场景3
│   │   ├── Scene4.tsx              # 场景4
│   │   └── Scene5.tsx              # 场景5
│   ├── config/
│   │   └── shots.ts                # 镜头数据配置
│   ├── CloudflareVideo.tsx         # 主视频组件
│   ├── Root.tsx                    # Remotion Root
│   └── index.ts                    # 入口文件
├── public/
│   └── assets/                     # 素材文件（符号链接）
├── package.json
├── tsconfig.json
└── README.md
```

## 特效和动画

本项目包含以下视觉效果：

- **Ken Burns 效果**：缓慢推拉镜头，增加画面动感
- **视频叠加**：使用混合模式叠加科技感视频
- **故障效果**：紧张场景的抖动和噪点
- **色调调整**：从冷色到暖色的情绪转变
- **多画面切换**：快速剪辑增强节奏感
- **分屏对比**：直观展示对比效果

## 自定义修改

### 修改镜头时长

编辑 `src/config/shots.ts` 文件中的 `duration` 字段：

```typescript
{
  id: 1,
  startTime: 0,
  duration: 5, // 秒
  // ...
}
```

### 修改文字和旁白

在 `src/config/shots.ts` 中修改 `text` 和 `narration` 字段：

```typescript
{
  id: 1,
  text: 'ERROR 503',
  narration: '互联网。',
  // ...
}
```

### 替换素材

将新素材放入 `public/assets/` 目录，然后更新 `shots.ts` 中的路径：

```typescript
{
  image: 'assets/images/your-image.jpg',
  overlayVideo: 'assets/videos/your-video.mp4',
  // ...
}
```

## 添加音频

在 `CloudflareVideo.tsx` 中添加音频轨道：

```tsx
import { Audio } from '@remotion/media';

export const CloudflareVideo: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* 场景 */}
      <Scene1 />
      {/* ... */}
      
      {/* 音频 */}
      <Audio
        src={staticFile('assets/audio/background-music.mp3')}
        volume={0.8}
      />
    </AbsoluteFill>
  );
};
```

## 性能优化建议

1. **使用 premountFor**：所有 Sequence 都已配置 premountFor，确保提前加载
2. **图片优化**：建议使用 1920x1080 或相近尺寸的图片
3. **视频格式**：推荐使用 MP4 (H.264) 格式
4. **渲染质量**：可以降低预览质量以提高开发效率

## 常见问题

### 素材路径错误

确保 `public/assets` 符号链接正确创建：

```bash
ls -la public/assets
```

### 渲染速度慢

- 使用 `--concurrency` 参数提高并行度
- 确保有足够的内存
- 使用 SSD 存储

### 视频质量不佳

修改 `remotion.config.ts`：

```typescript
Config.setVideoImageFormat("png"); // 更高质量
Config.setVideoBitrate("10M"); // 提高比特率
```

## 许可

本项目仅用于学习和演示目的。

---

Created with ❤️ using Remotion
