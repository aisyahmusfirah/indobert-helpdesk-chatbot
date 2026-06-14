
import urllib.request
import os

print("Sedang mengunduh berkas BERT pretrained (sekitar 400MB)... Mohon tunggu...")
url = "https://huggingface.co/bert-base-chinese/resolve/main/pytorch_model.bin"
output_dir = "./data"
output_path = os.path.join(output_dir, "pytorch model.bin")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

urllib.request.urlretrieve(url, output_path)
print("Unduhan selesai! Berkas berhasil disimpan di ./data/pytorch model.bin")

