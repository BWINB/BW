def LLM_summarization(text, max_length1):
    from transformers import pipeline

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    ARTICLE = text
    
    print(summarizer(ARTICLE, max_length=max_length1, min_length=30, do_sample=False))