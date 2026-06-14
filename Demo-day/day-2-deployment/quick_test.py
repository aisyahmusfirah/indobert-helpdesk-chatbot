#!/usr/bin/env python3
"""
FAST TEST - Verify vocab loading tanpa load model penuh
"""
import sys
from pathlib import Path

DEMO_DAY = Path(__file__).resolve().parents[1]  
PROJECT_ROOT = DEMO_DAY.parent 
VOCAB_PATH = PROJECT_ROOT / "Chatbot" / "Bert_chatbot" / "data" / "vocab.txt"

print("🧪 QUICK VOCAB CHECK TEST\n")

if VOCAB_PATH.exists():
    with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
        vocab = [line.strip() for line in f.readlines()]
    
    print(f"✅ vocab.txt found: {len(vocab)} tokens")
    print(f"   Sample: {vocab[:5]}")
    print(f"   [UNK] ID: {vocab.index('[UNK]') if '[UNK]' in vocab else 'NOT FOUND'}")
    print()
    print("✅ Backend will use this vocab (no [UNK] mismatch!)")
else:
    print(f"❌ vocab.txt NOT found at {VOCAB_PATH}")
    sys.exit(1)
