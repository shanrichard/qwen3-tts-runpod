# handler.py - Qwen3-TTS RunPod Serverless Handler
import base64
import io
import os
import torch
import runpod

# 全局模型缓存（懒加载）
_models = {}

def get_model(mode: str):
    """懒加载模型"""
    global _models
    
    if mode in _models:
        return _models[mode]
    
    from qwen_tts import Qwen3TTSModel
    
    model_map = {
        "custom_voice": "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
        "voice_design": "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        "voice_clone": "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    }
    
    model_name = model_map.get(mode)
    if not model_name:
        raise ValueError(f"Unknown mode: {mode}")
    
    print(f"Loading model for {mode}: {model_name}")
    
    # 不使用 flash_attention，用默认 attention 实现
    model = Qwen3TTSModel.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
    )
    
    _models[mode] = model
    print(f"Model loaded: {mode}")
    return model


def synthesize(job):
    try:
        inp = job["input"]
        mode = inp["mode"]
        text = inp["text"]
        language = inp.get("language", "Chinese")
        
        model = get_model(mode)
        
        if mode == "custom_voice":
            speaker = inp.get("speaker", "Vivian")
            instruct = inp.get("instruct")
            
            wavs, sr = model.generate_custom_voice(
                text=text,
                language=language,
                speaker=speaker,
                instruct=instruct,
            )
        
        elif mode == "voice_design":
            instruct = inp["instruct"]
            
            wavs, sr = model.generate_voice_design(
                text=text,
                language=language,
                instruct=instruct,
            )
        
        elif mode == "voice_clone":
            ref_audio_b64 = inp["ref_audio_b64"]
            ref_text = inp["ref_text"]

            # 解码 base64 并用 soundfile 加载为 numpy array
            import soundfile as sf
            ref_audio_bytes = base64.b64decode(ref_audio_b64)
            ref_audio_buffer = io.BytesIO(ref_audio_bytes)
            ref_audio_data, ref_sr = sf.read(ref_audio_buffer)

            wavs, sr = model.generate_voice_clone(
                text=text,
                language=language,
                ref_audio=ref_audio_data,
                ref_text=ref_text,
            )
        
        else:
            return {"error": f"Unknown mode: {mode}"}
        
        # 转换为 WAV bytes
        import soundfile as sf
        buffer = io.BytesIO()
        sf.write(buffer, wavs[0], sr, format="WAV")
        wav_bytes = buffer.getvalue()
        
        return {
            "status": "success",
            "sample_rate": sr,
            "mime": "audio/wav",
            "wav_base64": base64.b64encode(wav_bytes).decode("utf-8"),
        }
    
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


runpod.serverless.start({"handler": synthesize})
