
# 一括でインポートできるようにするため、以下のように変更します
from .translate_en2ja_prompt import *
from .translate_text2spoken_prompt import *

# __all__リストを更新して、すべてのインポートされた変数を含めます
__all__ = [
    "translate_en2ja_prompt",
    "translate_en2ja_system_prompt",
    "translate_text2spoken_prompt",
    "translate_text2spoken_system_prompt",
    "translate_text2spoken_filler_system_prompt"
]