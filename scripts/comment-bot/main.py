#!/usr/bin/env python3
"""
博客评论自动回复 Bot 主入口

功能：
1. 获取最近的 GitHub Discussions 评论
2. 判断评论类型，过滤不需要回复的评论
3. 对需要回复的评论，检索相关文章并生成回复
4. 发布回复到 GitHub Discussions
"""
import os
import sys
from pathlib import Path

# 添加模块路径
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from modules.github_client import GitHubClient, Comment
from modules.comment_classifier import CommentClassifier, CommentCategory
from modules.blog_indexer import BlogIndexer
from modules.ai_responder import AIResponder


def main():
    """主函数"""
    print("=" * 50)
    print("博客评论自动回复 Bot")
    print("=" * 50)

    # 加载配置
    config = Config.from_env()

    if not config.validate():
        print("配置验证失败，请检查环境变量")
        sys.exit(1)

    print(f"运行模式: {config.bot_mode}")
    print(f"仓库: {config.github_repository}")
    print(f"博客作者: {config.blog_author}")
    print()

    # 初始化各模块
    github_client = GitHubClient(
        token=config.github_token,
        owner=config.repo_owner,
        repo=config.repo_name,
        category_id=config.discussion_category_id,
        blog_author=config.blog_author,
    )

    ai_responder = AIResponder(
        api_key=config.dashscope_api_key,
        model="glm-4",  # 使用 GLM-4 模型
    )

    classifier = CommentClassifier(ai_responder=ai_responder)

    # 博客文章索引
    posts_dir = Path(__file__).parent.parent.parent / "source" / "_posts"
    blog_indexer = BlogIndexer(
        posts_dir=str(posts_dir),
        base_url=f"https://{config.repo_owner}.github.io",
    )
    blog_indexer.index()

    # 获取最近评论
    print("正在获取最近评论...")
    comments = github_client.get_recent_comments(hours=24)
    print(f"找到 {len(comments)} 条新评论")
    print()

    if not comments:
        print("没有需要处理的评论")
        return

    # 处理每条评论
    stats = {
        "total": len(comments),
        "skipped": 0,
        "replied": 0,
        "failed": 0,
    }

    for comment in comments:
        print("-" * 40)
        print(f"评论 ID: {comment.id}")
        print(f"作者: {comment.author}")
        print(f"内容: {comment.body[:100]}...")
        print(f"文章: {comment.discussion_title}")

        # 分类评论
        result = classifier.classify(comment.body, use_ai=True)
        print(f"分类: {result.category.value} (置信度: {result.confidence:.2f})")
        print(f"原因: {result.reason}")

        if not result.needs_reply:
            print("跳过此评论")
            stats["skipped"] += 1
            continue

        # 检索相关文章
        related_posts = blog_indexer.search(comment.body, top_k=2)
        posts_content = ""
        if related_posts:
            posts_content = "\n\n".join(
                f"### {post.title}\n{post.summary}\n链接: {post.url}"
                for post, score in related_posts
            )
            print(f"找到 {len(related_posts)} 篇相关文章")

        # 生成回复
        print("正在生成回复...")
        try:
            reply = ai_responder.generate_comment_reply(
                comment=comment.body,
                related_posts=posts_content,
                blog_author=config.blog_author,
            )
            print(f"生成的回复: {reply[:100]}...")

            # 发布回复
            if config.is_dry_run:
                print("[DRY-RUN] 跳过发布回复")
            else:
                success = github_client.reply_to_comment(
                    discussion_id=comment.discussion_id,
                    comment_id=comment.id,
                    body=reply,
                )
                if success:
                    stats["replied"] += 1
                else:
                    stats["failed"] += 1

        except Exception as e:
            print(f"处理失败: {e}")
            stats["failed"] += 1

        print()

    # 输出统计
    print("=" * 50)
    print("执行完成")
    print(f"总计: {stats['total']} 条")
    print(f"跳过: {stats['skipped']} 条")
    print(f"已回复: {stats['replied']} 条")
    print(f"失败: {stats['failed']} 条")
    print("=" * 50)


if __name__ == "__main__":
    main()
