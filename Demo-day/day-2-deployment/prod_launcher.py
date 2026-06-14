import subprocess
import time
import sys
import os

print("="*60)
print("  LAUNCHER PRODUCTION LIGHTWEIGHT SYSTEM - CHATBOT BERT  ")
print("="*60)

# Ambil lokasi python dari virtual environment yang sedang aktif
python_exe = sys.executable
current_dir = os.path.dirname(os.path.abspath(__file__))

print(f"[1/2] Menyalakan Jantung Backend (FastAPI) di Port 8000...")
# Menjalankan Uvicorn sebagai background process murni Python
backend_process = subprocess.Popen(
    [python_exe, "-m", "uvicorn", "main:app", "--port", "8000"],
    cwd=current_dir
)

# Kasih jeda 5 detik agar server FastAPI beres memuat Vocab IndoBERT terlebih dahulu
time.sleep(5)

print(f"[2/2] Menyalakan Gateway Frontend (Bot Discord)...")
# Menjalankan Bot Discord sebagai background process murni Python
bot_process = subprocess.Popen(
    [python_exe, "bot.py"],
    cwd=current_dir
)

print("\n" + "="*60)
print("🎉 BERHASIL! FastAPI dan Bot Discord sekarang berjalan berbarengan!")
print("Indikator Bot di Discord sekarang HARUSNYA SUDAH HIJAU (ONLINE).")
print("="*60)
print("Silakan lakukan demo !chat + mention di kelas.")
print("Tekan CTRL + C di terminal ini jika ingin mematikan kedua sistem sekaligus.\n")

try:
    # Menjaga skrip utama tetap hidup agar background process di atas tidak ikut mati
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Mematikan seluruh sistem chatbot secara aman...")
    backend_process.terminate()
    bot_process.terminate()
    print("👋 Semua proses berhasil dihentikan. Sampai jumpa!")