#!/usr/bin/env python3
"""
LOCAL TEST SERVER - Test [UNK] token fix tanpa Discord bot
Jalankan script ini untuk test model response sebelum deploy ke bot
"""
import sys
from pathlib import Path

# Setup paths
BACKEND_ROOT = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from backend.app.engines.bert_engine import BertChatEngine

print("="*70)
print("🧪 LOCAL TEST - BERT CHATBOT [UNK] TOKEN FIX")
print("="*70)
print()

# Load model
print("📥 Loading BERT model...")
print("   (This may take a moment...)\n")

try:
    engine = BertChatEngine()
    engine.load()
    print("\n✅ Model loaded successfully!\n")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test cases
print("="*70)
print("📊 TEST CASES - Send berbagai format input")
print("="*70)
print()

test_messages = [
    ("halo", "Lowercase greeting"),
    ("HALO", "UPPERCASE greeting"),
    ("Halo Apa Kabar?", "Mixed case with punctuation"),
    ("halo ada yang bisa saya bantu?", "Full lowercase sentence"),
    ("HALO ADA YANG BISA SAYA BANTU?", "Full UPPERCASE sentence"),
    ("apa kabar", "Simple lowercase"),
    ("APA KABAR", "Simple UPPERCASE"),
]

for i, (message, description) in enumerate(test_messages, 1):
    print(f"Test {i}: {description}")
    print(f"  Input:  \"{message}\"")
    
    try:
        response = engine.reply(message, beam_size=1)
        
        # Check for [UNK] tokens
        unk_count = response.count('[UNK]')
        
        print(f"  Output: \"{response}\"")
        print(f"  [UNK] tokens: {unk_count}")
        
        if unk_count == 0:
            print(f"  ✅ PASS - No [UNK] tokens!\n")
        elif unk_count <= 2:
            print(f"  ⚠️  WARNING - {unk_count} [UNK] tokens (may be acceptable)\n")
        else:
            print(f"  ❌ FAIL - Too many [UNK] tokens!\n")
        
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

print("="*70)
print("📝 INTERACTIVE MODE - Type pesan apapun (ketik 'exit' untuk keluar)")
print("="*70)
print()

while True:
    try:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\n✅ Goodbye!")
            break
        
        if not user_input:
            continue
        
        response = engine.reply(user_input, beam_size=3)
        unk_count = response.count('[UNK]')
        
        print(f"Bot: {response}")
        print(f"[UNK] tokens: {unk_count}\n")
        
    except KeyboardInterrupt:
        print("\n\n✅ Test stopped")
        break
    except Exception as e:
        print(f"Error: {e}\n")

print("\n" + "="*70)
print("✅ TEST COMPLETE")
print("="*70)
print()
print("If all tests passed with 0 [UNK] tokens, bot is ready to deploy! 🚀")
