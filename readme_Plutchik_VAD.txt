Aim: To get "scores" of text on the basis of:-

A) 8 emotions defined by psychologist named Plutchik.
The said emotions are: 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', and 'trust'.

B) 3 distinguised components of emotions : 'Valence', 'Arousal', and 'Dominance'

Libraries used: 
1. nltk.corpus stopwords- for removing common words of english that serve little to no purpose when it comes to analysing emotions
2. re - use of regular expressions was done to get rid of punctutations
3. pandas - to read the data file and access desired information
4. matplotlib - for visualisation of results ("scores")
5. nltk.corpus wordnet - for finding synonyms and antonyms of words

How it works: 
The data used has over 20k lexicons each rated on their 'valence', 'dominance', 'arousal' and their association with the 8 emotions defined by Plutchik alongwith the itensity with which they assosiate to that label. 

One way to analyse text is to "add up" the intensity scores of these labels and present a summarised result of intensities indexed by the label they represent. This is not entirely accurate as language can, and often times is, subjective and mostly comes with subtext. This is, however, an attempt to get an insight into what goes into making a portion of speech dominant, biased, or even angry or happy. With this due acknowledgement should be given to the fact that these numbers are merely indicators of the emotion speaker/author might be going for. 

