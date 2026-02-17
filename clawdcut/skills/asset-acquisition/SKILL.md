---
name: asset-acquisition
description: 素材获取与管理 - AI生成、素材库搜索、本地素材分析、版本控制
---

# Asset Acquisition Skill

## 用途

获取和管理视频制作所需的各种素材，包括分析本地素材、AI生成缺失素材、搜索外部素材库。

## 能力范围

### 1. 本地素材分析
- **视频分析**: 元数据提取、场景分割、内容识别
- **图像分析**: 分辨率、色彩、内容描述
- **音频分析**: 波形、频谱、内容类型

### 2. AI 素材生成
- **图像生成**: 使用 DALL-E、Midjourney 等生成图片
- **音效生成**: 生成特定音效（环境音、特效音）
- **配音合成**: 使用 ElevenLabs 等合成旁白
- **音乐生成**: 生成背景音乐（可选）

### 3. 素材库搜索
- **免费素材库**: Pexels、Pixabay、Unsplash
- **付费素材库**: Artlist、Epidemic Sound、Shutterstock
- **搜索策略**: 关键词优化、筛选条件、结果排序

### 4. 素材管理
- **分类存储**: 按类型和来源分类
- **元数据管理**: 记录素材信息和使用许可
- **版本控制**: 追踪素材变更
- **去重优化**: 避免重复下载

## 使用场景

### 场景 1: 完整素材准备流程
```
Director 需求: "需要以下素材：
  - 开场：日出海景
  - 中段：樱花飘落特写
  - 配乐：轻快治愈系音乐
  - 音效：海浪声、鸟鸣声"

Asset Manager 执行:
1. 检查本地素材库
   - 发现: sunrise.mp4 (可用)
   - 缺失: 樱花特写、配乐、音效

2. 生成/搜索缺失素材
   - AI生成: cherry_blossom.jpg (樱花特写)
   - 搜索 Pexels: upbeat_acoustic.mp3 (配乐)
   - AI生成: ocean_waves.wav (海浪声)
   - 搜索 Freesound: birds_chirping.wav (鸟鸣)

3. 验证素材质量
   - 检查分辨率、时长、格式
   - 确认版权许可

4. 返回素材包
   所有素材就绪，可供渲染使用
```

### 场景 2: AI 图像生成
```
需求: "生成一张日本神社的插画风格图片，樱花季，温暖色调"

生成参数:
- 平台: DALL-E 3
- Prompt: "A traditional Japanese shrine in spring, 
          cherry blossoms falling, warm golden hour lighting, 
          illustration style, Studio Ghibli inspired, 
          peaceful atmosphere, high detail"
- 尺寸: 1920x1080
- 风格: 插画

输出:
- 图片文件: generated/shrine_spring_001.png
- 元数据: 生成参数、使用许可
```

### 场景 3: 素材库搜索
```
需求: "搜索一段 30 秒的轻快背景音乐，适合旅行视频"

搜索策略:
1. Pexels (免费)
   - 关键词: "upbeat acoustic travel happy"
   - 筛选: 时长 20-40 秒，音乐类型
   - 结果: 5 个候选

2. Pixabay (免费)
   - 关键词: "cheerful guitar summer"
   - 筛选: 时长 20-40 秒
   - 结果: 3 个候选

3. 评估排序
   - 按匹配度、质量、许可排序
   - 推荐: pexels_upbeat_001.mp3

4. 下载验证
   - 下载并检查音质
   - 确认 CC0 许可
```

## 工作流程

### 步骤 1: 需求解析
- 理解需要的素材类型和规格
- 确定优先级（必需 vs 可选）
- 制定获取策略

### 步骤 2: 本地检查
- 扫描本地素材库
- 检查已有素材是否可用
- 标记缺失素材

### 步骤 3: 素材获取
根据素材类型选择获取方式：
- **本地已有** → 直接使用
- **AI 可生成** → 调用生成 API
- **素材库有** → 搜索并下载
- **需购买** → 标记并提示用户

### 步骤 4: 质量验证
- 检查文件完整性
- 验证格式兼容性
- 确认分辨率和时长

### 步骤 5: 版权确认
- 记录素材来源
- 确认使用许可
- 标注是否需要署名

### 步骤 6: 组织存储
- 按类型分类存储
- 生成素材清单
- 更新元数据

## 输出格式

