import codecs
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk


CHAT_NAME = "PIONEER_CHAT.TXT"
STOPWORDS_FILENAME = "STOPWORDS.TXT"
FONTPATH = 'FreeSans\\FreeSansBold.ttf'

def get_file_text(filename):
    f = codecs.open(filename, 'r', 'utf-8')
    text = f.read()
    f.close()
    return text


def get_stopwords():
    return eval(get_file_text(STOPWORDS_FILENAME))


def strip_emoji(text, EMOJI_PATTERN):
    return EMOJI_PATTERN.sub(r'', text)


def preprocess_msg(msg):
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251" 
        "]+"
    )

    msg = re.sub('\d{2}\/\d{2}\/\d{4}, \d{1,2}:\d{1,2} - .+?:', '', msg)
    msg = re.sub('ח{2,}', '', msg)
    msg = re.sub('[.!?\\-:]', '', msg)
    msg = strip_emoji(msg, EMOJI_PATTERN)
    msg = msg.strip()
    return msg


def get_wordlist(text):
    words = []
    stopwords = get_stopwords()
    msgs = text.split('\n')
    for i in range(len(msgs)):
        msgs[i] = preprocess_msg(msgs[i])
        words += msgs[i].split(' ')
    for i in range(len(words)):
        try:
            if(ord(words[i][0])>1400 and ord(words[i][0])<1600):
                if(words[i].lower() not in stopwords):
                    words[i] = words[i][::-1]
                else:
                    words[i] = ''
            else:
                words[i] = ''
        except:
            pass
    words = [x for x in words if x != '']
    return words


def plot_wordcloud():
    fd = nltk.FreqDist(get_wordlist(get_file_text('pioneer_chat.txt')))
    s = sorted(fd, key = fd.__getitem__, reverse = True)

    wcloud = WordCloud(font_path=FONTPATH).generate_from_frequencies(fd)

    plt.imshow(wcloud, interpolation = 'bilinear')
    plt.axis('off')
    plt.show()


def main():
    plot_wordcloud()


if __name__ == '__main__':
    main()
