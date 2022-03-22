import re
import sys
import logging

"""
Phrasing is performed on parsed text in IceParser (IceNLP) format, using phrases and special words to determine
speech pauses in text.

See examples of input and output in 'lawparsed.txt' and 'lawphrased.txt'

"""

# long, medium, and short pause labels
PAUSE_LABELS = ['<sil>', '<pau>', '<sp>']
PAUSE_PUNCTUATION = [',', '.', '!', '?']
PHRASE_OPENING = '['
PHRASE_CLOSING = ']'
# Phrase labels
NP = 'NP'  # noun phrase
AP = 'AP'  # adjective phrase
NP_SEQUENCE = 'NPs'
AP_SEQUENCE = 'APs'
PP = 'PP'  # prepositional phrase
CP = 'CP'  # coordinating conjunction
SCP = 'SCP'  # subordinating conjunction
VP = 'VP' # verb phrase,
INJP = 'InjP' # interjection
MWE = 'MWE'  # multi word expression
ADVP = 'AdvP'  # adverbial phrase

# tags
TF = 'tf'
# special words
REL = 'sem'


class Phrasing:
    """The Phrasing class can store three different labels for pauses: short pause, medium pause, and long pause.
    If you only need one or two labels, i.e. only want to label one pause length or only distinguish between
    short or long, you can provide a label as string or a list of three labels, of which two can be the same.
    The default labels are defined in PAUSE_LABELS."""

    def __init__(self, pause_labels=None):
        if pause_labels is None:
            self.long_pause = PAUSE_LABELS[0]
            self.medium_pause = PAUSE_LABELS[1]
            self.short_pause = PAUSE_LABELS[2]
        elif isinstance(pause_labels, str):
            # only one pause label, no differences in length
            self.long_pause = pause_labels
            self.medium_pause = pause_labels
            self.short_pause = pause_labels
        elif isinstance(pause_labels, list) and len(pause_labels) == 3:
            self.long_pause = pause_labels[0]
            self.medium_pause = pause_labels[1]
            self.short_pause = pause_labels[2]
        else:
            ValueError("An argument containing pause labels must either be a label as string or "
                       "a list of three pause labels as strings.")

    def insert_pauses(self, text: list) -> list:
        """Inserts pause labels into parsed text, based on heuristics about where speakers make pauses due to
        beginning/ending of phrases, punctuation, or due to special connection words.
        Input text should be a list of parsed sentences in IceParser format, see file lawparsed.txt"""

        if not self.is_valid_input(text):
            ValueError("Input to phrasing needs to be a list of strings in IceParser format")
        phrase_list = [self.list_phrases(x) for x in text]
        paused_phrases = self.pause_text(phrase_list)
        extracted_text = [self.extract_text(x) for x in paused_phrases]
        paused_text = self.switch_punctuation(extracted_text)
        return paused_text

    def is_valid_input(self, text: list) -> bool:
        """Ensure that the input is a list of parsed sentences in IceParser format (see IceNLP)."""
        if not isinstance(text, list):
            logging.error("Phrasing input is not a list: '" + str(text) + "'")
            return False
        if not text:
            logging.error("Phrasing input is empty")
            return False
        sent = text[0]
        # parsed text should match some kind of [NP ...][VP ...] pattern
        # we assume each sentence contains at least one noun or verb phrase
        if not re.match('\[.+(' + NP + '|' + VP + ').+]', sent):
            logging.error("It seems that the phrasing input is not in IceParser format: '" + str(sent) + "'")
            return False
        return True

    def list_phrases(self, line: str) -> list:
        """ Convert the parsed text into a list of phrases """
        phrase_list = line.split(PHRASE_OPENING)
        clean_phrases = [re.sub(PHRASE_CLOSING, '', item).rstrip(' ') for item in phrase_list]
        tokenized_phrases = [item.split(' ') for item in clean_phrases]
        #delete all empty strings from the phrase list
        return [list(filter(None, item)) for item in tokenized_phrases]

    def pause_text(self, phrased_sentences) -> list:
        """ Insert pauses according to phrasing """
        # i iterates through the sentences
        for i in range(len(phrased_sentences)):
            # j iterates through the phrases in each sentence
            for j in range(len(phrased_sentences[i])):
                try:
                    # third index is the token index within each phrase
                    if phrased_sentences[i][j - 1][-1] in PAUSE_PUNCTUATION:
                        pass
                    else:
                        if self.pause_criteria_not_met(phrased_sentences[i], j):
                            pass
                        elif self.medium_pause_criteria_met(phrased_sentences[i], j):
                            phrased_sentences[i][j - 1].append(self.medium_pause)
                        elif self.long_pause_criteria_met(phrased_sentences[i], j):
                            phrased_sentences[i][j - 1].append(self.long_pause)
                        if self.long_pause_criteria_previous_phrase_met(phrased_sentences[i], j):
                            phrased_sentences[i][j - 2].append(self.long_pause)
                except:
                    # we run into out of index errors, ignore and continue
                    pass
        return phrased_sentences

    def pause_criteria_not_met(self, phrased_sentence: list, phrase_index: int) -> bool:
        return phrased_sentence[phrase_index][0].startswith((NP, AP, PP, VP, INJP, MWE, ADVP)) or (
                phrased_sentence[0] == CP and phrased_sentence[phrase_index - 2][0] in [NP_SEQUENCE, AP_SEQUENCE]) or (
                phrased_sentence[phrase_index][0] == CP and (
                phrased_sentence[phrase_index - 1][0] == PP and phrased_sentence[phrase_index + 1][0] == PP))

    def medium_pause_criteria_met(self, phrased_sentence: list, phrase_index: int) -> bool:
        if phrased_sentence[phrase_index][1] == REL and phrased_sentence[phrase_index - 1][0] == NP:
            if (phrased_sentence[phrase_index - 2][0] == PP or (
                    phrased_sentence[phrase_index - 2][0] == NP and phrased_sentence[phrase_index - 3][0] == PP)):
                return True

        if (phrased_sentence[phrase_index][0] == CP and not phrased_sentence[phrase_index - 1][-1].startswith(TF)) \
                or (phrased_sentence[phrase_index - 2][0] == PP and phrased_sentence[phrase_index - 1][0] == NP and
                 phrased_sentence[phrase_index][0] == SCP and not phrased_sentence[phrase_index][1] == REL):
            return True

        return False

    def long_pause_criteria_met(self, phrased_sentence: list, phrase_index: int) -> bool:
        return phrased_sentence[phrase_index][0] == SCP and not phrased_sentence[phrase_index][1] == REL

    def long_pause_criteria_previous_phrase_met(self, phrased_sentence: list, phrase_index: int) -> bool:
        return phrased_sentence[phrase_index][0] == CP and (
                phrased_sentence[phrase_index - 1][0] == PP and phrased_sentence[phrase_index + 1][0] == PP)

    def extract_text(self, phrased_sentence: list) -> str:
        """ Delete empty items and extract text and pause tags from phrased_sentences, leaving phrase labels and
        PoS tags behind. For this, it is sufficient to extract every other token from each phrase, beginning
        at index 1: ['NP', 'stefnanda', 'nkee', '<sil>'] -> ['stefnanda', '<sil>']"""

        clean_phrases = [list(filter(None, item)) for item in phrased_sentence]
        extracted_text_list = []

        for i in range(len(clean_phrases)):
            extracted_text_list.append([clean_phrases[i][index] for index in range(1, len(clean_phrases[i]), 2)])
        return ' '.join([item for sublist in extracted_text_list for item in sublist])

    def switch_punctuation(self, clean_list):
        """ Put pause cues instead of punctuation marks """
        clean_list2 = [re.sub('[.?!;]', self.long_pause, sent) for sent in clean_list]
        clean_list3 = [re.sub('[,–\-:/−]', self.medium_pause, sent) for sent in clean_list2]
        clean_list4 = [re.sub('[„“()"”·*]', self.short_pause, sent) for sent in clean_list3]
        return clean_list4