```json
{
  "project_id": "uuid",
  "status": "ready",
  "assets": {
    "videos": [
      {
        "id": "vid_001",
        "filename": "sunrise.mp4",
        "path": "assets/original/sunrise.mp4",
        "source": "original",
        "duration": 15.5,
        "resolution": "1920x1080",
        "license": "user_owned",
        "status": "ready"
      }
    ],
    "images": [
      {
        "id": "img_001",
        "filename": "shrine_spring_001.png",
        "path": "assets/generated/shrine_spring_001.png",
        "source": "generated",
        "platform": "dall-e-3",
        "prompt": "A traditional Japanese shrine...",
        "resolution": "1920x1080",
        "license": "ai_generated",
        "status": "ready"
      }
    ],
    "audio": [
      {
        "id": "aud_001",
        "filename": "upbeat_acoustic.mp3",
        "path": "assets/searched/upbeat_acoustic.mp3",
        "source": "searched",
        "platform": "pexels",
        "duration": 32.0,
        "license": "pexels_license",
        "attribution_required": false,
        "status": "ready"
      },
      {
        "id": "sfx_001",
        "filename": "ocean_waves.wav",
        "path": "assets/generated/ocean_waves.wav",
        "source": "generated",
        "platform": "elevenlabs",
        "description": "Ocean waves crashing",
        "duration": 10.0,
        "license": "ai_generated",
        "status": "ready"
      }
    ],
    "missing": [
      {
        "type": "music",
        "description": "Epic orchestral track",
        "reason": "premium_content",
        "suggestion": "Consider purchasing from Artlist"
      }
    ]
  },
  "summary": {
    "total": 10,
    "ready": 9,
    "missing": 1,
    "generated": 3,
    "searched": 4,
    "original": 2
  }
}
```

## 素材来源配置

### AI 生成平台
```yaml
# ~/.clawdcut/config.yaml
ai_generation:
  image:
    provider: "dall-e"  # 或 "midjourney", "stable-diffusion"
    api_key: "${OPENAI_API_KEY}"
    default_size: "1920x1080"
    
  audio:
    provider: "elevenlabs"
    api_key: "${ELEVENLABS_API_KEY}"
    voice: "default"
```

### 素材库 API
```yaml
asset_libraries:
  pexels:
    api_key: "${PEXELS_API_KEY}"
    enabled: true
    
  pixabay:
    api_key: "${PIXABAY_API_KEY}"
    enabled: true
    
  artlist:
    api_key: "${ARTLIST_API_KEY}"
    enabled: false  # 付费，按需启用
```

## 工具调用

### analyze_local_assets
```python
analyze_local_assets(
    directory="assets/original/",
    recursive=True
)
```

### generate_image
```python
generate_image(
    prompt="A traditional Japanese shrine in spring...",
    size="1920x1080",
    style="illustration",
    output_path="assets/generated/"
)
```

### generate_audio
```python
generate_audio(
    text="欢迎来到美丽的京都",
    voice="zh-CN-XiaoxiaoNeural",
    output_path="assets/generated/narration.wav"
)
```

### search_asset_library
```python
search_asset_library(
    query="upbeat acoustic travel",
    type="music",
    duration_range=(20, 40),
    license="free",
    platforms=["pexels", "pixabay"]
)
```

### download_asset
```python
download_asset(
    url="https://pexels.com/...",
    output_path="assets/searched/",
    verify_license=True
)
```

## 版权管理

### 许可类型

| 来源 | 许可类型 | 商用 | 署名 | 说明 |
|------|---------|------|------|------|
| **用户上传** | 用户自有 | ✅ | ❌ | 用户拥有版权 |
| **AI生成** | 平台政策 | ✅/⚠️ | ❌ | 视平台而定 |
| **Pexels** | Pexels License | ✅ | ❌ | 免费商用 |
| **Pixabay** | Pixabay License | ✅ | ❌ | 免费商用 |
| **Unsplash** | Unsplash License | ✅ | ❌ | 免费商用 |
| **Artlist** | 订阅许可 | ✅ | ❌ | 需订阅 |

### 版权检查清单
- [ ] 确认素材来源
- [ ] 检查使用许可
- [ ] 确认是否需要署名
- [ ] 记录许可信息
- [ ] 检查是否有使用限制（如次数、地域）

## 最佳实践

1. **优先使用本地素材** - 避免不必要的下载
2. **AI 生成次之** - 快速获得定制化素材
3. **素材库搜索最后** - 补充缺失的素材
4. **记录所有来源** - 便于后续版权核查
5. **验证素材质量** - 下载后检查是否可用
6. **分类存储** - 按来源和类型组织

## 常见错误

- ❌ 不检查版权就使用素材
- ❌ 忽略素材格式兼容性
- ❌ 重复下载相同素材
- ❌ 不记录素材来源
- ❌ 使用低质量素材

## 依赖

- moviepy - 视频分析
- pillow - 图像处理
- requests - API 调用
- openai - DALL-E 图像生成
- elevenlabs - 语音合成
