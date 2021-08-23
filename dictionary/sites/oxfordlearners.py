import requests
from dictionary.sites.basic import Word


# Surpress warnings from BeautifulSoup.
with open("/dev/null", "w") as f:
    import sys
    saved = sys.stderr
    sys.stderr = f
    from BeautifulSoup import BeautifulSoup
    sys.stderr = saved


WORD_URL = (
    'https://www.oxfordlearnersdictionaries.com/'
    'definition/english/{}'
)


class Oxfordlearners():
    def __init__(self):
        pass

    def find_top_container(self, tc):
        top_container = {}

        top_g = tc.find('div')
        if top_g is None:
            return

        webtop = top_g.find('div')
        if webtop is None:
            return

        # Name
        name_h1 = top_g.find('h1')
        if name_h1 is None:
            return
        top_container['name'] = str(name_h1.text)

        # Pos (Type : Noun, adv, ...)
        pos_span = top_g.find('span', {'class': 'pos'})
        if pos_span is None:
            return
        top_container['pos'] = str(pos_span.text)

        # Phonetics Britain
        phon_span = top_g.find('span', {'class': 'phonetics'})
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

    def extract_content_from_sense(sense):
        sense_li_classes = sense.findChildren(
            'li', {'class': 'sense'}, recursive=False)

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

    def find_def_and_examples(self, li, content=None):
        if content is None:
            content = {}

        defs = li.find('span', {'class': 'def'})
        if defs is None:
            return content
        # define may have tags
        
        content['def'] = str(defs.text.encode('utf-8'))
        
        examples = li.find('ul', {'class': 'examples'})
        if examples is None:
            return content
        example_lis = examples.findAll('li')
        content['example'] = []
        for example_li in example_lis:
            example = example_li.find('span', {'class': 'x'})
            if example is None:
                continue
            # TODO: some words are bold <span class="cl">...</span>
            content['example'].append(str(example.string))
        return content

    def find_sense_single(self, sense):
        contents = []
        sense_li_classes = sense.findChildren(
                'li', {'class': 'sense'}, recursive=False)
        for sense_li_class in sense_li_classes:
            contents.append(self.find_def_and_examples(sense_li_class))
        return contents


    def find_senses_multiple(self, sense):
        def __get_li_id(shcut_h2):
            li_id = None
            for attr in shcut_h2.attrs:
                # attr is tuple like (key,value)
                # key is like id, class, ...
                if attr[0] == 'id':
                    # li's id = {wordname}_sng_{id}
                    # shcut's id = {wordname}_shcut_{id}
                    # We can get the il's id from shcut's id
                    # replacing shcut to sng
                    elems = attr[1].split('_')
                    li_id = elems[0] + '_sng_' + elems[-1]
                    break
            return li_id

        # There are two types below
        # [ {'shcut_h2': " ", 'def': ' ', 'examples': ['','','']}, {} ]
        contents = []
        shcut_g_spans = sense.findAll('span', {'class': 'shcut-g'})
        # The case of there is no shcut_h2
        if len(shcut_g_spans) == 0:
            contents = self.find_sense_single(sense)
        # The case of ther is shcut_h2
        else:
            for shcut_g_span in shcut_g_spans:
                content = {}

                if shcut_g_span is None:
                    continue

                shcut_h2 = shcut_g_span.findChildren(
                        'h2', {'class': 'shcut'}, recursive=False)
                if not shcut_h2:
                    continue
                # Only one.
                shcut_h2 = shcut_h2[0]

                li_id = __get_li_id(shcut_h2)
                if li_id is None:
                    continue

                content['shcut'] = str(shcut_h2.string)
                # TODO: Duplicated
                sense_li_classes = sense.findChildren(
                        'li', {'class': 'sense', 'id': li_id}, recursive=False)
                # One time
                for sense_li_class in sense_li_classes:
                    contents.append(self.find_def_and_examples(
                        sense_li_class, content))
        return contents

    def send_request(self, word):
        url = WORD_URL.format(word)
        user_agent = {
            'User-Agent': (
                'Mozilla/5.0 '
                '(Macintosh; Intel Mac OS X 10_12_1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/55.0.2883.75 Safari/537.36'
            )
        }

        req = requests.get(url, headers=user_agent)
        if req.status_code == 200:
            return req.content
        else:
            return None

    def find_word(self, word):
        content = self.send_request(word)
        if content is None:
            return None

        bs = BeautifulSoup(content)
        entry_div = bs.find('div', {'class': 'entry'})
        if entry_div is None:
            return None

        # top_containers Get(name, type, phon)
        top_containers = entry_div.find('div', {'class': 'top-container'})
        for tc in top_containers:
            if tc is None:
                continue
            top_container = self.find_top_container(tc)
            if top_container is None:
                continue
            break

        single = entry_div.findChildren(
            'ol', {'class': 'sense_single'}, recursive=False)
        multi = entry_div.findChildren(
            'ol', {'class': 'senses_multiple'}, recursive=False)
        if single:
            contents = self.find_sense_single(single[0])
        elif multi:
            contents = self.find_senses_multiple(multi[0])

        word_inst = Word(word)
        word_inst.set_phon(
            top_container['phon_br'] + ' ' + top_container['phon_n_am'])
        for content in contents:
            if 'def' in content and 'example' in content:
                if 'shcut' in content:
                    word_inst.set_contents(
                        content['shcut'], content['def'],
                        content['example'])
                else:
                    word_inst.set_contents(
                        None, content['def'],
                        content['example'])
        return word_inst
