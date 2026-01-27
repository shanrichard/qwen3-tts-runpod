# Qwen3-TTS RunPod Serverless

基于 Qwen3-TTS 的语音合成服务，部署在 RunPod Serverless。

## 支持的模式

1. **custom_voice** - 预设音色 + 情感指令
2. **voice_design** - 文字描述创建声音
3. **voice_clone** - 3秒克隆声音

## 输入示例

### CustomVoice
```json
{
  "mode": "custom_voice",
  "text": "你好，很高兴认识你",
  "speaker": "Vivian",
  "instruct": "用开心的语气说"
}
```

### VoiceDesign
```json
{
  "mode": "voice_design",
  "text": "哥哥你回来啦",
  "instruct": "年轻活泼的女声，带有撒娇的语气"
}
```

## 可用音色 (CustomVoice)

- Vivian - 明亮年轻女声（中文）
- Serena - 温暖温柔女声（中文）
- Uncle_Fu - 低沉醇厚男声（中文）
- Dylan - 清澈自然男声（北京话）
- Eric - 活泼略沙哑男声（四川话）
- Ryan - 动感男声（英文）
- Aiden - 阳光男声（英文）
