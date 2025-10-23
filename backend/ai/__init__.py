"""
AI 模組

提供 OpenAI GPT-4/GPT-5 整合功能
"""

from .gpt5_client import GPT5Client
from .content_generator import ContentGenerator

__all__ = ['GPT5Client', 'ContentGenerator']

