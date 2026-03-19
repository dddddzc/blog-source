"""
GitHub API 封装模块
处理 Discussions 的获取和回复
"""
import requests
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Comment:
    """评论数据结构"""

    id: str
    discussion_id: str
    discussion_number: int
    discussion_title: str
    body: str
    author: str
    created_at: str
    url: str


class GitHubClient:
    """GitHub GraphQL API 客户端"""

    API_URL = "https://api.github.com/graphql"

    def __init__(self, token: str, owner: str, repo: str, category_id: str, blog_author: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.category_id = category_id
        self.blog_author = blog_author
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _query(self, query: str, variables: dict = None) -> dict:
        """执行 GraphQL 查询"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(
            self.API_URL,
            headers=self.headers,
            json=payload,
            timeout=30,
        )

        if response.status_code != 200:
            raise Exception(f"GitHub API 错误: {response.status_code} - {response.text}")

        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL 错误: {data['errors']}")

        return data.get("data", {})

    def get_recent_comments(self, hours: int = 24) -> list[Comment]:
        """
        获取最近指定小时内的评论

        Args:
            hours: 查询最近多少小时内的评论（默认 24 小时）

        Returns:
            评论列表
        """
        since = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"

        # 查询指定分类下的 Discussions
        query = """
        query($owner: String!, $repo: String!, $categoryId: ID!) {
            repository(owner: $owner, name: $repo) {
                discussions(categoryId: $categoryId, first: 50, orderBy: {field: UPDATED_AT, direction: DESC}) {
                    nodes {
                        id
                        number
                        title
                        url
                        comments(first: 100) {
                            nodes {
                                id
                                body
                                createdAt
                                author {
                                    login
                                }
                                replies(first: 10) {
                                    nodes {
                                        author {
                                            login
                                        }
                                        body
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        variables = {
            "owner": self.owner,
            "repo": self.repo,
            "categoryId": self.category_id,
        }

        data = self._query(query, variables)

        comments = []

        for discussion in data.get("repository", {}).get("discussions", {}).get("nodes", []):
            discussion_id = discussion["id"]
            discussion_number = discussion["number"]
            discussion_title = discussion["title"]
            discussion_url = discussion["url"]

            for comment in discussion.get("comments", {}).get("nodes", []):
                created_at = comment.get("createdAt", "")

                # 排除博客作者自己的评论
                author = comment.get("author", {}).get("login", "")
                if author == self.blog_author:
                    continue

                # 检查是否已有 Bot 回复（通过检查回复内容是否包含 AI 助手标识）
                # 因为 Bot 使用用户自己的账号，所以需要通过内容来判断
                has_bot_reply = any(
                    "AI 助手" in reply.get("body", "") or "AI助手" in reply.get("body", "")
                    for reply in comment.get("replies", {}).get("nodes", [])
                )

                if has_bot_reply:
                    print(f"跳过评论 {comment['id'][:20]}... (已有 Bot 回复)")
                    continue

                comments.append(
                    Comment(
                        id=comment["id"],
                        discussion_id=discussion_id,
                        discussion_number=discussion_number,
                        discussion_title=discussion_title,
                        body=comment["body"],
                        author=author,
                        created_at=created_at,
                        url=discussion_url,
                    )
                )

        return comments

    def reply_to_comment(self, discussion_id: str, comment_id: str, body: str) -> bool:
        """
        回复评论

        Args:
            discussion_id: Discussion ID
            comment_id: 要回复的评论 ID
            body: 回复内容

        Returns:
            是否成功
        """
        mutation = """
        mutation($discussionId: ID!, $body: String!, $replyToId: ID) {
            addDiscussionComment(input: {
                discussionId: $discussionId,
                body: $body,
                replyToId: $replyToId
            }) {
                comment {
                    id
                    url
                }
            }
        }
        """

        variables = {
            "discussionId": discussion_id,
            "body": body,
            "replyToId": comment_id,
        }

        try:
            data = self._query(mutation, variables)
            comment = data.get("addDiscussionComment", {}).get("comment", {})
            print(f"回复成功: {comment.get('url', '')}")
            return True
        except Exception as e:
            print(f"回复失败: {e}")
            return False
