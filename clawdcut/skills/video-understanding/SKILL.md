---
name: video-understanding
description: 多模态视频内容分析 - 提取元数据、场景分割、情绪识别、美学评估
---

# Video Understanding Skill

## 用途

分析和理解视频内容，提取关键信息用于剪辑决策。

## 能力范围

### 1. 元数据提取
- 视频时长、分辨率、帧率、编码格式
- 音频轨道信息（采样率、声道数）
- 文件大小、创建时间

### 2. 场景分割
- 自动检测镜头切换点
- 场景边界识别
- 关键帧提取（每场景代表性帧）

### 3. 内容识别
- **视觉内容**: 人物、物体、场景、动作
- **音频内容**: 语音、音乐、音效、静音段
- **文字内容**: OCR 识别画面中的文字

### 4. 情绪分析
- **面部表情**: 快乐、悲伤、惊讶、愤怒等
- **氛围情绪**: 紧张、放松、温馨、压抑等
- **音乐情绪**: 激昂、舒缓、悬疑、欢快等

### 5. 美学评估
- **构图**: 三分法、对称、引导线
- **色彩**: 色调、饱和度、对比度
- **光影**: 曝光、阴影、高光
- **节奏**: 镜头运动、剪辑节奏

## 使用场景

### 场景 1: 素材初步分析
```
用户上传了 10 个视频文件
↓
扫描并分析所有视频
↓
生成分析报告：
- video_01.mp4: 旅行风景，时长 3:45，情绪：宁静美好
- video_02.mp4: 人物采访，时长 2:10，情绪：真诚温暖
- video_03.mp4: 动作场景，时长 0:45，情绪：紧张刺激
...
```

### 场景 2: 精彩片段提取
```
用户需求: "找出最精彩的 30 秒"
↓
分析所有素材的情绪曲线
↓
识别高潮片段（情绪峰值）
↓
推荐: video_05.mp4 的 1:20-1:50 段
   原因: 情绪高涨、画面精彩、节奏紧凑
```

### 场景 3: 素材匹配
```
用户需求: "找一段温馨的家庭场景"
↓
搜索所有素材的情绪标签
↓
匹配: video_02.mp4 (家庭聚餐，温馨标签)
      video_07.mp4 (亲子互动，温暖标签)
↓
返回匹配结果和推荐理由
```

## 工作流程

### 步骤 1: 元数据提取
```python
metadata = {
    "filename": "video.mp4",
    "duration": 180.5,  # 秒
    "resolution": "1920x1080",
    "fps": 30,
    "video_codec": "h264",
    "audio_codec": "aac",
    "file_size": 234567890,  # bytes
}
```

### 步骤 2: 场景分割
```python
scenes = [
    {"start": 0, "end": 15.3, "key_frame": "frame_0000.jpg"},
    {"start": 15.3, "end": 42.7, "key_frame": "frame_0459.jpg"},
    {"start": 42.7, "end": 180.5, "key_frame": "frame_1281.jpg"},
]
```

### 步骤 3: 关键帧分析
对每个场景的关键帧进行：
- 物体检测（人物、场景类型）
- 情绪识别（面部表情、氛围）
- 美学评估（构图、色彩）

### 步骤 4: 音频分析
- 语音识别（转录文字）
- 音乐检测（类型、情绪）
- 音效识别（环境音、特效音）

### 步骤 5: 综合分析
整合所有信息，生成完整分析报告。

## 输出格式

```json
{
  "file_path": "assets/original/video_travel.mp4",
  "metadata": {
    "duration": 245.6,
    "resolution": "1920x1080",
    "fps": 30,
    "file_size": 567890123
  },
  "scenes": [
    {
      "index": 0,
      "start_time": 0,
      "end_time": 32.5,
      "duration": 32.5,
      "key_frame": ".clawdcut/cache/frames/video_travel_scene_0.jpg",
      "visual_content": {
        "description": "日出海景，沙滩上有几个游客",
        "objects": ["sea", "beach", "sun", "people"],
        "scene_type": "landscape"
      },
      "emotion": {
        "mood": "peaceful",
        "intensity": 0.7,
        "description": "宁静美好"
      },
      "aesthetics": {
        "composition": "rule_of_thirds",
        "color_tone": "warm",
        "lighting": "golden_hour",
        "score": 8.5
      }
    }
  ],
  "audio": {
    "has_voice": false,
    "has_music": true,
    "music_mood": "relaxing",
    "transcription": null
  },
  "overall": {
    "dominant_emotion": "peaceful",
    "suggested_usage": "开场或结尾，营造氛围",
    "quality_score": 8.5
  }
}
```

## 工具调用

### video_analysis
```python
video_analysis(
    file_path="assets/original/video.mp4",
    extract_scenes=True,      # 是否场景分割
    extract_emotion=True,     # 是否情绪分析
    extract_aesthetics=True,  # 是否美学评估
    extract_audio=True        # 是否音频分析
)
```

### batch_video_analysis
```python
batch_video_analysis(
    directory="assets/original/",
    pattern="*.mp4"
)
```

## 最佳实践

1. **缓存结果** - 分析过的视频缓存结果，避免重复分析
2. **增量更新** - 只分析新增或修改的素材
3. **异步处理** - 大文件分析使用异步，不阻塞主流程
4. **质量分级** - 根据美学评分筛选优质素材

## 限制

- 单文件最大 10GB（受内存限制）
- 分析时间约为视频时长的 10-30%
- 情绪识别准确率约 80-90%
- 需要 GPU 加速以获得更好性能（可选）

## 依赖

- moviepy - 视频处理
- opencv-python - 图像分析
- transformers - 情绪识别模型
- librosa - 音频分析
