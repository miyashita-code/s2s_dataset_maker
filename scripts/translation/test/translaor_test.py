import pytest
import asyncio
import json
import os
from typing import List
import sys

sys.path.insert(0, './')

from dotenv import load_dotenv
from scripts.translation.translator import Translator

import pytest_asyncio

@pytest.mark.asyncio
class TestTranslator:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        load_dotenv()
        self.translator = Translator(api_key=os.getenv("OPENAI_API_KEY"))
        
        # テスト用の入力データを定義
        self.batch_en_texts = [
            "How does your process work?",
            "Hello! I'm Omni, your friendly voice assistant. My process involves using advanced AI algorithms to understand and respond to your questions in real-time, allowing me to provide helpful answers and solutions.",
            """Sure! Imagine you have a stack of shirts sorted by size, but they're all mixed up. You want to arrange them from the smallest to the largest. Bubble sort works by comparing two shirts at a time, starting with the first two. If the first shirt is larger than the second, you swap them. Then, you move to the next pair and do the same until you reach the end. This process is repeated from the beginning until no more swaps are needed. It's called 'bubble sort' because the largest items slowly "bubble up" to the top of the list."""
        ]

        self.batch_written_texts_for_filler = [
            "次のそれぞれを、麺類、ご飯類と分類してください。 お寿司、チャーハン、ラーメン、きつねそば、うな重、かまたまうどん",
            "以下のキュウリに関する文章から、実が大きくならない理由を挙げてください。 キュウリの実が大きくならない理由はいくつかありますが、一番の多い原因は温度管理によるものです。初夏と晩夏の温度管理が難しいため、この頃は収穫量が少なくなる時期です。生育適温内で収穫のピークを迎えるように苗を植え付けるようにしましょう。 次にチェックしておきたいのは水分と養分の管理です。生育初期に水分や養分を与えすぎると軟弱な株に育ってしまいます。特に肥料（元肥・追肥）が多いと本来、栄養や水分を求めて広く深く張るはずの根が軟弱に育って、草丈が大きくなってからの水分・養分の吸収力に大きな影響が出てしまうので注意してください",
            "老舗百貨店の店員として、以下のお客様からの要望を満たす品物を選び、５００文字以内で簡潔に文章にまとめてください。 海外からのお客様にお渡しするお土産として、軽くてかさばらず、持ち帰る際に壊れにくい、日本の伝統的な品物を選んでください。当方は４０代女性で、お渡し先は６０代の欧米人のご夫婦です。"
        ]

        self.batch_written_texts = [
            "ゼリーを作るためには、以下の材料が必要になります。 ジュース,ゼラチン,砂糖 ジュースの味を変えることで、いろいろな味のゼリーを作ることができます。その日の気分によってジュースの味を変えて試してみると良いかもしれません。",
            "日本語を母国語としない人々にとって、「日本語は非常に難しい言語である」と言われています。 その理由として、 ・漢字、ひらがな、カタカナ、と表記が何種類もある。 ・同一の漢字でも音読みと訓読みがある ・地名の読みが難しい ・主語、述語が省略される などが挙げられます。 そして、やっと基本的な日本語を習得してもさらなる壁が立ちはだかっているのです。 例えば、「はやくいって」、この言葉がすべて平仮名で書かれていたり会話の中で出てきた場合です。 外国人のＡ君が大学の講義を終えてアルバイト先に向かっているとき、校門で日本人の友達Ｂ君に出会い進路相談をされ、１時間が経過してしまいます。さすがにもうアルバイトの開始時間に間に合わない！！そこでＡ君はＢ君に急いでいることを伝えると…Ｂ君から「はやくいって！」と言われました。 Ａ君はその言葉の意味を理解しかねてしばし立ち尽くしてしまいます。 「はやくいって」は、「早く言って」と「早く行って」の両方の解釈が出来てしまうのです。 １，アルバイトがあって急いでいるのなら、その旨をB君に「早く言って」ほしかった。 ２，アルバイトがあって急いでいるのなら、アルバイト先に「早く行って」 上記のように、複数の解釈ができる日本語が多く存在しており、「習得に時間がかかる言語である」といわれる理由の一つです。",
            "「それな」という表現は、主に若い世代やSNSなどのコミュニケーションで使用される表現です。肯定的な意味を持ち、相手の発言に対して、相づちを打つときに使われる若者の言葉です。 「そうだよね！」に近い意味で使われます。また、肯定だけではなく、興味のない話や、話を早く終わらせたいときにも使われるようです。語源は、巨大匿名掲示板から出たネットスラングだという説や、関西弁の「ほんまそれな」の「ほんま」が省略され、「それな」だけが残ったのではいかという説があります。"
        ]
    
    @pytest.mark.parametrize(
        "method, input_data, expected_method",
        [
            ("translate_en2ja", "batch_en_texts", "translate_en2ja"),
            ("translate_text2spoken", "batch_written_texts", "translate_text2spoken"),
            ("translate_text2spoken_with_filler", "batch_written_texts_for_filler", "translate_text2spoken_with_filler"),
        ]
    )
    async def test_translation(self, method, input_data, expected_method):
        translator_method = getattr(self.translator, method)
        input_texts = getattr(self, input_data)
        
        translations = []
        for text in input_texts:
            translated = await translator_method(text)
            translations.append(translated)


        assert translations is not None, f"{method} の結果が None です。"
        assert isinstance(translations, list), f"{method} の結果がリストではありません。"
        assert len(translations) == len(input_texts), f"{method} の結果の長さが入力データと一致しません。"
        assert all(isinstance(item, str) for item in translations), f"{method} の結果に文字列以外のデータが含まれています。"

    async def test_batch_translation(self):
        # バッチ翻訳を実行
        batch_enja = await self.translator.batch_translate_en2ja(self.batch_en_texts)
        batch_text2spoken = await self.translator.batch_translate_text2spoken(self.batch_written_texts)
        batch_text2spoken_with_filler = await self.translator.batch_translate_text2spoken_with_filler(self.batch_written_texts_for_filler)
        
        # 結果をまとめる
        results = {
            "batch_translate_en2ja_from" : self.batch_en_texts,
            "batch_translate_en2ja_to": batch_enja,
            "batch_translate_text2spoken_from": self.batch_written_texts,
            "batch_translate_text2spoken_to": batch_text2spoken,
            "batch_translate_text2spoken_with_filler_from": self.batch_written_texts_for_filler,
            "batch_translate_text2spoken_with_filler_to": batch_text2spoken_with_filler
        }
        
        # 結果をJSONファイルに保存
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        
        # アサーションで結果がNoneでないことを確認
        for key, result in results.items():
            assert isinstance(result, list), f"{key} の結果がリストではありません。"
            assert all(item is not None for item in result), f"{key} の中に None が含まれています。"
    
    async def test_batch_translation_with_load_balancing(self):
        """
        負荷分散テスト:
        max_size=5でn=13の入力を渡し、バッチ翻訳が正しく分割・処理されることを確認する。
        """
        # テスト用の入力データを13個作成
        test_input = ["負荷分散テストです"] * 13
        max_size = 5
        
        # バッチ翻訳を実行
        translations = await self.translator.batch_translate_en2ja(test_input, max_size=max_size)
        
        # 結果のアサーション
        assert translations is not None, "翻訳結果が None です。"
        assert isinstance(translations, list), "翻訳結果がリストではありません。"
        assert len(translations) == 13, f"翻訳結果の長さが13ではありません。実際の長さ: {len(translations)}"
        assert all(isinstance(item, str) for item in translations), "翻訳結果に文字列以外のデータが含まれています。"
        for translated in translations:
            assert translated != "負荷分散テストです", "翻訳が正しく行われていません。"
