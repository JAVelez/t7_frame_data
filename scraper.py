from selenium import webdriver
from selenium.webdriver.common.by import By
from time import time
from models import character_model, move_model
import os

path = 'chromedriver.exe'
driver = webdriver.Chrome(executable_path=path)
# driver.get('https://rbnorway.org/T7-frame-data/')

suffix_syntax = '-t7-frames'
char_list_names = ('akuma', 'alisa', 'anna', 'armor-king', 'asuka', 'bob', 'bryan', 'claudio', 'devil-jin', 'dragunov',
                   'eddy', 'eliza', 'fahkumram', 'feng', 'ganryu', 'geese', 'gigas', 'heihachi', 'hwoarang', 'jack7',
                   'jin', 'josie', 'julia', 'katarina', 'kazumi', 'kazuya', 'king', 'kuma', 'lars', 'law', 'lee',
                   'lei', 'leo', 'leroy', 'lili', 'lucky-chloe', 'marduk', 'master-raven', 'miguel', 'negan', 'nina',
                   'noctis', 'paul', 'shaheen', 'steve', 'xiaoyu', 'yoshimitsu', 'zafina')
char_list_names_test = ('akuma', 'bryan', 'shaheen', 'zafina')

iter_list = char_list_names
if os.environ.get('test'):
    iter_list = char_list_names_test

char_list = []

t_start_complete = time()

for c in iter_list:
    t_start = time()
    driver.get('https://rbnorway.org/' + c + suffix_syntax)
    page = driver.find_element_by_xpath("//h2[@class='title']")

    # create character
    character = character_model(name=c)

    # create move entry
    special_move_index = 1
    special_move_list_length = driver.find_element_by_xpath("//div[@class='entry clearfix']/table[%d]/tbody" % special_move_index).text.count('\n') + 1
    if character.name != 'alisa' and character.name != 'heihachi':
        for m in range(special_move_list_length):
            # create move entry
            move = move_model()
            if move.extract_move_properties(row=m + 1, driver=driver):
                # save move
                character.add_move(move)
    else:
        if character.name == 'alisa':
            for m in range(special_move_list_length):
                if 68 <= m <= 71:
                    # implement code to add last two moves missing
                    pass
                else:
                    move = move_model()
                    move.extract_move_properties(row=m + 1, driver=driver)
                    character.add_move(move)
        if character.name == 'heihachi':
            for m in range(special_move_list_length):
                if m == 69:
                    # implement code to add last move missing
                    pass
                else:
                    move = move_model()
                    move.extract_move_properties(row=m + 1, driver=driver)
                    character.add_move(move)

    # TODO add basic fc moves such as d jab

    # save character
    if character.contains_dick_jab():
        pass
    else:
        move = move_model()
        move.add_dick_jab()
        character.add_move(move)

    char_list.append(character)
    t_elapsed = (time() - t_start)
    print('extracted %s successfully in %f' % (page.text, t_elapsed))

t_elapsed_complete = (time() - t_start_complete) / 60
print('finished update of data in %f minutes' % t_elapsed_complete)

driver.quit()