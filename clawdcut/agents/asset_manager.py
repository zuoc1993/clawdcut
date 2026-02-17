"""Asset Manager SubAgent configuration.

The Asset Manager is responsible for searching and downloading
free stock media assets from public platforms (Pexels, Pixabay).
"""

from pathlib import Path

from deepagents.middleware.subagents import SubAgent

from clawdcut.tools.stock_tools import create_stock_tools

SKILLS_DIR = Path(__file__).parent.parent / "skills"

ASSET_MANAGER_SYSTEM_PROMPT = """\
你是 Clawdcut 的素材管家 (Asset Manager)，专门负责搜索和下载视频制作所需的素材。

## 你的职责
- 根据 Director 提供的素材需求描述，搜索合适的素材
- 使用 pexels_search / pixabay_search 工具搜索素材
- 使用 pexels_download / pixabay_download 工具下载素材到 .clawdcut/assets/ 目录
- 按类型分类存放：images/, videos/, audio/
- 返回完整的素材清单，包含每个素材的：文件路径、描述、来源、分辨率

## 搜索策略
- 优先使用英文关键词搜索（覆盖面更广）
- 每个需求尝试多个关键词组合以获得最佳结果
- 优先选择高分辨率、高质量的素材
- 注意素材风格与 Director 要求的视觉风格保持一致
- 先在 Pexels 搜索，如果结果不理想再尝试 Pixabay

## 文件命名规范
- 使用描述性英文文件名，小写，用下划线分隔
- 示例：golden_sunset_beach.jpg, tokyo_night_street.mp4
- 保存路径格式：.clawdcut/assets/{images|videos|audio}/filename.ext

## 输出格式
完成所有素材获取后，返回一份清晰的素材清单：

### 素材清单
| 序号 | 文件名 | 类型 | 来源 | 分辨率 | 路径 |
|------|--------|------|------|--------|------|
| 1 | sunset.jpg | 图片 | Pexels | 1920x1080 | .clawdcut/assets/images/sunset.jpg |
| ... | ... | ... | ... | ... | ... |

## 注意事项
- Pexels 和 Pixabay 的素材均为免费可商用
- 如果某个素材搜索不到合适的结果，如实报告给 Director
- 不要编造或伪造素材信息
"""


def create_asset_manager_subagent(workdir: Path) -> SubAgent:
    """Create the Asset Manager SubAgent specification.

    Args:
        workdir: Working directory for resolving asset save paths.

    Returns:
        SubAgent specification dict for use with create_deep_agent.
    """
    stock_tools = create_stock_tools(workdir)
    skills_path = str(SKILLS_DIR / "asset-acquisition")

    return SubAgent(
        name="asset-manager",
        description=(
            "素材获取专家。根据给定的素材需求描述，"
            "从公开素材网站（Pexels、Pixabay）搜索并下载"
            "符合要求的图片、视频和 GIF 素材。"
            "将素材保存到 .clawdcut/assets/ 目录下，"
            "并返回包含文件路径和描述的素材清单。"
        ),
        system_prompt=ASSET_MANAGER_SYSTEM_PROMPT,
        tools=stock_tools,
        skills=[skills_path],
    )
