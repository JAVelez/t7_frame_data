from parse import *


class character_model:
    def __init__(self, name):
        self.name = name
        self.move_list = []

    def add_move(self, move):
        self.move_list.append(move)

    def export_moves(self):
        pass

    def contains_dick_jab(self):
        for m in self.move_list:
            if (m.input.__contains__('FC+1') or m.input.__contains__('d+1')) and m.speed.__contains__('10'):
                return True
        return False


class move_model:
    def __init__(self):
        self.name = ''
        self.input = ''
        self.hit_prop = ''
        self.dmg = ''
        self.speed = ''
        self.on_block = ''
        self.on_hit = ''
        self.on_ch = ''

    def extract_move_properties(self, row, driver, category=1):
        self.input = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[1]" % (category, row)).text.lower()
        self.hit_prop = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[2]" % (category, row)).text.lower()
        self.dmg = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[3]" % (category, row)).text.lower()
        self.speed = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[4]" % (category, row)).text.lower()
        self.on_block = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[5]" % (category, row)).text.lower()
        self.on_hit = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[6]" % (category, row)).text.lower()
        self.on_ch = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody/tr[%s]/td[7]" % (category, row)).text.lower()
        if self.clean_input():
            self.clean_hit_prop()
            self.clean_dmg()
            self.clean_speed()
            self.clean_on_block()
            self.clean_on_hit(self.on_hit)
            self.clean_on_hit(self.on_ch)
            return True
        else:
            return False

    def add_dick_jab(self):
        self.name = '"Down jab"'
        self.input = '"FC+1"'
        self.hit_prop = 'm'
        self.dmg = 5
        self.speed = 10
        self.on_block = -5
        self.on_hit = '"+6"'
        self.on_ch = '"+6"'

    def clean_input(self):
        if self.input.lower().__contains__('counter'):
            return False
        if self.input.lower().__contains__('after tnt'):
            return False
        else:
            return True

    def clean_hit_prop(self):
        # replace
        self.hit_prop = self.hit_prop.lower().replace(' (tj)', '')
        self.hit_prop = self.hit_prop.lower().replace(' (tc)', '')
        self.hit_prop = self.hit_prop.lower().replace('(tj)', '')
        self.hit_prop = self.hit_prop.lower().replace('(tc)', '')
        self.hit_prop = self.hit_prop.lower().replace('m(throw)', 'mub')
        self.hit_prop = self.hit_prop.lower().replace('(throw)', '')
        self.hit_prop = self.hit_prop.lower().replace(' (throw)', '')
        self.hit_prop = self.hit_prop.lower().replace('sm', 'm')
        self.hit_prop = self.hit_prop.lower().replace('!', 'ub')
        self.hit_prop = self.hit_prop.lower().replace('(tport)', '')
        self.hit_prop = self.hit_prop.lower().replace(' (tport)', '')
        self.hit_prop = self.hit_prop.lower().replace('ll', 'l, l')
        self.hit_prop = self.hit_prop.lower().replace('mm', 'm, m, ')
        self.hit_prop = self.hit_prop.lower().replace('hh', 'h, h, ')

        # parse
        self.hit_prop = self.expand_multiples('x', self.hit_prop)
        self.hit_prop = self.clean_commas(self.hit_prop)

        # final strip of trailing whitespaces
        self.hit_prop = self.hit_prop.strip()

        # rep_of_hits = search('{hit:l}{hit2:l}', self.hit_prop)
        # if rep_of_hits:
        #     self.hit_prop = self.hit_prop.replace('%s%s' % (rep_of_hits['hit'], rep_of_hits['hit2']),
        #                                           '%s, %s' % (rep_of_hits['hit'], rep_of_hits['hit2']))

    def clean_dmg(self):
        pass

    def clean_speed(self):
        pass

    def clean_on_block(self):
        pass

    def clean_on_hit(self, on_hit):
        pass

    def expand_multiples(self, mult, string):
        # parse
        times = search('%s {times:d}' % mult, string)
        if times:
            new_hit_prop = ''
            hit = search('{hit:l} %s' % mult, string)['hit']
            for i in range(times['times']):
                new_hit_prop = new_hit_prop + hit + ', '
            return string.replace('%s x %d' % (hit, times['times']), new_hit_prop)
        else:
            return string

    def clean_commas(self, string):
        index = string.strip().rfind(',')
        if index == len(string.strip()) - 1:
            return string[:index]
        else:
            return string

