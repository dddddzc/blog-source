"""
配置管理模块
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """应用配置"""

    # GitHub 配置
    github_token: str
    github_repository: str
    discussion_category_id: str

    # 阿里云百炼配置
    dashscope_api_key: str

    # 运行模式
    bot_mode: str  # 'dry-run' 或 'production'

    # 博客作者 GitHub 用户名
    blog_author: str = "dddddzc"

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        # 使用 DISCUSSIONS_REPOSITORY 而不是 GITHUB_REPOSITORY
        # 因为 GITHUB_REPOSITORY 会被 GitHub Actions 自动设置为当前仓库
        github_repo = os.getenv("DISCUSSIONS_REPOSITORY", "")
        owner, repo = github_repo.split("/") if "/" in github_repo else ("", "")

        return cls(
            github_token=os.getenv("PERSONAL_ACCESS_TOKEN", ""),
            github_repository=github_repo,
            discussion_category_id=os.getenv("DISCUSSION_CATEGORY_ID", ""),
            dashscope_api_key=os.getenv("DASHSCOPE_API_KEY", ""),
            bot_mode=os.getenv("BOT_MODE", "production"),
            blog_author=owner,  # 仓库所有者即为博客作者
        )

    @property
    def repo_owner(self) -> str:
        """获取仓库所有者"""
        parts = self.github_repository.split("/")
        return parts[0] if len(parts) > 0 else ""

    @property
    def repo_name(self) -> str:
        """获取仓库名称"""
        parts = self.github_repository.split("/")
        return parts[1] if len(parts) > 1 else ""

    @property
    def is_dry_run(self) -> bool:
        """是否为 dry-run 模式"""
        return self.bot_mode == "dry-run"

    def validate(self) -> bool:
        """验证配置是否完整"""
        required_fields = [
            ("PERSONAL_ACCESS_TOKEN", self.github_token),
            ("DISCUSSIONS_REPOSITORY", self.github_repository),
            ("DISCUSSION_CATEGORY_ID", self.discussion_category_id),
            ("DASHSCOPE_API_KEY", self.dashscope_api_key),
        ]

        missing = [name for name, value in required_fields if not value]

        if missing:
            print(f"缺少必要的环境变量: {', '.join(missing)}")
            return False

        return True
