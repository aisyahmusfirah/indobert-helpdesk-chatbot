#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
from torch.utils.data.dataloader import DataLoader
import time
import datetime
import sys

print("Step 1: Loading config...", file=sys.stderr)
from config import Config
print(f"Device: {Config.device}", file=sys.stderr)

print("Step 2: Loading dataset...", file=sys.stderr)
from dataloader import DreamDataset, collate_fn
dataset = DreamDataset()
print(f"Dataset size: {len(dataset)}", file=sys.stderr)

print("Step 3: Creating dataloader...", file=sys.stderr)
dataloader = DataLoader(dataset, batch_size=Config.batch_size, shuffle=True, collate_fn=collate_fn)
print(f"Dataloader created with {len(dataloader)} batches", file=sys.stderr)

print("Step 4: Loading BERT vocab...", file=sys.stderr)
from tokenizer import load_bert_vocab
word2idx = load_bert_vocab()
print(f"Vocab size: {len(word2idx)}", file=sys.stderr)

print("Step 5: Creating BERT config...", file=sys.stderr)
from bert_model import BertConfig
bertconfig = BertConfig(vocab_size=len(word2idx))
print(f"BERT config created", file=sys.stderr)

print("Step 6: Creating Seq2SeqModel...", file=sys.stderr)
from seq2seq_bert import Seq2SeqModel
bert_model = Seq2SeqModel(config=bertconfig)
print(f"Model created", file=sys.stderr)

print("Step 7: Loading pretrained weights...", file=sys.stderr)
from train import load_model
load_model(bert_model, Config.pretrain_model_path)
bert_model.to(Config.device)
print(f"Model loaded to {Config.device}", file=sys.stderr)

print("Step 8: Creating optimizer...", file=sys.stderr)
optim_parameters = list(bert_model.parameters())
optimizer = torch.optim.Adam(optim_parameters, lr=Config.learning_rate, weight_decay=1e-3)
print(f"Optimizer created", file=sys.stderr)

print("Step 9: Starting training...", file=sys.stderr)
step = 0
epoch = 0
for token_ids, token_type_ids, target_ids in dataloader:
    start_time = time.time()
    step += 1
    token_ids = token_ids.to(Config.device)
    token_type_ids = token_type_ids.to(Config.device)
    target_ids = target_ids.to(Config.device)
    
    print(f"Batch {step}: token_ids shape {token_ids.shape}", file=sys.stderr)
    
    predictions, loss = bert_model(token_ids, token_type_ids, labels=target_ids, device=Config.device)
    
    print(f"Loss: {loss.item()}", file=sys.stderr)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    print(f"Step {step} completed in {time.time() - start_time:.2f}s", file=sys.stderr)
    
    if step >= 2:
        print("Test completed successfully!", file=sys.stderr)
        break

print("All tests passed!", file=sys.stderr)
