from transformers import AutoConfig, AutoModel, LlamaTokenizerFast

from typing import Dict, List

def get_grouped_params(model, no_decay=["bias", "LayerNorm.weight"]) -> List[Dict]:
    weight_decay = 0.1
    
    params_with_wd, params_without_wd = [], []
    for n, p in model.named_parameters():
        if any(nd in n for nd in no_decay):
            params_without_wd.append(p)
        else:
            params_with_wd.append(p)
    return [
        {"params": params_with_wd, "weight_decay": weight_decay},
        {"params": params_without_wd, "weight_decay": 0.0},
    ]

def get_config(config_path: str):
    config = AutoConfig().from_pretrained(config_path)
    return config

def get_model(config, save_dir: str):
    config.save_pretrained(save_dir)
    return AutoModel().from_config(config)

def get_tokenizer(tokenizer_path: str, save_dir: str):
    tokenizer = LlamaTokenizerFast(
        vocab_file=tokenizer_path
    )
    tokenizer.save_pretrained(save_dir)
    return tokenizer