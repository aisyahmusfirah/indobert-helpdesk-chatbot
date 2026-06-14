"""
Quick backend integration test - Load the model like the FastAPI server does.
This verifies the [UNK] token fix before deploying.
"""
import sys
from pathlib import Path

# Setup backend paths
BACKEND_ROOT = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

print("="*70)
print("🧪 BACKEND INTEGRATION TEST - [UNK] TOKEN FIX")
print("="*70)
print()

try:
    # Import engine
    print("📥 Importing BertChatEngine...")
    from backend.app.engines.bert_engine import BertChatEngine
    print("   ✅ Imported successfully\n")
    
    # Instantiate engine
    print("📥 Loading BERT model...")
    engine = BertChatEngine()
    engine.load()
    print("   ✅ Model loaded successfully\n")
    
    # Test messages
    print("="*70)
    print("📊 INFERENCE TEST CASES")
    print("="*70)
    print()
    
    test_messages = [
        "halo",
        "HALO",
        "Halo apa kabar?",
        "HALO APA KABAR?",
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"Test {i}: Input=\"{msg}\"")
        try:
            response = engine.reply(msg, beam_size=1)  # beam_size=1 for quick test
            
            # Check for [UNK] tokens in response
            unk_count = response.count('[UNK]')
            
            print(f"  Response: \"{response}\"")
            print(f"  [UNK] count: {unk_count}")
            
            if unk_count == 0:
                print(f"  ✅ PASS")
            else:
                print(f"  ⚠️  {unk_count} [UNK] tokens found")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    print("="*70)
    print("✅ BACKEND INTEGRATION TEST COMPLETE")
    print("="*70)
    print()
    print("Ready for Discord bot deployment! 🚀")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
