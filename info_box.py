from ahocorasick import Automaton
import fuzzyset
import urllib
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import nltk
import re
import pandas as pd
import numpy as np
nltk.download('punkt')
# !python3 -m spacy download en_core_web_sm
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import spacy
import regex
class PageContents():
  def __init__(self, url):
      self.quote_page = url
      try:
        self.page = urllib.request.urlopen(self.quote_page,  timeout = 5)
        self.soup = BeautifulSoup(self.page, 'html.parser')
      except:
        self.table = False
      
#       side_pane = self.soup.find('tbody')#.find_all('tr')
      try:
        self.side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'}) # or infobox biography vcard
        if not self.side_pane:
            self.side_pane = self.soup.find('table', attrs={'class': 'infobox biography vcard'})
        self.table_entry_list = self.side_pane.find('tbody').find_all('tr')
        self.table = True
      except:
        self.table = False
#       print(self.table_entry_list)
#       self.table_entry_list = self.soup.find('tbody').find_all('tr')
   
  def get_party(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      party = ''
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
              if child.text == 'Political party':
                  party = child.next_sibling.contents[0].get('title')
#                   print(party)
             
  def get_name(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      names = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
#               print(child)
              try:
                if child.text == 'Born':
                    div_list = child.next_sibling.find_all('div')
                    for i, item in enumerate(div_list):
#                       try:
                      t = item['class']
#                       print(t)
                      if t[0] == 'nickname':
#                         print(item.text)
                        names.append(item.text)
#                       except:
#                         pass
                    break
              except:
                pass  
      if len(names) != 0:
        return names
      else:
#         print('no name found')
#         print(self.soup.find('div', attrs={'class': 'fn'}).text)
        try:
          names.append(self.soup.find('div', attrs={'class': 'fn'}).text)
#         div_list = self.soup.find('tbody').find_all('div')
#         for i, item in enumerate(div_list):
#           try:
#             t = item['class']
# #             print(t)
#             if t[0] == 'fn':
# #               print(item.contents[0])
#               names.append(item.contents[0])
        except:
          pass
      return names
  def get_birth_date(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      date = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
            try:
              if child.text == 'Born':
                  for i, item in enumerate(child.next_sibling.contents):
#                     try:
                    t = item.span['class']
#                       print(t)
                    if t[0] == 'bday':
#                         print(child.next_sibling.contents[i+1])
                      date.append(child.next_sibling.contents[i+1])
#                     except:
#                       pass
                  break
            except:
              pass
      return date  
    
  def get_birth_place(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
              try:
                  if child.text == 'Born':
    #                   print(child.next_sibling.contents)
    #                 sibling = find all 
    #                 for content in child.next_sibling.contents:
    #                   if 
    #                   try:
                      party.append(child.next_sibling.contents[-1].text)
                      break
    #                   except:
    #                     pass
              except:
                  pass
      return party
    
  def get_children(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
#               print(child.text)
              try:
                  if child.text == 'Children':
                      children = child.next_sibling.find_all('a')
    #                   print([child for child in children])
    #                   print(child.next_sibling.contents[0].text)
    #                   print(child.next_sibling.contents)
    #                   sen = re.sub('[[0-9]*]', '', sentence) #remove the reference brackets
                      party.extend([re.sub('[[0-9]*]', '', child.text) for child in children])
              except:
                  pass
      if party != ['']:
#         print(party)
        return party
      else:
        return self.get_children_alternate()
      
  def get_children_alternate(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
#               print(child.text)
              if child.text == 'Children':
#                   children = child.next_sibling.find_all('a')   
#                   print('-----')
#                   print(child.next_sibling.contents)
                  for kid in child.next_sibling.contents:
#                     print(type(kid))
#                     print('---+++_++_+++')
                    try:
                      a = BeautifulSoup(kid, "html.parser").find_all('a')
#                       print('printing a s')
#                       print(a)
                      if not bool(a):
#                         print(kid)
                        party.append(kid)
#                       else:
#                         print('html kid!')
#                         party.append(re.sub('[[0-9]*]', '', kid.text))
                    except:
#                       print(kid.text)
#                       party.append(re.sub('[[0-9]*]', '', kid.text))
                        pass
      return party
    
  def get_spouses(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_self.all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
              try:
                text = child.text
              except:
                continue
              if text == 'Spouse(s)':
                try:
#                   children = child.next_sibling.contents[0].find_all('a')
                  children = child.next_sibling.find_all('a')
#                   print([child.text for child in children])
                  if len(children) == 0:
#                     print(child.next_sibling.text)
                    party.extend([child.next_sibling.text])
                  else:
                    party.extend([child.text for child in children])
                except:
#                   print(child.next_sibling.contents)
                  return child.next_sibling.contents
                  pass
                break
      return party
  
  def get_parents(self):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       side_pane = self.soup.find('tbody')#.find_all('tr')
#       table_entry_list = side_pane.find_all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
              try:
                text = child.text
              except:
                continue
              if text == 'Parents':
                  children = child.next_sibling.find_all('a')
#                   print([child.text for child in children])
                  party.extend([child.text for child in children])
      return party
  
  def get_any(self, field):
#       side_pane = self.soup.find('table', attrs={'class': 'infobox vcard'})
#       table_entry_list = side_pane.find_all('tr')
      party = []
      for table_entry in self.table_entry_list:
          for child in table_entry.children:
              if child.text == field:
                  party.append(child.next_sibling.contents[0].text)
      return party

  def get_text(self):
    '''TODO: filter out the table entries and stuff that are coming under paragraph tags as text'''

#     nltk.download('punkt')
    if not self.table:
      return []
    paragraphs = self.soup.find_all('p')
    paragraphs_list = []
    for par in paragraphs:
      paragraphs_list.append(sent_tokenize(par.text))
    #   len(sent_tokenize_list)
    # paragraphs_list

    text = []
    for paragraph in paragraphs_list: 
      for sentence in paragraph:
        sen = re.sub('[[0-9]*]', '', sentence) #remove the reference brackets
        sen = re.sub('\xa0', ' ', sen) #remove the reference brackets
        text.append(sen)
    #     print(sen)  
    return text

  def get_text_chunk(self):
    '''TODO: filter out the table entries that are coming under paragraph tags'''
#     nltk.download('punkt')
    if not self.table:
      return []
    paragraphs = self.soup.find_all('p')
    paragraphs_list = []
    for par in paragraphs:
      paragraphs_list.append(sent_tokenize(par.text))
    #   len(sent_tokenize_list)
    # paragraphs_list

    text = ''
    for paragraph in paragraphs_list: 
      for sentence in paragraph:
        sen = re.sub('[[0-9]*]', '', sentence) #remove the reference brackets
        text = text + ' ' + sen
    #     print(sen)  
    return text

  def get_info_dict(self):
    info_dict = {}
    if not self.table:
      info_dict['NAME'] = ['']
      info_dict['BIRTH_DATE'] = ['']
      info_dict['BIRTH_PLACE'] = ['']
      info_dict['CHILDREN'] = ['']
      info_dict['SPOUSES'] = ['']
      info_dict['PARENTS'] = ['']
      return info_dict
    
    info_dict['NAME'] = self.get_name()
    info_dict['BIRTH_DATE'] = self.get_birth_date()
    info_dict['BIRTH_PLACE'] = self.get_birth_place()
    info_dict['CHILDREN'] = self.get_children()
    info_dict['SPOUSES'] = self.get_spouses()
    info_dict['PARENTS'] = self.get_parents()
    return info_dict
  
  def get_contents(self):
    return self.get_info_dict(), self.get_text()
  
def aggregate_parts_and_annotate(annotated_list, txt, words_within = 2):
  annot_list = []
#   print(len(annotated_list))
  if len(annotated_list) > 1:
    matched = set([ annotated_list[i][3][1][1] for i in range(1,len(annotated_list)-1)])
    sub_sentence = txt[annotated_list[0][0]][annotated_list[0][3][0]+1:annotated_list[-1][3][0]-len(annotated_list[-1][3][1][1])]
    enclosed = set(sub_sentence.split()) # could there be an elegant way to do this?? 
    difference = enclosed.difference(matched)
    if len(difference)>words_within:
#       pass
      for annot in annotated_list:
        annot_list.append((annotated_list[0][0],(annot[3][0]-len(annot[3][1][1])+1, annot[3][0]+1), annot[4])) # [sentence number, (start char, end char), annotation type]
    else:
        annot_list.append((annotated_list[0][0],(annotated_list[0][3][0]-len(annotated_list[0][3][1][1])+1,annotated_list[-1][3][0]+1),annotated_list[0][4]))
#     print(enclosed.difference(matched)) 
#     print(sub_sentence.split())
  elif len(annotated_list) == 1:
    annot_list.append((annotated_list[0][0],(annotated_list[0][3][0]-len(annotated_list[0][3][1][1])+1, annotated_list[0][3][0]+1), annotated_list[0][4])) # [sentnce number, (start char, end char), anootation type]
  else:
    return []
    #   print(annot_list)
  return annot_list

def annotate_text(info_dict, txt):
  annotations = []
  keys = list(info_dict.keys())
  for key in keys: # for every entry in the info dictionary 
    annotate_list = []
    for i, sentence in enumerate(txt): # get a sentence from the text
        fz = fuzzyset.FuzzySet(use_levenshtein=False)
        for word in sentence.split(): # add all the words into a fuzzy set from that sentence
            fz.add(word)        
    #     A=Automaton()
        for j, detail in enumerate(info_dict[key]): # get a detail in the list under an info line
          annotate_sub = []
          matched_list = []
          A = Automaton()
          tokens_in_detail = len(detail.split()) # split the detail into words
          for word in detail.split(): # get a word from the detail
    #         print(word)
            result = fz.get(word)    # get the matching 
            if(result and result[0][0]>=0.5 and not len(result[0][1])/2 < len(word)/2): #if the matching confidence is high and word length is high
              matched_list.append((word, result))
  #             print(result[0][1], word)
  #         if len(matched_list) == tokens_in_detail:
          if abs(len(matched_list) - tokens_in_detail) < 1 and len(matched_list)!=0:
            for matches in matched_list:
                for match in matches[1]:
                    A.add_word(match[1], (matches[0], match[1]))
  #                   print(match[1], '--->', match)
            A.make_automaton()
    #         print(sentence)
            for item in A.iter(sentence):
                # print(item, item[0]+1- len(item[1][1]), item[0] , sentence)
                # print(item, item[0]+1- len(item[1][1]), item[0])
                annotate_sub.append([i, j, detail, item, key])
            if len(annotate_sub) != 0:
              annotate_list.append(annotate_sub)    
#     annotation_minimized = []
    for list_sub in annotate_list:
      if list_sub[0][2].split()[0] != list_sub[0][3][1][0]:
        list_sub.pop(0)
#       annotation_minimized.extend(aggregate_parts_and_annotate(list_sub,txt))
      annotations.extend(aggregate_parts_and_annotate(list_sub, txt))

#   for list_sub in annotations: #uncomment to print the annotation list!
#     print(list_sub, txt[list_sub[0]], '\'', txt[list_sub[0]][list_sub[1][0]:list_sub[1][1]], '\'')
  return annotations

def takeSentenceNumber(annot):
  return annot[0]

class InfoCard():
    '''accepts a beautiful soup html table from a wikipedia page and scrapes the table to a dictionary'''
    def __init__(self, page_content):
        self.info_table = {}
        if not page_content.table:
            raise Exception('page content is incomplete')
        for table_entry in page_content.table_entry_list:
            try:
                left_col = table_entry.find('th', attrs={'scope': 'row'})
                right_col = left_col.next_sibling
                self.info_table[self._row_filter(left_col.text)] = self._get_text_parts(self._get_kids(right_col))
            except:
                pass
        self.info_table_unfiltered = self.info_table
        self.info_table = self._filter_info_scrapes(self.info_table)
        print('info card is scraped successfully')
        logging.debug(self.info_table)
    
    def _row_filter(self, text):
        return re.sub('\xa0', ' ', text)
        
        
    def _get_kids(self, html_mother):
        kid_list = []
        try:
            kids = html_mother.children
            for kid in kids:
                kid_list.append(self._get_kids(kid))
        except:
            return html_mother
        return kid_list 

    def _get_text_parts(self, text_lists):
        text_parts = []
        if type(text_lists) == list:
            for element in text_lists:
                text_parts.extend(self._get_text_parts(element))
        else:
            text_parts.append(text_lists)
        return(text_parts)

    def _filter_info_scrapes(self, scape_dict):
        mask_dict = {}
        for key, val in scape_dict.items():
            mask_dict[key] = []
            for i, element in enumerate(scape_dict[key]):
                name = ''
                lst = [' '+nm[0] for nm in [part.split('(') for part in element.split(' ')] if nm[0]!='']
                element = ''.join(lst).strip()
                fnd = [c in element for c in u'[]\n\xa0']
                if not True in fnd:
                    mask_dict[key].append(element)  
        return mask_dict    

# can we use snorkle to get this entity scraping done??? 
# if so it'd be better to have the lable functions in a ready way to generally working on all the pages!!

class PrivateEntities():
    '''given a dictionary of a side bar it is processed for private entities of interest'''
    def __init__(self, info_card):
        self.info_dict = info_card.info_table
        # print(info_card.info_table)
        self._get_entity_dict()
        self._extract_entities()
        
    def _extract_entities(self):
        # TREAT everyone the same? or call a seperate function per each entity?
        # leave the not found entities as empty lists so we can use the html scraper to fill them (usually the name of the person)
        # lets treat everything generally, ultimate filtering happens at the comparison stage(if theres one)
        for entity_key in self.entity_dict.keys():
#             print(entity_key, self.entity_dict[entity_key])
            if self.entity_dict[entity_key] == []:
                continue
            for tiny_dict in self.entity_dict[entity_key]:
                self._pick_entity(tiny_dict, entity_key)
            logging.debug(self.entity_dict[entity_key])
    
    def _pick_entity(self, entity_list, entity_key):
        nlp = spacy.load("en_core_web_sm")
#         print(entity_list)
#         Find named entities, phrases and concepts
#         entity_list.append([])
#         print(entity_list[0][0])
        #TODO: add a check for the NAME too
        if entity_key == 'BIRTH_PLACE':
            mask_str = ''
            for scrape in self.info_dict[entity_list['dict_key']]:
                doc = nlp(str(scrape))
                if doc.ents and doc.ents[0].label_ == 'DATE':
                    mask_str = mask_str + 'd'
                elif str(scrape) == '' or str(scrape) == ',':
                    mask_str = mask_str + 's'
                elif self._is_name(str(scrape)):
                    mask_str = mask_str + 't'
                else:
#                     print(scrape)
                    mask_str = mask_str + 'u'
#             print(mask_str)
            indices = self._get_target_indices([r'[s][t]',r'[d][t]'], mask_str)  
            for index in indices:
                entity_list['entity_list'].append(self.info_dict[entity_list['dict_key']][index])
        else:    
            for scrape in self.info_dict[entity_list['dict_key']]:
                if entity_list['type'] == 'PERSON': #spacy skips certain parts of a name, so we use this trick instead
                    doc = nlp('was named '+str(scrape))
                    logging.debug(scrape)
                else:
                    doc = nlp(str(scrape))
                if doc.ents and doc.ents[0].label_ == entity_list['type']:   
                    entity_list['entity_list'].append(doc.ents[0].text)
                    logging.debug('appended entity: ', doc.ents[0].text, doc.ents[0].label_, len(doc.ents), doc.ents)
                elif not self._entity_noise(entity_key, str(scrape)):
                    entity_list['entity_list'].append(str(scrape))
                else:
                    pass
                
    def _get_target_indices(self, pattern_list, mask_str):
        '''TODO: if the target is inside the pattern'''
        indices = []
        for pattern in pattern_list:
            m_iter = re.finditer(pattern, mask_str)
            if m_iter:
                for m in m_iter: 
                    indices.append(m.start()+1)
        return indices        
        
    def _entity_noise(self, entity_key, text):
        try:
            return getattr(self, '_filter_{0}'.format(entity_key))(text)
        except:
            logging.error('filter function for {0} not found'.format(entity_key))
            return True
    
    def _get_entity_dict(self):
        self.entity_dict = {}
        self.entity_dict['NAME'] = []
        self.entity_dict['BIRTH_DATE'] = []
        self.entity_dict['BIRTH_PLACE'] = []
        self.entity_dict['CHILDREN'] = []
        self.entity_dict['SPOUSES'] = []
        self.entity_dict['PARENTS'] = []
        self.entity_dict['EDUCATION'] = []
        if 'Born' in self.info_dict.keys():
            self.entity_dict['NAME'] += [{'dict_key':'Born', 'type':'PERSON', 'entity_list':[]}]
            self.entity_dict['BIRTH_DATE'] += [{'dict_key':'Born', 'type':'DATE', 'entity_list':[]}]
            self.entity_dict['BIRTH_PLACE'] += [{'dict_key':'Born', 'type':'GPE', 'entity_list':[]}]
        if 'Born:' in self.info_dict.keys():
            self.entity_dict['NAME'] += [{'dict_key':'Born:', 'type':'PERSON', 'entity_list':[]}]
            self.entity_dict['BIRTH_DATE'] += [{'dict_key':'Born:', 'type':'DATE', 'entity_list':[]}]
            self.entity_dict['BIRTH_PLACE'] += [{'dict_key':'Born:', 'type':'GPE', 'entity_list':[]}]
        
        if 'Birth name' in self.info_dict.keys():
            self.entity_dict['NAME'] += [{'dict_key':'Birth name', 'type':'PERSON', 'entity_list':[]}]
        
        if 'Date of birth' in self.info_dict.keys():
            self.entity_dict['BIRTH_DATE'] += [{'dict_key':'Date of birth', 'type':'DATE', 'entity_list':[]}] 
        
        if 'Place of birth' in self.info_dict.keys():
            self.entity_dict['BIRTH_PLACE'] += [{'dict_key':'Place of birth', 'type':'GPE', 'entity_list':[]}] 
        
        if 'Children' in self.info_dict.keys():
            self.entity_dict['CHILDREN'] += [{'dict_key':'Children', 'type':'PERSON', 'entity_list':[]}]
            
        if 'Spouse(s)' in self.info_dict.keys():
            self.entity_dict['SPOUSES'] += [{'dict_key':'Spouse(s)', 'type':'PERSON', 'entity_list':[]}]
        if 'Spouses' in self.info_dict.keys():
            self.entity_dict['SPOUSES'] += [{'dict_key':'Spouses', 'type':'PERSON', 'entity_list':[]}]
        if 'Spouse' in self.info_dict.keys():
            self.entity_dict['SPOUSES'] += [{'dict_key':'Spouse', 'type':'PERSON', 'entity_list':[]}]
            
        if 'Parents' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Parents', 'type':'PERSON', 'entity_list':[]}]
        if 'Parent' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Parent', 'type':'PERSON', 'entity_list':[]}]
        if 'Parent(s)' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Parent(s)', 'type':'PERSON', 'entity_list':[]}]
        if 'Father' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Father', 'type':'PERSON', 'entity_list':[]}]
        if 'Mother' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Mother', 'type':'PERSON', 'entity_list':[]}]
        if 'Father’s name' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Father’s name', 'type':'PERSON', 'entity_list':[]}]
        if 'Mother’s name' in self.info_dict.keys():
            self.entity_dict['PARENTS'] += [{'dict_key':'Mother’s name', 'type':'PERSON', 'entity_list':[]}]
            
        if 'Education' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Education', 'type':'ORG', 'entity_list':[]}]
        if 'Alma mater' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Alma mater', 'type':'ORG', 'entity_list':[]}]
        if 'Alma\xa0mater' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Alma\xa0mater', 'type':'ORG', 'entity_list':[]}]
        if 'Almat mater' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Almat mater', 'type':'ORG', 'entity_list':[]}]
        if 'Law School' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Law School', 'type':'ORG', 'entity_list':[]}]
        if 'School' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'School', 'type':'ORG', 'entity_list':[]}]
        if 'Schools' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Schools', 'type':'ORG', 'entity_list':[]}]
        if 'High school' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'High school', 'type':'ORG', 'entity_list':[]}]
        if 'High school:' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'High school:', 'type':'ORG', 'entity_list':[]}]
        if 'College' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'College', 'type':'ORG', 'entity_list':[]}]
        if 'Colleges' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'Colleges', 'type':'ORG', 'entity_list':[]}]
        if 'College(s)' in self.info_dict.keys():
            self.entity_dict['EDUCATION'] += [{'dict_key':'College(s)', 'type':'ORG', 'entity_list':[]}]
            
    def _get_sub_entity_dict(self, entity, dict_key):
        key_association_dict = {'NAME':{'Birth name', 'Born', 'Born:','Name','Name(s)','Full name'},
                                'BIRTH_PLACE':{'Born', 'Born:' ,'Home town'},
                                'BIRTH_DATE':{'Born', 'Born:'},
                                'CHILDREN':{'Children'},
                                'SPOUSES':{'Spouse','Spouse(s)','Spouses'},
                                'PARENTS':{'Parent','Parent(s)','Parents','Father','Father’s name','Mother','Mother’s name'},
                                'EDUCATION':{'Education','High school','High school:','Law School','School','Schools',
                                             'College','College(s)','Colleges','Alma mater','Almat mater','Alma\xa0mater'}}
        
    def _filter_NAME(self, text):
        '''cannot simply filter noise due to many possible candidates'''
        return True
    def _filter_BIRTH_DATE(self, text):
        return True
    def _filter_BIRTH_PLACE(self, text):
        return True
    def _filter_CHILDREN(self, text):
#         return False # let's assume we don't find any noisy text under info boxes children till we do an analysis
        return not self._is_name(text)
    def _filter_SPOUSES(self, text):
        return not self._is_name(text)
    def _filter_PARENTS(self, text):
        return not self._is_name(text)
    def _filter_EDUCATION(self, text):
        return True
    def _is_name(self, text):
        p = regex.compile(r"\p{Lu}") # To support (currently) 1702 uppercase letters
#         p = regex.compile(r"[[:upper:]]") # To support (currently) 1822 uppercase letters
        if p.match(text):
            return True
        else:
            return False