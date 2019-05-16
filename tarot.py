from collections import defaultdict
import csv
import os
import random

from flask import url_for
       

class Question:

    def __init__(self, options, attr, size=4):
        ''' options is list of question/answer pairs '''
        sample = None
        if type(options) == dict:
            sample = random.sample(options.keys(), size)
        else:
            sample = random.sample(range(0, len(options)), size)
        self.options = [options[r] for r in sample]
        self.nr = random.randint(0, size - 1)
        self.answer = self.options[self.nr]
        self.id = sample[self.nr]
        self.attr = attr

    def __str__(self):
        return 'Welk %s past het best bij %s?' % (self.attr, self.answer)


class Card:

    numbers = 'nul een twee drie vier vijf zes zeven acht negen tien'.split()

    def __init__(self, attrs):
        self.getal = attrs['getal']
        self.naam = attrs['naam']
        self.serie = attrs['serie']
        self.kernwoord = attrs['kernwoord']
        self.steekwoord = attrs['steekwoord']
        self.advies = attrs['advies']
        self.waarschuwing = attrs['waarschuwing']
        self.opmerking = attrs['opmerking']
        self.symbolen = sorted(s.strip() for s in attrs['symbolen'].split(',') if s)

    def __str__(self):
        naam = self.naam
        if self.serie == 'groot':
            naam = '%s (%s)' % (naam, self.getal)
        else:
            naam = 'de %s van %s' % (naam, self.serie)
        
        return naam

    @property
    def img(self):
        naam = self.naam
        if self.serie == 'groot':
            naam = 'GroteArcana/%s-%s' % (self.getal, naam)
        else:
            naam = 'KleineArcana/%s/%s-%s' % (self.serie, self.serie, naam)
        
        return '%s.jpg' % naam.replace(' ', '-')

    def get_attr(self, attr):
        val = getattr(self, attr)
        if attr == 'steekwoord':
            val = random.choice(val.split(', '))
        return val

    def link_symbols(self, symbols):
        for sym in self.symbolen:
            try:
                symbol = symbols[sym]
                symbol.cards.append(self)
            except KeyError:
                print('Link %s to %s FAILED' % (self, sym))

    @property
    def url(self):
        naam = self.naam

        # special cases
        if self.serie == 'Zwaarden' and self.getal == '9':
            return 'http://tarotstapvoorstap.nl/tarot-vragen/zwaarden-9-uit-de-tarot-ook-dit-gaat-voorbij/'
        if self.serie == 'Staven' and self.getal == '6':
            return 'http://tarotstapvoorstap.nl/tarotkaarten/tarotkaarten-staven-zes/'
        if self.serie == 'Pentakels' and self.naam == 'Page':
            return 'http://tarotstapvoorstap.nl/tarotkaarten/tarotkaart-pentakels-schildknaap-page/'
        if self.serie == 'groot' and self.naam == 'De Dwaas':
            return 'http://tarotstapvoorstap.nl/tarotkaarten/de-dwaas-tarot-nul/'

        # general case
        if self.serie in ['groot']:
            if naam == 'Kracht':
                naam = 'De Kracht'
            elif naam == 'De Hogepriesteres':
                naam = 'Hogepriesteres'
            naam = 'tarotkaart-%s' % naam
        else:
            try:
                naam = self.numbers[int(self.getal)]
            except IndexError:
                pass
            except ValueError:
                pass
            
            if naam == 'Page':
                naam = 'schildknaap'
                
            naam = 'tarotkaart-%s-%s' % (self.serie, naam)
            if self.serie in ['Pentakels'] and (self.getal or self.naam == 'Aas'):
                naam = 'rider-waite-%s' % naam
        
        return 'https://tarotstapvoorstap.nl/tarotkaarten/%s/' % naam.replace(' ', '-').lower()


class Deck:

    def __init__(self, symboliek, filename='kaarten.csv'):
        self.cards = []
        try:
            from data import cards
            self.parse_rows(cards)
        except ImportError:
            print('Reading from CSV. You may want to run csv2.py')
            with open(filename) as fin:
                reader = csv.DictReader(fin)
                self.parse_rows(reader)
        for card in self.cards:
            card.link_symbols(symboliek.symbolen)

    def parse_rows(self, reader):
        for row in reader:
            self.cards.append(Card(row))

    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        self.current += 1
        if self.current >= len(self.cards):
            raise StopIteration
        return self.cards[self.current]

    def question(self):
        return Question(self.cards, 
                        random.choice(['kernwoord', 'steekwoord', 'advies', 'waarschuwing']))

    def nr(self, card):
        return self.cards.index(card)

    def url(self, card):
        return url_for('card', nr=self.nr(card))

    def link(self, card):
        return '<a href="%s?hidden=0">%s</a>' % (self.url(card), card.naam)

    def directions(self, nr):
        if nr == 0:
            return (11, 1, 1, 21)
        elif nr == 1:
            return (0,2,11,21)
        elif nr == 11:
            return (1,12,0,10)
        elif nr == 20:
            return (10,21,21,19)
        elif nr == 21:
            return (20,0,10,20)

        if self.cards[nr].serie == 'groot':
            return (
                nr - 10 if nr > 10 else nr + 10,
                nr + 1 if nr < 20 else 11,
                nr + 10 if nr < 11 else nr - 10,
                nr - 1 if nr > 1 else 20
            )
        else:
            return (
                nr - 14 if nr > 35 else nr + 42,
                nr + 1 if nr < 77 else 14,
                nr + 14 if nr < 36 else nr - 42,
                nr - 1 if nr > 22 else 77
            )

        return (0,0,0,0)

class Symbool:

    symboliek = None

    def __init__(self, row):
        self.naam = row['naam'].strip().lower()
        self.betekenis = row['betekenis']
        self.referenties = [r.strip().lower() for r in row['zie'].split(',') if r]
        self.cards = []

    def __str__(self):
        return self.naam

    def get_attr(self, attr):  # for quiz answer
        return self.symboliek.get(self)

    @property
    def img(self):
        try:
            card = random.choice(self.cards)
            return card.img
        except IndexError:
            return 'achterkant.jpg'

class Symboliek:

    def __init__(self, filename='symboliek.csv'):
        self.symbolen = {}
        Symbool.symboliek = self
        
        try:
            from data import symbols
            self.parse_rows(symbols)
        except ImportError:
            print('Reading from CSV. You may want to run csv2.py')
            with open(filename) as fin:
                reader = csv.DictReader(fin)
                self.parse_rows(reader)

    def parse_rows(self, reader):
        for row in reader:
            if row['naam']:
                symbool = Symbool(row)
                self.symbolen[symbool.naam] = symbool

    def get(self, naam):
        try:
            symbool = self.symbolen[naam.lower()]
        except KeyError:
            return ''
        except AttributeError:
            symbool = naam
        betekenis = symbool.betekenis
        if betekenis:
            if symbool.referenties:
                betekenis += ' (zie ook %s)' % ', '.join(self.link_for_name(r) for r in symbool.referenties)
        else:
            referenties = ['%s (via %s)' % (self.get(ref), ref) for ref in symbool.referenties]
            betekenis = ' '.join(referenties)

        return betekenis

    @staticmethod
    def link_for_name(name):
        url = url_for('symbols')
        return '<a href="%s#%s">%s</a>' % (url, name, name)

    def url(self, symbol):
        url = url_for('symbols')
        return '%s#%s' % (url, symbol.naam)

    def link(self, symbol):
        return '<a href="%s">%s</a>' % (symbol.url, symbol.naam)

    def question(self):
        return Question(self.symbolen, 'betekenis')