def main():
    with open(sys.argv[1]) as file:
        lines = [line.strip() for line in file]

    phraser = Phrasing()
    #paused_text = phraser.insert_pauses(['[NP Ekkert fohen ] [VP hefur sfg3en komið ssg ] [AdvP fram aa ] [SCP sem c ] [VP styður sfg3en ] [NP þann fakeo framburð nkeo ] [NP stefnanda nkee ] [SCP að c ] [NP hún fpven ] [VP hafi svg3en mátt ssg ] [VP gera sfg3fn ] [NP ráð nhen ] [PP fyrir aþ ] [MWE_CP því fpheþ að c ] [AdvP sjálfkrafa aa ] [VP tæki svg3eþ ] [PP við ao [NP [AP ótímabundin lvensf ] ráðning nven ] ] [PP í aþ [NP framhaldi nheþ ] ] [PP af aþ [NP þriggja tfkfe mánaða nkfe ] [NP [AP tímabundinni lveþsf ] ráðningu nveþ ] ] [CP eða c ] [AdvP að aa ] [VPs samið ssg ] [VPb hafi svg3en verið ssg ] [PP á ao [AdvP þá aa ] [NP leið nveo ] ] . . '])
    phraser.insert_pauses([])
    paused_text = phraser.insert_pauses(lines)
    for line in paused_text:
        print(line)
    #with open(sys.argv[2], 'w') as f:
    #    for item in paused_text:
    #        f.write("%s\n" % item)


if __name__ == '__main__':
    main()


