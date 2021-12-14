import re
import sys

""" Put the parsed format into a readable list format"""
def manipulate_text(line):
    line1 = line.split("[")
    line2 = [re.sub("\]", "", item).rstrip(" ") for item in line1]
    line3 = [item.split(" ") for item in line2]
    line4 = [list(filter(None, item)) for item in line3]
    return line4


""" Insert pauses accordingly to phrasing"""
def pause_text(manipulated_list):

    for i in range(len(manipulated_list)):
        for j in range(len(manipulated_list[i])):
            try:
                if manipulated_list[i][j-1][-1] in [',', '.', '!', '?']:
                    pass
                else:
                    if manipulated_list[i][j][0].startswith(('NP', 'AP', 'PP', 'VP', 'InjP', 'MWE', 'AdvP')) or (manipulated_list[i][0] == 'CP' and manipulated_list[i][j-2][0] in ['NPs', 'APs']) or (manipulated_list[i][j][0] == 'CP' and (manipulated_list[i][j-1][0] == 'PP' and manipulated_list[i][j+1][0] == 'PP')):
                        pass
                    elif (manipulated_list[i][j][1] == 'sem' and manipulated_list[i][j-1][0] == 'NP'):
                        if (manipulated_list[i][j-2][0] == 'PP' or (manipulated_list[i][j-2][0] == 'NP' and manipulated_list[i][j-3][0] == 'PP')):
                            manipulated_list[i][j-1].append('<pau>')
                    elif (manipulated_list[i][j][0] == 'CP') or (manipulated_list[i][j-2][0] == 'PP' and manipulated_list[i][j-1][0] == 'NP' and manipulated_list[i][j][0] == 'SCP' and not manipulated_list[i][j][1] == 'sem'):# and manipulated_list[i-2][0] not in ['NPs', 'APs']:
                        manipulated_list[i][j-1].append('<pau>')
                    elif (manipulated_list[i][j][0] == 'SCP' and not manipulated_list[i][j][1] == 'sem'):
                        manipulated_list[i][j-1].append('<sil>')
                    if manipulated_list[i][j][0] == 'CP' and (manipulated_list[i][j-1][0] == 'PP' and manipulated_list[i][j+1][0] == 'PP'):
                        manipulated_list[i][j-2].append('<sil>')
            except:
                pass
    return manipulated_list

""" Delete empty items and extract text """
def extract_text(line):
    line2 = [list(filter(None, item)) for item in line]
    line3 = []
    
    for i in range(len(line2)):
        line3.append([line2[i][index] for index in range(1, len(line2[i]), 2)])
    line4 = " ".join([item for sublist in line3 for item in sublist])
    
    return line4



long_pause = '<sil>'
medium_pause = '<pau>'
short_pause = '<sp>'

""" Put pause cues instead of punctuation marks """
def switch_punctuation(clean_list):
    clean_list2 = [re.sub('[\.\?\!\;]', long_pause, sent) for sent in clean_list]
    clean_list3 = [re.sub('[,\–\-\:\/\−]', medium_pause, sent) for sent in clean_list2]
    clean_list4 = [re.sub('[\„\“\(\)\"\”\·\*]', short_pause, sent) for sent in clean_list3]
    return clean_list4
    
    

with open(sys.argv[1]) as file:
    lines = [line.strip() for line in file]

manipulated_text = [manipulate_text(x) for x in lines]
paused_text = pause_text(manipulated_text)
extracted_text = [extract_text(x) for x in paused_text]
punctuated_text = switch_punctuation(extracted_text)

with open(sys.argv[2], 'w') as f:
    for item in punctuated_text:
        f.write("%s\n" % item)

