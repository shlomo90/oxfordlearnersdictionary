def complete_example(example):
    example_fmt = (' - {example}')
    return example_fmt.format(example=example)


def complete_define(shcut, define):
    define_fmt = ('{shcut}\nDefine: {define}')
    return define_fmt.format(shcut=shcut, define=define)


def complete_word(name, phon, defines):
    word_fmt = (
        '----------------------------------------------\n'
        'Name           : {name}\n'
        'Phonetic(br/am): {phon}\n'
        '----------------------------------------------\n'
        '{define_fmt}'
    )
    return word_fmt.format(name=name, phon=phon, define_fmt='\n'.join(defines))


class Word:
    def __init__(self, name):
        self.name = name
        self.phon = ''
        # {definition: [example, ]}
        self.definitions = {}

    def set_phon(self, phon):
        self.phon = phon

    def set_contents(self, shcut, define, examples):
        if shcut in self.definitions:
            self.definitions[shcut][define] = []
            self.definitions[shcut][define] += examples
        else:
            self.definitions[shcut] = {}
            self.definitions[shcut][define] = []
            self.definitions[shcut][define] += examples

    def show_word(self):
        defines = []
        for key, value in self.definitions.iteritems():
            shcut = ''
            if key is not None:
                shcut = 'Short Cut: ' + key

            for define, examples in value.iteritems():
                define_msgs = complete_define(shcut, define)
                msgs = []
                for example in examples:
                    if example == 'None':
                        continue
                    msgs.append(complete_example(example))
                if not msgs:
                    continue
                example_msgs = '\n'.join(msgs)
                defines.append('\n'.join([define_msgs, example_msgs]))
                defines.append('\n')

        print(complete_word(self.name, self.phon, defines))
