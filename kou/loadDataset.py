from datasets import load_dataset

#VoiceAssistant-400kのデータセットを取得する
dataset = load_dataset("gpt-omni/VoiceAssistant-400k", split="train")

print(dataset[0]["question"])