import requests, re
from BeautifulSoup import BeautifulSoup


class BasicDictionary(object):
    class Word:
        DEFINE_FMT = ('{define}\n'
                      '  - {example}')
        WORD_FMT = ('{name} ({phon})\n'
                    '{define_fmt}')

        def __init__(self, name):
            self.name = name
            self.phon = ''
            # {definition: [example, ]}
            self.definitions = {}

        def set_phon(self, phon):
            self.phon = phon

        def set_define_example(self, define, examples):
            self.definitions[define] = []
            self.definitions[define] += examples

        def show_word(self):
            defines = []
            for define, example in self.definitions.iteritems():
                define = self.DEFINE_FMT.format(define=define, example=example)
                defines.append(define)

            msg = self.WORD_FMT.format(name=self.name, phon=self.phon, define_fmt='\n'.join(defines))
            print msg
            return msg



class Oxfordlearners(BasicDictionary):
    WORD_URL = ('https://www.oxfordlearnersdictionaries.com/'
                'definition/english/{}')

    def __init__(self):
        pass

    def find_top_container(self, tc):
        top_container = {}
        #           top-g       webtop
        webtop = tc.find('div').find('div')
        if webtop is None:
            return

        # Name
        name_h1 = webtop.find('h1')
        if name_h1 is None:
            return
        top_container['name'] = str(name_h1.text)

        # Pos (Type : Noun, adv, ...)
        pos_span = webtop.find('span', {'class': 'pos'})
        if pos_span is None:
            return
        top_container['pos'] = str(pos_span.text)

        # Phonetics Britain
        phon_span = webtop.find('span', {'class': 'phonetics'})
        if phon_span is None:
            return
        phon_br_cls = phon_span.find('div', {'class': 'phons_br'})
        if phon_br_cls is None:
            return
        phon_br = phon_br_cls.find('span', {'class': 'phon'})
        if phon_br is None:
            return
        top_container['phon_br'] = str(phon_br.string)

        # Phonetics North America
        phon_n_am_cls = phon_span.find('div', {'class': 'phons_n_am'})
        if phon_n_am_cls is None:
            return
        phon_n_am = phon_n_am_cls.find('span', {'class': 'phon'})
        if phon_n_am is None:
            return
        top_container['phon_n_am'] = str(phon_n_am.string)
        return top_container

    def find_sense_single(self, sense):
        contents = []

        sense_li_classes = sense.findChildren('li', {'class': 'sense'}, recursive=False)
        for sense_li_class in sense_li_classes:
            content = {}
            defs = sense_li_class.find('span', {'class': 'def'})
            if defs is None:
                continue
            content['def'] = str(defs.string)
            
            examples = sense_li_class.find('ul', {'class': 'examples'})
            if examples is None:
                continue
            example_lis = examples.findAll('li')
            content['example'] = []
            for example_li in example_lis:
                example = example_li.find('span', {'class': 'x'})
                if example is None:
                    continue
                # TODO: some words are bold <span class="cl">...</span>
                content['example'].append(str(example.string))
            contents.append(content)
        return contents


    def find_senses_multiple(self, sense):
        # There are two types below
        # [ {'shcut_h2': " ", 'def': ' ', 'examples': ['','','']}, {} ]
        contents = []

        shcut_g_spans = sense.findAll('span', {'class': 'shcut-g'})
        # The case of there is no shcut_h2
        if len(shcut_g_spans) == 0:
            sense_li_classes = sense.findChildren('li', {'class': 'sense'}, recursive=False)

            for sense_li_class in sense_li_classes:
                content = {}
                defs = sense_li_class.find('span', {'class': 'def'})
                if defs is None:
                    continue
                content['def'] = str(defs.string)
                
                examples = sense_li_class.find('ul', {'class': 'examples'})
                if examples is None:
                    continue
                example_lis = examples.findAll('li')
                content['example'] = []
                for example_li in example_lis:
                    example = example_li.find('span', {'class': 'x'})
                    if example is None:
                        continue
                    # TODO: some words are bold <span class="cl">...</span>
                    content['example'].append(str(example.string))
                contents.append(content)
            return contents
        # The case of ther is shcut_h2
        else:
            for shcut_g_span in shcut_g_spans:
                content = {}
                if shcut_g_span is None:
                    continue
                shcut_h2 = shcut_g_span.findChildren('h2', {'class': 'shcut'}, recursive=False)
                if not shcut_h2:
                    continue

                # li's id = {wordname}_sng_{id}
                # shcut's id = {wordname}_shcut_{id}
                # We can get the il's id from shcut's id replacing shcut to sng
                li_id = None
                for attr in shcut_h2[0].attrs:
                    if attr[0] == 'id':
                        elems = attr[1].split('_')
                        li_id = elems[0] + '_sng_' + elems[-1]
                        break
                if li_id is None:
                    continue
                content['shcut'] = str(shcut_h2[0].string)
                # TODO: Duplicated
                sense_li_classes = sense.findChildren('li', {'class': 'sense', 'id': li_id}, recursive=False)
                # One time
                for sense_li_class in sense_li_classes:
                    defs = sense_li_class.find('span', {'class': 'def'})
                    if defs is None:
                        continue
                    content['def'] = str(defs.string)
                    
                    examples = sense_li_class.find('ul', {'class': 'examples'})
                    if examples is None:
                        continue
                    example_lis = examples.findAll('li')
                    content['example'] = []
                    for example_li in example_lis:
                        example = example_li.find('span', {'class': 'x'})
                        if example is None:
                            continue
                        # TODO: some words are bold <span class="cl">...</span>
                        content['example'].append(str(example.string))
                    contents.append(content)
        return contents

    def find_word(self, word):
        url = self.WORD_URL.format(word)
        req = requests.get(url)
        bs = BeautifulSoup(req.content)
        entry_div = bs.find('div', {'class': 'entry'})
        if entry_div is None:
            return None

        # top_containers Get(name, type, phon)
        top_containers = entry_div.findAll('div', {'class': 'top-container'})
        for tc in top_containers:
            top_container = self.find_top_container(tc)
            if top_container is None:
                continue
            break

        # ol class="sense_single"
        # ol class="senses_multiple"
        single = entry_div.findChildren('ol', {'class': 'sense_single'}, recursive=False)
        multi = entry_div.findChildren('ol', {'class': 'senses_multiple'}, recursive=False)
        if single:
            contents = self.find_sense_single(single[0])
        elif multi:
            contents = self.find_senses_multiple(multi[0])

        word_inst = super(Oxfordlearners, self).Word(word)
        word_inst.set_phon(top_container['phon_br'] + ' ' + top_container['phon_n_am'])
        for content in contents:
            word_inst.set_define_example(content['def'], content['example'])
        word_inst.show_word()
        return word_inst
