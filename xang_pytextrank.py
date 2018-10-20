def top_keywords_sentences(text,stopwords=None, spacy_nlp=None, skip_ner=True, phrase_limit=15, sent_word_limit=150):
    #Parse incoming text
    parse=parse_doc(text2json(text))
    parse_list=[json.loads(pretty_print(i._asdict())) for i in parse]

    #Create and rank graph for keywords
    graph, ranks = text_rank(parse_list)
    norm_rank=normalize_key_phrases(parse_list, ranks, stopwords=stopwords, spacy_nlp=spacy_nlp, skip_ner=skip_ner)
    norm_rank_list=[json.loads(pretty_print(rl._asdict())) for rl in norm_rank ]
    phrases = ", ".join(set([p for p in limit_keyphrases(norm_rank_list, phrase_limit=phrase_limit)]))

    # return a matrix like result for the top keywords
    kernel = rank_kernel(norm_rank_list)

    # Rank the sentences
    top_sent=top_sentences(kernel, parse_list)
    top_sent_list=[json.loads(pretty_print(s._asdict())) for s in top_sent ]
    sent_iter = sorted(limit_sentences(top_sent_list, word_limit=sent_word_limit), key=lambda x: x[1])

    # Return ranked sentences
    s=[]
    for sent_text, idx in sent_iter:
        s.append(make_sentence(sent_text))

    graf_text = " ".join(s)

    return(graf_text,phrases)
