"""
评论分类器模块
判断评论是否需要回复
"""
import re
from enum import Enum
from typing import Optional
from dataclasses import dataclass


class CommentCategory(Enum):
    """评论类别"""

    QUESTION = "question"  # 技术问题/求助 - 需要回复
    SUGGESTION = "suggestion"  # 建议/反馈 - 需要回复
    DISCUSSION = "discussion"  # 深度讨论 - 需要回复
    PRAISE = "praise"  # 赞美/感谢 - 跳过
    GREETING = "greeting"  # 打招呼/寒暄 - 跳过
    EMOJI_ONLY = "emoji_only"  # 纯表情 - 跳过
    SPAM = "spam"  # 垃圾信息 - 跳过


@dataclass
class ClassificationResult:
    """分类结果"""

    category: CommentCategory
    confidence: float
    reason: str

    @property
    def needs_reply(self) -> bool:
        """是否需要回复"""
        return self.category in [
            CommentCategory.QUESTION,
            CommentCategory.SUGGESTION,
            CommentCategory.DISCUSSION,
        ]


class CommentClassifier:
    """评论分类器"""

    # 需要回复的关键词
    QUESTION_KEYWORDS = [
        "怎么",
        "如何",
        "为什么",
        "请问",
        "求助",
        "帮忙",
        "问题",
        "错误",
        "报错",
        "失败",
        "不行",
        "无法",
        "能不能",
        "可以吗",
        "有没",
        "是不是",
        "为什么",
        "原因",
        "解决",
        "怎么办",
        "请教",
        "?",
        "？",
        "how",
        "why",
        "what",
        "help",
        "issue",
        "error",
        "problem",
    ]

    # 赞美/感谢关键词
    PRAISE_KEYWORDS = [
        "谢谢",
        "感谢",
        "太棒",
        "厉害",
        "牛逼",
        "优秀",
        "赞",
        "好文",
        "收藏",
        "学习了",
        "受教",
        "不错",
        "写得",
        "真好",
        "感谢分享",
        "thanks",
        "thank",
        "good",
        "great",
        "nice",
        "awesome",
    ]

    # 打招呼关键词
    GREETING_KEYWORDS = [
        "你好",
        "您好",
        "哈喽",
        "hello",
        "hi",
        "嗨",
        "早上好",
        "晚上好",
        "下午好",
    ]

    # 表情模式
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )

    def __init__(self, ai_responder=None):
        """
        初始化分类器

        Args:
            ai_responder: AI 回复生成器（用于 AI 分类）
        """
        self.ai_responder = ai_responder

    def classify(self, comment_body: str, use_ai: bool = True) -> ClassificationResult:
        """
        分类评论

        Args:
            comment_body: 评论内容
            use_ai: 是否使用 AI 辅助分类

        Returns:
            分类结果
        """
        # 阶段一：规则快速过滤
        rule_result = self._rule_based_classify(comment_body)
        if rule_result.confidence >= 0.9:
            return rule_result

        # 阶段二：AI 智能分类
        if use_ai and self.ai_responder:
            return self._ai_classify(comment_body)

        return rule_result

    def _rule_based_classify(self, body: str) -> ClassificationResult:
        """基于规则的分类"""
        body_lower = body.lower().strip()

        # 检查是否为纯表情
        text_without_emoji = self.EMOJI_PATTERN.sub("", body)
        if len(text_without_emoji.strip()) < 3:
            return ClassificationResult(
                category=CommentCategory.EMOJI_ONLY,
                confidence=0.95,
                reason="评论主要是表情符号",
            )

        # 检查是否过短
        if len(body.strip()) < 5:
            return ClassificationResult(
                category=CommentCategory.GREETING,
                confidence=0.8,
                reason="评论过短",
            )

        # 检查打招呼
        for keyword in self.GREETING_KEYWORDS:
            if keyword in body_lower and len(body.strip()) < 20:
                return ClassificationResult(
                    category=CommentCategory.GREETING,
                    confidence=0.85,
                    reason="看起来是打招呼",
                )

        # 检查赞美/感谢
        praise_count = sum(1 for kw in self.PRAISE_KEYWORDS if kw in body_lower)
        if praise_count >= 2 or (praise_count >= 1 and len(body.strip()) < 30):
            return ClassificationResult(
                category=CommentCategory.PRAISE,
                confidence=0.85,
                reason="看起来是赞美或感谢",
            )

        # 检查问题关键词
        question_count = sum(1 for kw in self.QUESTION_KEYWORDS if kw in body_lower)
        if question_count >= 1:
            return ClassificationResult(
                category=CommentCategory.QUESTION,
                confidence=0.7,
                reason="包含问题关键词",
            )

        # 默认：需要进一步 AI 分类
        return ClassificationResult(
            category=CommentCategory.DISCUSSION,
            confidence=0.5,
            reason="规则无法确定，需要 AI 分类",
        )

    def _ai_classify(self, body: str) -> ClassificationResult:
        """使用 AI 进行分类"""
        prompt = f"""你是一个评论分类助手。请判断以下评论的类型。

评论内容：{body}

分类选项：
- question: 提出问题或求助
- suggestion: 提供建议或反馈
- discussion: 有价值的讨论内容
- praise: 纯粹的赞美或感谢
- greeting: 简单打招呼
- emoji_only: 纯表情或符号
- spam: 垃圾/广告信息

请只输出分类结果（一个词），不要输出其他内容。"""

        try:
            response = self.ai_responder.generate_response(prompt, enable_search=False)
            category_str = response.strip().lower()

            # 映射到枚举
            category_map = {
                "question": CommentCategory.QUESTION,
                "suggestion": CommentCategory.SUGGESTION,
                "discussion": CommentCategory.DISCUSSION,
                "praise": CommentCategory.PRAISE,
                "greeting": CommentCategory.GREETING,
                "emoji_only": CommentCategory.EMOJI_ONLY,
                "spam": CommentCategory.SPAM,
            }

            category = category_map.get(category_str, CommentCategory.DISCUSSION)

            return ClassificationResult(
                category=category,
                confidence=0.9,
                reason=f"AI 分类结果: {category_str}",
            )
        except Exception as e:
            print(f"AI 分类失败: {e}")
            return self._rule_based_classify(body)
