from flask import Flask, render_template, request, url_for
#from flask_pymongo import PyMongo
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize 
from nltk.corpus import wordnet
import re

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/analysis',methods=['GET'])
def Analysis():
    return render_template('analysis.html')

@app.route('/summary',methods=['GET'])
def Summary():
    return render_template('summary.html')

@app.route('/syn',methods=['GET'])
def Syn():
    return render_template('syn.html')

@app.route("/score", methods=['POST'])
#@app.route("/score")
def score():
    
    data_vad=pd.read_excel("VAD.xlsx")
    
    data=pd.read_excel("FIRST_8_EMO.xlsx")
    data.fillna(0, inplace=True)
    datas=pd.get_dummies(data, columns=['emotion'])

    datas['emotion_sadness']=datas['emotion_sadness'].multiply(datas['emotion-intensity-score'])
    datas['emotion_anger']=datas['emotion_anger'].multiply(datas['emotion-intensity-score'])
    datas['emotion_anticipation']=datas['emotion_anticipation'].multiply(datas['emotion-intensity-score'])
    datas['emotion_fear']=datas['emotion_fear'].multiply(datas['emotion-intensity-score'])

    datas['emotion_joy']=datas['emotion_joy'].multiply(datas['emotion-intensity-score'])
    datas['emotion_disgust']=datas['emotion_disgust'].multiply(datas['emotion-intensity-score'])
    datas['emotion_surprise']=datas['emotion_surprise'].multiply(datas['emotion-intensity-score'])
    datas['emotion_trust']=datas['emotion_trust'].multiply(datas['emotion-intensity-score'])

    del datas['emotion-intensity-score']


    def clean_text(text):
        # remove backslash-apostrophe 
        text = re.sub("\'", "", text) 
        # remove everything except alphabets 
        text = re.sub("[^a-zA-Z]"," ",text) 
        # remove whitespaces 
        text = ' '.join(text.split()) 
    
        text = text.lower() 
        return text

    stop_words = set(stopwords.words('english'))

    # function to remove stopwords
    def remove_stopwords(text):
        no_stopword_text = [w for w in text if not w in stop_words]
        return ' '.join(no_stopword_text)


    def score_vad(sentence):
        corpuso=clean_text(sentence)
        corpuso=corpuso.split(' ')
        corpuso=remove_stopwords(corpuso)
        corpuso=corpuso.split(' ')
        return data_vad.loc[data_vad['Word'].isin(corpuso)].sum(axis = 0, skipna = True)[1:]

    def score_emo(sentence):
        corpuso=clean_text(sentence)
        corpuso=corpuso.split(' ')
        corpuso=remove_stopwords(corpuso)
        corpuso=corpuso.split(' ')
        return datas.loc[datas['word'].isin(corpuso)].sum(axis = 0, skipna = True)[1:]

    def same(x):
        return x
    
    #THE MAIN THING

    if request.method == 'POST':
        message=request.form['Text']
        data= message
        output1 = score_vad(data)
        output2 = score_emo(data)
        sum_emo = sum_vad = 0
        for i in range(0, 2):
            sum_vad += output1[i]
        for i in range(0, 2):
            output1[i] = round((output1[i]/sum_vad)*10, 2)

        for i in range(0, 7):
            sum_emo += output2[i]
        if sum_emo != 0:
            for i in range(0, 7):
                output2[i] = round((output2[i]/sum_emo)*10, 2)
        x = same(data)
        
    return render_template('emo_result.html', message = " {} ".format(x), predictionVAD_Valence=" {} ".format(output1[0]) ,predictionVAD_Arousal=" {} ".format(output1[1]) , predictionVAD_Dominance=" {} ".format(output1[2])
    , predictionEMO_anger=" {} ".format(output2[0]), predictionEMO_anticipation=" {} ".format(output2[1]), predictionEMO_disgust=" {} ".format(output2[2]), predictionEMO_fear=" {} ".format(output2[3]), predictionEMO_joy=" {} ".format(output2[4]), predictionEMO_sadness=" {} ".format(output2[5]), predictionEMO_surprise=" {} ".format(output2[6]), predictionEMO_trust=" {} ".format(output2[7]) )
    
@app.route("/summary", methods=['POST'])
def summary():
    if request.method == 'POST':
        data=request.form['Text']
                
        def clean_text(text):
            # remove backslash-apostrophe 
            text = re.sub("\'", "", text) 
            # remove everything except alphabets 
            text = re.sub("[^a-zA-Z]"," ",text) 
            # remove whitespaces 
            text = ' '.join(text.split()) 
            text = text.lower() 
            return text

    stop_words = set(stopwords.words('english'))

    # function to remove stopwords
    def remove_stopwords(text):
        no_stopword_text = [w for w in text if not w in stop_words]
        return ' '.join(no_stopword_text)

    sentence = data
    corpuso=clean_text(sentence)
    corpuso=corpuso.split(' ')
    corpuso=remove_stopwords(corpuso)
    corpuso=corpuso.split(' ')

    freqTable = dict() 
    for word in corpuso: 
        word = word.lower() 
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1

    sentences = sent_tokenize(data) 
    sentenceValue = dict() 
    
    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 
    
    
    
    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue)) 
    
    # Storing sentences into our summary. 
    summary = '' 

    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)): 
            summary += " " + sentence 
    if (len(summary)==0):
        d=data
    else:
        d=summary 
    return render_template('summary.html', data=" {} ".format(data), d=" {} ".format(d))

@app.route("/syn", methods=['POST'])

def syn():
    if request.method == 'POST':
        data=request.form['Text']

    synonyms = []
    antonyms = []
    for syn in wordnet.synsets(data):
            
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
    
   
    d1= synonyms
    d2= antonyms

    return render_template('syn.html', data= " {} ".format(data), d1=" {} ".format(d1), d2=" {} ".format(d2))

if __name__=="__main__":
    app.run(debug=False)
