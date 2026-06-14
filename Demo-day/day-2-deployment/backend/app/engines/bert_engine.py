"""Engine inferensi BERT — memakai kode Chatbot/Bert_chatbot."""
import os
import sys
import re
from pathlib import Path

import torch

from backend.app.config import BERT_CHECKPOINT, CHATBOT_ROOT
from backend.app.engines.base import ChatEngine


class LocalVocabTokenizerWrapper:
    """
    Wrapper untuk tokenizer BERT dengan:
    - Forced local vocab loading (vocab.txt dari training)
    - do_lower_case=True untuk preprocessing
    - Aggressive text cleaning untuk menghilangkan [UNK] tokens
    """
    
    def __init__(self, base_tokenizer, vocab_path: str | Path = None, do_lower_case: bool = True):
        self.base_tokenizer = base_tokenizer
        self.do_lower_case = do_lower_case
        self.vocab_path = Path(vocab_path) if vocab_path else None
        
        # Load vocab dari file lokal jika disediakan
        if self.vocab_path and self.vocab_path.exists():
            self._load_local_vocab(self.vocab_path)
        
    def _load_local_vocab(self, vocab_path: Path):
        """Load vocabulary dari file lokal (vocab.txt)."""
        try:
            with open(vocab_path, 'r', encoding='utf-8') as f:
                vocab_list = [line.strip() for line in f.readlines()]
            
            # Update base tokenizer's vocab dict
            if hasattr(self.base_tokenizer, '_token_dict'):
                # Tokenizer class dengan _token_dict
                new_vocab = {token: idx for idx, token in enumerate(vocab_list)}
                self.base_tokenizer._token_dict = new_vocab
                self.base_tokenizer._token_dict_inv = {v: k for k, v in new_vocab.items()}
                self.base_tokenizer._vocab_size = len(new_vocab)
                print(f"✅ Loaded local vocab dari {vocab_path}: {len(new_vocab)} tokens")
        except Exception as e:
            print(f"⚠️ Error loading vocab: {e}. Menggunakan tokenizer default.")
    
    def _preprocess_text(self, text: str) -> str:
        """Aggressive preprocessing untuk matching training data."""
        if not isinstance(text, str):
            return text
            
        # Step 1: Lowercase (match training config)
        if self.do_lower_case:
            text = text.lower()
        
        # Step 2: Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Step 3: Strip leading/trailing spaces
        text = text.strip()
        
        # Step 4: Remove common punct yang bisa cause tokenizer issues
        # Tapi preserve Indonesian punctuation
        text = text.replace('\\', '')
        text = text.replace('\\n', ' ')
        text = text.replace('\\t', ' ')
        
        return text
    
    def encode(self, text_a, text_b=None, **kwargs):
        """Encode dengan preprocessing aggressive + local vocab."""
        # Preprocess both texts
        text_a = self._preprocess_text(text_a)
        if text_b is not None:
            text_b = self._preprocess_text(text_b)
        
        # Encode dengan base tokenizer (now using local vocab)
        return self.base_tokenizer.encode(text_a, text_b, **kwargs)
    
    def tokenize(self, text, **kwargs):
        """Tokenize dengan preprocessing."""
        text = self._preprocess_text(text)
        return self.base_tokenizer.tokenize(text, **kwargs)
    
    def __getattr__(self, name):
        """Delegate semua method lain ke base_tokenizer."""
        return getattr(self.base_tokenizer, name)


class BertChatEngine(ChatEngine):
    name = "bert"

    def __init__(self, checkpoint: Path | None = None, device: str | None = None):
        self.checkpoint = Path(checkpoint or BERT_CHECKPOINT)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self._model = None

    def load(self) -> None:
        if not self.checkpoint.is_file():
            raise FileNotFoundError(
                f"Checkpoint BERT tidak ditemukan: {self.checkpoint}\n"
                "Latih di Chatbot/Bert_chatbot lalu salin bert_dream.bin ke Demo-day/models/"
            )

        bert_dir = CHATBOT_ROOT / "Bert_chatbot"
        if not bert_dir.is_dir():
            raise FileNotFoundError(f"Folder Bert_chatbot tidak ditemukan: {bert_dir}")
        if str(bert_dir) not in sys.path:
            sys.path.insert(0, str(bert_dir))

        from bert_model import BertConfig
        from seq2seq_bert import Seq2SeqModel
        from tokenizer import load_bert_vocab, Tokenizer

        prev_cwd = os.getcwd()
        os.chdir(bert_dir)
        try:
            word2idx = load_bert_vocab()
            config = BertConfig(len(word2idx))
            model = Seq2SeqModel(config)
            
            # Load local vocab file path
            vocab_path = bert_dir / "data" / "vocab.txt"
            
            # Wrap tokenizer dengan local vocab loading + lowercase + aggressive preprocessing
            base_tokenizer = model.tokenizer
            model.tokenizer = LocalVocabTokenizerWrapper(
                base_tokenizer, 
                vocab_path=vocab_path,
                do_lower_case=True  # Match training config
            )
            
            state = torch.load(self.checkpoint, map_location=self.device)
            model.load_state_dict(state)
            model.eval()
            self._model = model
            print(f"✅ Model BERT loaded from {self.checkpoint}")
            print(f"✅ Tokenizer wrapped dengan local vocab + do_lower_case=True")
        finally:
            os.chdir(prev_cwd)

    def reply(self, message: str, beam_size: int = 3, **kwargs) -> str:
        if self._model is None:
            raise RuntimeError("Model belum dimuat. Panggil load() terlebih dahulu.")
        text = message.strip()
        if not text:
            return "Silakan kirim pesan yang tidak kosong."
        # Preprocess input: lowercase + aggressive cleaning
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return self._model.generate(text, beam_size=beam_size, device=self.device)
