import nltk
from nltk.corpus import wordnet
import pandas as pd
import re
from random_word import RandomWords
import time
import contractions


puns_dt = pd.read_csv("dad_jokes.csv").iloc[0:10]



def transform_mc(df,col,random=2,synonym=1,antonym=1,mc_length=5):
    tmp_lst = list(df[col].values)


    def deEmojify(inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

    clean_lst = [deEmojify(str(i)) for i in tmp_lst]


    processed_lst = []
    split_line_list = []
    for i in clean_lst:
        synonyms = []
        antonyms = []
        last_word = i.split()[-1]
        split_line = i.rsplit(' ', 1)[0]
        split_line_list.append(split_line)
        last_word = re.sub(r'[^\w\s]','',last_word)

        print("Original sentence: " + i)
        print("Last Word: " + last_word)
        #print(split_line)

        for syn in wordnet.synsets(last_word):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())

        #print(list(set(synonyms)))
        #print(set(antonyms))

        syn_pool = list(set(synonyms))[0:synonym]
        ant_pool = list(set(antonyms))[0:antonym]
        r = RandomWords()
        total_pool = syn_pool + ant_pool + [last_word]

        remaining_length = mc_length - len(total_pool)

        if remaining_length>0:
            time.sleep(3)

            try:
                tmp_lst = r.get_random_words(limit=remaining_length)
            except:
                tmp_lst = ["hello" for i in range(remaining_length)]
            #print(tmp_lst)


            total_pool = syn_pool + ant_pool + tmp_lst + [last_word]

            processed_lst.append(total_pool)
        print("new word choices: {}".format(total_pool))
        print("\n")



    d1 = {"Body": processed_lst}
    df2 = pd.DataFrame(d1)

    df3 = df2[['body1','body2','body3','body4','body5']] = pd.DataFrame(df2.Body.values.tolist(), index= df2.index)
    #df3[col] = df[col]
    #df["WordChoice1"] =
        #random_pool = [r.get_random_word() for i in range(random)]


    #print(df3)
    for i in range(mc_length):
        df["Word_{}".format(i+1)] = df3[i]

    df["correct_last_word"] = df["Word_{}".format(mc_length)]
    df["processed_sentence"] = split_line_list
    print(df)


        # Return a single random word







transform_mc(puns_dt, col = "Body")
