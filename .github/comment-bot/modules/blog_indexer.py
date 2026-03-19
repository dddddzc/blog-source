"""
博客文章索引模块
解析和检索博客文章内容
"""
import os
import re
from typing import Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BlogPost:
    """博客文章数据结构"""

    title: str
    url: str
    categories: list[str]
    tags: list[str]
    summary: str
    content: str
    date: str


class BlogIndexer:
    """博客文章索引器"""

    def __init__(self, posts_dir: str, base_url: str = "https://dddddzc.github.io"):
        """
        初始化索引器

        Args:
            posts_dir: 博客文章目录路径
            base_url: 博客基础 URL
        """
        self.posts_dir = Path(posts_dir)
        self.base_url = base_url.rstrip("/")
        self.posts: list[BlogPost] = []
        self._indexed = False

    def index(self) -> list[BlogPost]:
        """
        索引所有博客文章

        Returns:
            文章列表
        """
        if self._indexed:
            return self.posts

        self.posts = []

        if not self.posts_dir.exists():
            print(f"文章目录不存在: {self.posts_dir}")
            return self.posts

        for md_file in self.posts_dir.glob("*.md"):
            try:
                post = self._parse_post(md_file)
                if post:
                    self.posts.append(post)
            except Exception as e:
                print(f"解析文章失败 {md_file}: {e}")

        self._indexed = True
        print(f"索引完成，共 {len(self.posts)} 篇文章")

        return self.posts

    def _parse_post(self, file_path: Path) -> Optional[BlogPost]:
        """
        解析单篇文章

        Args:
            file_path: 文章文件路径

        Returns:
            博客文章对象
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 解析 front-matter
        front_matter, body = self._parse_front_matter(content)

        if not front_matter:
            return None

        # 提取标题
        title = front_matter.get("title", file_path.stem)

        # 提取日期
        date = front_matter.get("date", "")

        # 提取分类和标签
        categories = front_matter.get("categories", [])
        if isinstance(categories, str):
            categories = [categories]

        tags = front_matter.get("tags", [])
        if isinstance(tags, str):
            tags = [tags]

        # 生成 URL
        url = self._generate_url(file_path, front_matter)

        # 提取摘要（前 200 字）
        summary = self._extract_summary(body)

        return BlogPost(
            title=title,
            url=url,
            categories=categories,
            tags=tags,
            summary=summary,
            content=body,
            date=str(date),
        )

    def _parse_front_matter(self, content: str) -> tuple[dict, str]:
        """
        解析 front-matter

        Args:
            content: 文章内容

        Returns:
            (front_matter_dict, body_content)
        """
        if not content.startswith("---"):
            return {}, content

        # 查找第二个 ---
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return {}, content

        front_matter_str = content[3:end_idx].strip()
        body = content[end_idx + 3 :].strip()

        # 解析 YAML 格式的 front-matter
        front_matter = {}
        for line in front_matter_str.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # 处理列表
                if value.startswith("[") and value.endswith("]"):
                    value = [
                        item.strip().strip("\"'")
                        for item in value[1:-1].split(",")
                        if item.strip()
                    ]

                front_matter[key] = value

        return front_matter, body

    def _generate_url(self, file_path: Path, front_matter: dict) -> str:
        """
        生成文章 URL

        Args:
            file_path: 文章文件路径
            front_matter: front-matter 字典

        Returns:
            文章 URL
        """
        # Hexo 默认 permalink 格式: :year/:month/:day/:title/
        date_str = str(front_matter.get("date", ""))
        title = front_matter.get("title", file_path.stem)

        # 解析日期
        if date_str:
            # 格式: 2026-03-07 12:00:00 或 2026-03-07
            date_parts = date_str.split(" ")[0].split("-")
            if len(date_parts) >= 3:
                year, month, day = date_parts[0], date_parts[1], date_parts[2]
            else:
                year, month, day = "2024", "01", "01"
        else:
            year, month, day = "2024", "01", "01"

        # 生成 URL safe 的标题
        url_title = re.sub(r"[^\w\u4e00-\u9fff-]", "-", title)
        url_title = re.sub(r"-+", "-", url_title).strip("-")

        return f"{self.base_url}/{year}/{month}/{day}/{url_title}/"

    def _extract_summary(self, body: str, max_length: int = 200) -> str:
        """
        提取文章摘要

        Args:
            body: 文章正文
            max_length: 最大长度

        Returns:
            摘要文本
        """
        # 移除 markdown 标记
        text = re.sub(r"#+ ", "", body)  # 标题
        text = re.sub(r"\*\*|__", "", text)  # 粗体
        text = re.sub(r"\*|_", "", text)  # 斜体
        text = re.sub(r"`[^`]+`", "", text)  # 行内代码
        text = re.sub(r"```[\s\S]*?```", "", text)  # 代码块
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # 图片
        text = re.sub(r"\[([^\]]+)\]\(.*?\)", r"\1", text)  # 链接
        text = re.sub(r"<!--more-->", "", text)  # more 标记
        text = re.sub(r"\n+", " ", text)  # 换行
        text = text.strip()

        if len(text) > max_length:
            text = text[:max_length] + "..."

        return text

    def search(self, query: str, top_k: int = 3) -> list[tuple[BlogPost, float]]:
        """
        搜索相关文章

        Args:
            query: 查询文本
            top_k: 返回前 k 个结果

        Returns:
            [(文章, 相关度分数)] 列表
        """
        if not self._indexed:
            self.index()

        query_lower = query.lower()
        query_words = set(re.findall(r"\w+", query_lower))

        results = []

        for post in self.posts:
            score = 0.0

            # 标题匹配
            if query_lower in post.title.lower():
                score += 10.0

            # 标签匹配
            for tag in post.tags:
                if tag.lower() in query_lower or query_lower in tag.lower():
                    score += 5.0

            # 分类匹配
            for cat in post.categories:
                if cat.lower() in query_lower or query_lower in cat.lower():
                    score += 3.0

            # 内容关键词匹配
            content_lower = post.content.lower()
            for word in query_words:
                if len(word) > 1:  # 忽略单字符
                    score += content_lower.count(word) * 0.5

            if score > 0:
                results.append((post, score))

        # 按分数排序
        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]

    def get_all_content(self) -> str:
        """
        获取所有文章内容（用于构建上下文）

        Returns:
            所有文章内容的合并文本
        """
        if not self._indexed:
            self.index()

        contents = []
        for post in self.posts[:10]:  # 最多取前 10 篇
            contents.append(f"## {post.title}\n\n{post.summary}\n")

        return "\n".join(contents)
