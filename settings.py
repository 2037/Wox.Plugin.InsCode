import json

def preset_fn(preset_prompt): return {
    "role": "system", "content": preset_prompt}

def load_prompts():
    with open('presets.json', 'r') as f:
        presets = json.load(f)
    return presets

def list_prompts():
    with open('presets.json', 'r') as f:
        presets = json.load(f)
    return [preset for preset in presets]
    
def set_prompts(prompts):
    with open('presets.json', 'w+') as f:
        json.dump(prompts, f)

def add_propmts(name,prompt):
    with open('presets.json', 'r') as f:
        presets = json.load(f)
    content = preset_fn(prompt)
    presets["name"] = content
    set_prompts(prompts=presets)
