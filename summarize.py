import torch
from transformers import BartForConditionalGeneration, BartTokenizer
# Generate summary on text with <= 1024 tokens


def generate_summary(long_text: str):
    bart_model = BartForConditionalGeneration.from_pretrained(
        'facebook/bart-large-cnn')
    bart_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
   # tokenize without truncation
    inputs_no_trunc = bart_tokenizer(
        long_text, max_length=None, return_tensors='pt', truncation=False)

    # get batches of tokens corresponding to the exact model_max_length
    chunk_start = 0
    chunk_end = bart_tokenizer.model_max_length  # == 1024 for Bart
    inputs_batch_lst = []
    while chunk_start <= len(inputs_no_trunc['input_ids'][0]):
        # get batch of n tokens
        inputs_batch = inputs_no_trunc['input_ids'][0][chunk_start:chunk_end]
        inputs_batch = torch.unsqueeze(inputs_batch, 0)
        inputs_batch_lst.append(inputs_batch)
        chunk_start += bart_tokenizer.model_max_length  # == 1024 for Bart
        chunk_end += bart_tokenizer.model_max_length  # == 1024 for Bart

    # generate a summary on each batch
    summary_ids_lst = [bart_model.generate(
        inputs, num_beams=4, max_length=120, early_stopping=True) for inputs in inputs_batch_lst]

    # decode the output and join into one string with one paragraph per summary batch
    summary_batch_lst = []
    for summary_id in summary_ids_lst:
        summary_batch = [bart_tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_id]
        summary_batch_lst.append(summary_batch[0])
    summary_all = '\n'.join(summary_batch_lst)
    return summary_all
