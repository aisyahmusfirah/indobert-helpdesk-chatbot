# 🧪 LOCAL TESTING GUIDE - Before Deploy to Bot

## Opsi Testing Tersedia

### **OPSI 1: CEPAT ⚡ (30 detik)**
Test vocab loading only - verifikasi vocab.txt accessible:

```bash
cd Demo-day\day-2-deployment
python quick_test.py
```

Output yang diharapkan:
```
✅ vocab.txt found: 21128 tokens
✅ Backend will use this vocab
```

---

### **OPSI 2: MEDIUM 🟡 (2-3 menit)**
Test actual tokenizer dengan sample messages:

```bash
cd Demo-day\day-2-deployment
python test_server_local.py
```

Apa yang terjadi:
1. Load BERT model (1-2 menit)
2. Test 7 sample messages (berbagai case)
3. Tampilkan response + [UNK] token count
4. Masuk ke interactive mode (ketik pesan apapun)

Expected output:
```
✅ Model loaded successfully!

Test 1: Lowercase greeting
  Input:  "halo"
  Output: "halo juga! ada yang bisa saya bantu?"
  [UNK] tokens: 0
  ✅ PASS - No [UNK] tokens!
```

Exit interactive mode: ketik `exit` atau tekan `Ctrl+C`

---

### **OPSI 3: LENGKAP 🟢 (untuk debugging)**
Full test dengan semua validasi:

```bash
cd Demo-day\day-2-deployment
python test_full_tokenizer.py
```

(Lebih slow karena test lebih detail)

---

## 📋 STEP-BY-STEP: Recommended Flow

### **BEFORE Deploy ke Bot:**

1. **Quick vocab check (30 sec)**
   ```bash
   python quick_test.py
   ```
   Pastikan output: `✅ vocab.txt found`

2. **Local server test (3 min)**
   ```bash
   python test_server_local.py
   ```
   
   Test sample messages:
   - Ketik: `halo`
   - Verify: Response tanpa [UNK] tokens
   - Ketik: `HALO` (uppercase)
   - Verify: Response tanpa [UNK] tokens
   - Ketik: berbagai kalimat lainnya
   
   Sampai puas → ketik `exit`

3. **Deploy ke Bot**
   ```bash
   python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 🎯 Apa yang Dicek di Test

### Test akan verify:
✅ Model loads correctly  
✅ Tokenizer wrapping works  
✅ do_lower_case=True applied  
✅ Local vocab used  
✅ No [UNK] tokens (atau minimal)  
✅ Response generated  

### Jika ada [UNK] tokens:
Check:
1. vocab.txt path correct?
2. Model checkpoint exists?
3. Server properly restarted?

---

## 💡 Interactive Mode Tips

Di interactive mode bisa test:
- Berbagai case: "halo", "HALO", "HaLo"
- Berbagai sentence: "apa kabar", "siapa nama kamu", dll
- Indonesian slang/informal language
- Punctuation: "halo?", "halo!", dll

Keluarkan saat sudah confident, lalu deploy ke bot.

---

## ⏱️ Time Estimate

| Test | Time | Recommended |
|------|------|-------------|
| `quick_test.py` | 30 sec | Always run first |
| `test_server_local.py` | 3 min | Run before deploy |
| `test_full_tokenizer.py` | 5 min | Debug jika ada issue |

---

## ✅ Signs Everything is Working

```
✅ quick_test.py: vocab.txt found + [UNK] ID shown
✅ test_server_local.py: Model loads + responses have 0 [UNK] tokens
✅ Interactive mode: Responses sensible + no [UNK] tokens
```

If all above checks pass → **READY TO DEPLOY TO BOT** 🚀

---

## 🚀 Deployment Command (After Testing)

```bash
cd Demo-day\day-2-deployment
python -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Then test di Discord bot!

---

## 📝 Notes

- Tests use same engine as FastAPI server
- No bot needed for testing
- Can run multiple times
- Safe to run (non-destructive)
- All tests print debug info for troubleshooting
