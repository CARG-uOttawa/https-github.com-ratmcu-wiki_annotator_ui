import sys
import os
import pandas as pd
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from info_box import InfoCard, PrivateEntities, PageContents
from data_loader import NerDataset, sample_data

tag_dict = {'BD':{'color':"#ff0000", 'tag': '-BD'},
            'CH':{'color':"#ff6600", 'tag': '-CH'},
            'PR':{'color':"#0066ff", 'tag': '-PR'},
            'SP':{'color':"#ff3399", 'tag': '-SP'},
            'ED':{'color':"#993399", 'tag': '-ED'},
            'BP':{'color':"#009900", 'tag': '-BP'}
            }

pii_to_tag = {'BIRTH_DATE':'BD', 
              'CHILDREN':'CH',
              'SPOUSES':'SP',
              'PARENTS':'PR',
              'BIRTH_PLACE':'BP',
              'EDICATION':'ED'}

dataset_dir = './scrapes'
text_data_dir = './test_txt'
manual_data_dir = './manual_annot_txt'
class UFunc():
    def setupDataset(self):
        self.text_data_files = sorted([os.path.join(f[0], name) for f in os.walk(text_data_dir) 
                        if len(f[2])!=0 for name in f[2] if os.path.splitext(name)[-1] == '.txt' and name.split('_')[0]=='annot'],
                    key=lambda path: int(path.split('_')[-1].split('.')[0]))
        self.file_indices = [int(path.split('_')[-1].split('.')[0]) for path in self.text_data_files]
        # self.summary_files = sorted([os.path.join(f[0], name) for f in os.walk(dataset_dir) 
        #                 if len(f[2])!=0 for name in f[2] if os.path.splitext(name)[-1] == '.csv' and name.split('_')[0]=='summary' and (int(name.split('_')[-1].split('.')[0]) in self.file_indices)],
        #             key=lambda path: int(path.split('_')[-1].split('.')[0]))
        self.summary_files = sorted([os.path.join(f[0], name) for f in os.walk(dataset_dir) 
                        if len(f[2])!=0 for name in f[2] if os.path.splitext(name)[-1] == '.csv' and name.split('_')[0]=='summary'],
                    key=lambda path: int(path.split('_')[-1].split('.')[0]))
        # load all the summary csv filenames from the dataset folder 

    def load(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile) # lock the location to the txt dataset folder
        # fname = dialog.getOpenFileName()
        self.fileName = QFileDialog.getOpenFileName(self,
            "Open annotation file", "./test_txt", "text Files (*.txt)")
        # fname = dialog.getExistingDirectory()
        print(self.fileName[0])
        # get the file name and get the index ()
        # load the file into the dataset class
        # get the url and get the info box dictionary
        self.html = "<p>"
        html = ""
        self.data_tool = NerDataset(self.fileName[0])
        self.data_index = int(self.fileName[0].split('_')[-1].split('.')[0])
        print(self.data_index)
        # print(self.summary_files[self.data_index])
        # df = pd.read_csv(self.summary_files[self.data_index])
        for sum_file in self.summary_files:
            if self.data_index == int(sum_file.split('_')[-1].split('.')[0]):
                print(sum_file)
                df = pd.read_csv(sum_file)
        # self.url = df.get_value(0, 'URL')
        self.url = df.at[0, 'URL']
        print(self.url)
        self.getPII(self.url)
        for sent in self.data_tool.sents:
            for word in sent[1:-1]: # skip the [CLS] and [SEP] tags
                html = html + word + " "
            html = html + ("<br>")
        # print(html)
        self.html =  self.html + html + "</p>"
        # print(self.html)
        self.edit.clear()
        self.edit.appendHtml(self.html)

    def save(self):
        # print(self.html)
        # transform indices to the tokens
        text = self.edit.toPlainText()    
        # print(text)
        # go back and change marking to tokens
        left = 0
        tokens = []
        for selection in self.selection_list:
            if selection[0] - left > 0:
                token_length = len(text[left:selection[0]].split())
                tokens.extend(['O']*token_length)
            token_length = len(text[selection[0]:selection[1]].split())
            left = selection[1]
            tokens.extend(['B-'+selection[2]]*1)
            if token_length-1 > 0:
                tokens.extend(['I-'+selection[2]]*(token_length-1))
        token_length = len(text[self.selection_list[-1][1]:].split())
        tokens.extend(['O']*token_length)
        token_index = 0
        name = self.fileName[0].split('/')[-1]
        name = manual_data_dir + '/' + 'manual_' + name
        print(name)
        f = open(name, "w")
        for sent in self.data_tool.sents:
            for word in sent[1:-1]: # skip the [CLS] and [SEP] tags
                print(word, tokens[token_index])
                f.write(word + ' ' + tokens[token_index])
                f.write('\n')
                token_index = token_index + 1
            print('-----------')
            f.write('\n')
        f.close()
        # print(text)
        # print(tokens)


    def clear(self):
        self.color("")
    def bd(self):
        self.color('BD')
    def ch(self):
        self.color('CH')
    def pr(self):
        self.color('PR')
    def sp(self):
        self.color('SP')
    def ed(self):
        self.color('ED')
    def bp(self):
        self.color('BP')

    def color(self, tag):
        if self.selection == [0, 0, 0]:
            return
        found = False
        clear = -1
        for i, gap in enumerate(self.selection_list):
            if gap[0] == self.selection[0] and gap[1] == self.selection[1]:
                if tag == "" :
                    self.selection_list[i][2] = tag 
                    clear = i
                    found = True
                    break
                else:
                    print('overlapping annotations, please clear the annotation and try')
                    return  

            if gap[0] <= self.selection[0] and gap[1] >= self.selection[0] or \
            gap[0] <= self.selection[1] and gap[1] >= self.selection[1] or \
            gap[0] >= self.selection[0] and gap[1] <= self.selection[1] or \
            gap[0] >= self.selection[0] and gap[1] <= self.selection[1] :
                print('overlapping annotations, please clear the annotation and try')
                return
                            
        text = self.edit.toPlainText()    
        # print(text)
        
        if not found and tag != '':
            self.selection[2] = tag
            while text[self.selection[0]] == ' ':
                if self.selection[0] + 1 != len(text):
                    self.selection[0] = self.selection[0] + 1
            self.selection_list.append(self.selection)

        self.selection = [0, 0, 0]
        
        if(len(self.selection_list)==0):
            return        
        self.selection_list.sort(key = lambda elem: elem[0])#+elem[1])
        # print(self.selection_list)
             
        self.html = "<p>"
        html2 = "<p style='line-height: 30px;'>"
        left = 0
        for i, gap in enumerate(self.selection_list):
            self.html = self.html + text[left:gap[0]]
            html2 = html2 + text[left:gap[0]]
            if gap[2] != "":
                self.html = self.html + "<font color={1}>{0}</font>".format(text[gap[0]:gap[1]], tag_dict[gap[2]]['color'])
                html2 = html2 + "<font style='color: #ffffff;background-color: {1};padding: 5px 10px;border-radius: 5px;'>{0}</font>".format(text[gap[0]:gap[1]], tag_dict[gap[2]]['color'])
            else:
                self.html = self.html + "{0}".format(text[gap[0]:gap[1]])
                html2 = html2 + "{0}".format(text[gap[0]:gap[1]])
            left = gap[1]
        self.html = self.html + "{0}</p>".format(text[self.selection_list[-1][1]:])
        html2 = html2 + "{0}</p>".format(text[self.selection_list[-1][1]:])
        if clear >= 0:
            self.selection_list.pop(clear)
        html = self.html.split("\n")
        self.html = ''
        for line in html[:-1]:
            self.html =  self.html + line + '<br>'
        self.html =  self.html + html[-1]
        print(self.html)

        html = html2.split("\n")
        html2 = ''
        for line in html[:-1]:
            html2 =  html2 + line + '<br>'
        html2 =  html2 + html[-1]
        print(html2)
        # print(self.edit.verticalScrollBar().value())
        val = self.edit.verticalScrollBar().value()
        self.edit.clear()
        # self.edit.appendHtml(self.html)
        self.edit.appendHtml(html2)
        self.edit.verticalScrollBar().setSliderPosition(val)

    def handleSelectionChanged(self):
        cursor = self.edit.textCursor()
        if cursor.selectionStart() == cursor.selectionEnd():
            return
        self.selection = [cursor.selectionStart(), cursor.selectionEnd(), 0]
        # print ("Selection start: %d end: %d" % 
        #     (cursor.selectionStart(), cursor.selectionEnd()))

    def getPII(self, url):
        pg = PageContents(url)
        info_card = InfoCard(pg)
        entities = PrivateEntities(info_card).entity_dict
        # print(info_card.info_table)
        # print(entities)    
        # get a dictionary with the needed entitites, and the list of scraped PII relavant 
        piis = {}
        pii_html = "<p>"
        for key in entities.keys():
            piis[key] = []
            if key in pii_to_tag.keys():
                clr = tag_dict[pii_to_tag[key]]['color']
                pii_html = pii_html + "<font color={1}>{0}</font>".format(key, clr) + " : "
                lis = ''
                if len(entities[key]) != 0:
                    for entry in entities[key]:
                        piis[key].extend(entry['entity_list'])
                        lis.join(entry['entity_list'])
                    if len(piis[key]) != 0:
                        for ite in piis[key][:-1]:
                            lis = lis + ite + ', '
                        lis = lis + piis[key][-1]
                # print(lis)
                pii_html = pii_html + lis + '<br>'
        pii_html = pii_html + '</p>'   
        # print(piis)
        # print(pii_html)
        self.info_box.appendHtml(pii_html)
        return piis    