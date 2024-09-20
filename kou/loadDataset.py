from datasets import load_dataset

print("Loading Dataset")

#VoiceAssistant-400kのデータセットを取得する
dataset = load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

print("Loaded Dataset")

#`split_name`列の`identity`のデータを抽出したデータセット
dataset_identity = dataset.filter(lambda example: example["split_name"] == "identity")

print("Extracted Dataset")

#`question`のテキストデータを抽出したリスト
question_text_list = dataset_identity["question"]

print(question_text_list[0:3])