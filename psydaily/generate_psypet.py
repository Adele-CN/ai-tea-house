#!/usr/bin/env python3
"""
PsyPet 角色生成器 - 使用 Fal.ai
生成 4 个候选角色图
"""

import os
import requests
import json
from datetime import datetime

FAL_KEY = "545d5972-af84-4f29-b766-ed700c26dc01:da5b68161eac0c298cb75e787322ed42"
OUTPUT_DIR = "/root/.openclaw/workspace/psydaily/assets/psypet"

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4 个角色提示词
CHARACTERS = [
    {
        "name": "茶宠小僧",
        "filename": "tea_monk.png",
        "prompt": "A tiny cute monk meditating inside a ceramic tea cup, zen minimalist style, soft warm lighting, peaceful expression, traditional Chinese tea ceremony setting, studio ghibli inspired, kawaii style, high detail, 8k quality"
    },
    {
        "name": "信息小怪兽",
        "filename": "info_monster.png",
        "prompt": "A cute small monster overwhelmed by swirling digital information, spirals of binary code and notifications surrounding it, pixel art meets studio ghibli style, big innocent eyes, slightly confused but endearing expression, pastel colors with neon accents, soft lighting, emotional storytelling"
    },
    {
        "name": "心理学猫头鹰",
        "filename": "psy_owl.png",
        "prompt": "A wise owl wearing round reading glasses, sitting on a stack of psychology books, minimalist zen aesthetic, soft cream and sage green color palette, clean lines, modern illustration style, warm intelligent eyes, peaceful atmosphere"
    },
    {
        "name": "禅宗小狐狸",
        "filename": "zen_fox.png",
        "prompt": "A small fox meditating in lotus position, zen garden background with raked sand patterns, Japanese ink painting meets kawaii style, soft orange and cream colors, peaceful expression with half-closed eyes, minimalist composition, tranquil atmosphere"
    }
]

def generate_image(prompt, output_path):
    """使用 Fal.ai 生成图片"""
    try:
        # Fal.ai API endpoint for Flux
        url = "https://fal.run/fal-ai/flux/dev"
        
        headers = {
            "Authorization": f"Key {FAL_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "image_size": "square_hd",  # 1024x1024
            "num_inference_steps": 28,
            "guidance_scale": 3.5,
            "enable_safety_checker": False
        }
        
        print(f"🎨 正在生成: {os.path.basename(output_path)}")
        response = requests.post(url, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            # 获取图片 URL
            image_url = result.get('images', [{}])[0].get('url')
            
            if image_url:
                # 下载图片
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"✅ 已保存: {output_path}")
                    return True
        
        print(f"❌ 生成失败: {response.status_code} - {response.text[:200]}")
        return False
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    print("🚀 PsyPet 角色生成器")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = []
    
    for char in CHARACTERS:
        print(f"\n📦 角色: {char['name']}")
        output_path = os.path.join(OUTPUT_DIR, char['filename'])
        success = generate_image(char['prompt'], output_path)
        results.append({
            'name': char['name'],
            'filename': char['filename'],
            'success': success,
            'path': output_path if success else None
        })
    
    print("\n" + "=" * 60)
    print("📊 生成结果:")
    for r in results:
        status = "✅" if r['success'] else "❌"
        print(f"{status} {r['name']}: {r['filename']}")
    
    print(f"\n💾 输出目录: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
