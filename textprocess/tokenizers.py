
import spacy
nlp = spacy.load('en_core_web_sm')
def tokenize_text(text , dropped_pos_ = []):
    lda_tokens = []
    doc = nlp(text)
    for token in doc:
        if token.is_space or token.is_punct or token.is_stop or token.pos_  in dropped_pos_:
            continue
        else:
            lda_tokens.append(token.lemma_)
    return lda_tokens
