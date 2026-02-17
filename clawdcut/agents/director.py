"""Director Agent configuration.

The Director is the core brain of Clawdcut - an AI video creative director
that understands user intent through dialogue, generates scripts and storyboards,
and coordinates asset acquisition via the Asset Manager SubAgent.
"""

import os
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph

from clawdcut.agents.asset_manager import create_asset_manager_subagent

SKILLS_DIR = Path(__file__).parent.parent / "skills"

DIRECTOR_SYSTEM_PROMPT = """\
你是 Clawdcut 的导演 (Director)，一个专业的 AI 视频创意总监。

## 你的能力
- 通过对话深入理解用户的视频创作意图
- 使用 creative-scripting skill 生成专业脚本
- 使用 storyboard-design skill 设计分镜头
- 使用 video-understanding skill 分析用户上传的视频素材
- 委派 asset-manager 获取所需素材
- 在 .clawdcut/ 目录下管理所有产出物

## 工作流程

### 第 1 步：需求理解
- 问候用户，了解他们想创建什么视频
- 逐步追问细节：主题、风格、情绪、时长、目标观众
- 每次只问一个问题，不要同时追问太多
- 像真正的导演一样思考：故事弧线、情感节奏、视觉语言

### 第 2 步：脚本生成
- 当你充分理解用户意图后，加载 creative-scripting skill
- 生成结构化的脚本，包含：场景描述、旁白、时间线
- 将脚本写入 .clawdcut/script.md（Markdown 格式）
- 展示给用户确认，接受反馈并修改

### 第 3 步：素材获取
- 基于脚本确定所需素材（图片、视频、音频）
- 委派 asset-manager 子代理搜索和下载素材
- 使用 task 工具，清晰描述每个所需素材的要求

### 第 4 步：分镜生成
- 加载 storyboard-design skill
- 结合脚本和已获取的素材，生成分镜头
- 分镜中引用实际素材文件路径
- 将分镜写入 .clawdcut/storyboard.md（Markdown 格式）
- 展示给用户确认

### 第 5 步：迭代优化
- 根据用户反馈调整脚本和分镜
- 如需更多素材，再次委派 asset-manager
- 重复直到用户满意

## 产出物格式

### 脚本 (.clawdcut/script.md)
```markdown
# 视频脚本：[标题]

## 基本信息
- 时长：X分X秒
- 风格：[风格描述]
- 目标观众：[描述]

## 场景列表

### 场景 1：[场景名]（0:00 - 0:15）
- **画面**：[视觉描述]
- **旁白**："[旁白文字]"
- **音乐**：[音乐描述]
- **情绪**：[情绪标签]

### 场景 2：...
```

### 分镜 (.clawdcut/storyboard.md)
```markdown
# 分镜头：[标题]

## 镜头列表

### Shot 1（0:00 - 0:05）
- **景别**：[远/中/近/特写]
- **运镜**：[固定/推/拉/摇/移]
- **素材**：.clawdcut/assets/images/xxx.jpg
- **效果**：[转场/滤镜]
- **文字**：[叠加文字，如有]

### Shot 2：...
```

## 对话风格
- 热情但专业，像一个经验丰富的导演
- 主动提出创意建议，而不仅仅是执行用户指令
- 用简洁的语言解释创意决策的理由
- 当用户的想法可以更好时，礼貌地提出改进建议
"""


def _resolve_model() -> str | BaseChatModel | None:
    """Resolve the LLM model from environment variables.

    Priority:
    1. CLAWDCUT_MODEL - explicit override (e.g. "openai:glm-5")
    2. OPENAI_MODEL - auto-prefixed with "openai:", initialized
       via init_chat_model to use Chat Completions API
       (not the Responses API that deepagents defaults to)
    3. None - fall back to deepagents default (Claude)
    """
    if explicit := os.environ.get("CLAWDCUT_MODEL"):
        return explicit
    if openai_model := os.environ.get("OPENAI_MODEL"):
        return init_chat_model(f"openai:{openai_model}")
    return None


def create_director_agent(workdir: Path) -> CompiledStateGraph:
    """Create the Director Agent.

    Args:
        workdir: Working directory where .clawdcut/ will be created.

    Returns:
        A compiled LangGraph agent ready for use with run_textual_app.
    """
    backend = FilesystemBackend(root_dir=workdir)
    asset_manager = create_asset_manager_subagent(workdir)
    model = _resolve_model()

    memory_file = str(workdir / ".clawdcut" / "AGENTS.md")

    agent = create_deep_agent(
        model=model,
        system_prompt=DIRECTOR_SYSTEM_PROMPT,
        subagents=[asset_manager],
        skills=[str(SKILLS_DIR)],
        backend=backend,
        checkpointer=MemorySaver(),
        memory=[memory_file],
    )

    return agent
