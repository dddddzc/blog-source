"""
AI 回复生成模块
使用阿里云百炼平台的 GLM-5 模型
"""
import dashscope
from dashscope import Generation
from typing import Optional


class AIResponder:
    """AI 回复生成器"""

    def __init__(self, api_key: str, model: str = "glm-5"):
        """
        初始化 AI 回复生成器

        Args:
            api_key: 阿里云百炼 API Key
            model: 模型名称（glm-5）
        """
        self.api_key = api_key
        self.model = model
        dashscope.api_key = api_key

    def generate_response(
        self,
        prompt: str,
        enable_search: bool = True,
        max_tokens: int = 500,
    ) -> str:
        """
        生成回复

        Args:
            prompt: 提示词
            enable_search: 是否启用联网搜索（GLM-5 不支持此参数）
            max_tokens: 最大生成 token 数

        Returns:
            生成的回复文本
        """
        try:
            # GLM-5 需要使用 message 格式
            response = Generation.call(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                result_format="message",
            )

            if response.status_code == 200:
                # message 格式返回的是 choices 列表
                return response.output.choices[0].message.content.strip()
            else:
                raise Exception(f"API 调用失败: {response.code} - {response.message}")

        except Exception as e:
            print(f"AI 生成失败: {e}")
            raise

    def generate_comment_reply(
        self,
        comment: str,
        related_posts: str = "",
        blog_author: str = "dddddzc",
    ) -> str:
        """
        生成评论回复

        Args:
            comment: 评论内容
            related_posts: 相关文章内容
            blog_author: 博客作者名称

        Returns:
            回复文本
        """
        prompt = f"""你是一个技术博客的智能助手，负责回复读者的评论。

## 背景信息
- 博客作者：{blog_author}
- 博客地址：https://dddddzc.github.io

## 相关文章内容
{related_posts if related_posts else "暂无相关文章"}

## 读者评论
{comment}

## 回复要求
1. 语气友好、专业，像朋友一样自然交流
2. 如果问题在文章中有答案，优先引用文章内容
3. 如果需要补充信息，可以提供相关建议
4. 如果不确定答案，诚实说明并建议读者查阅其他资源
5. 回复控制在 150 字以内
6. 使用中文回复

直接输出回复内容，不要有任何开场白或自我介绍。"""

        reply = self.generate_response(prompt, enable_search=True, max_tokens=300)
        # 添加 Bot 签名
        return f"{reply}\n\n---\n*By Bot*"


# 用于测试
if __name__ == "__main__":
    import os

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("请设置 DASHSCOPE_API_KEY 环境变量")
        exit(1)

    responder = AIResponder(api_key)

    # 测试分类
    test_prompt = "请判断这条评论的类型：'博主你好，请问这个怎么安装？'"
    result = responder.generate_response(test_prompt, enable_search=False)
    print(f"分类结果: {result}")

    # 测试回复生成
    reply = responder.generate_comment_reply(
        comment="请问 Hexo 怎么部署到 GitHub Pages？",
        related_posts="## My First Blog\n\n介绍了 Hexo + GitHub 搭建博客的过程...",
    )
    print(f"生成的回复: {reply}")
