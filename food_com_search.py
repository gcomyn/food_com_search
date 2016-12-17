# -*- coding: utf-8 -*-
##################################################################################################
### Created by Stan Paszt on December 16, 2016
##################################################################################################
# Copyright 2016 Stan Paszt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
'''
This will download recipes from the search item provided from food.com.
The output will be written to the current directory.
The search item is reqired to be entered on the command line.
'''
import argparse
import json
import os
#import sys  # used for debug purposes... comment out for production

import requests
from bs4 import BeautifulSoup as bs

from fFix_FN import ffix_fn
from my_clean_string import my_clean_string
from println import _format_output, println
from recipe import Recipe

LINE_WIDTH = 163

PROG_DESC = '''
This will download recipes from the search item provided from food.com.
The output will be written to the current directory.
The search item is reqired to be entered on the command line.
'''
PROG_VER = 'food_com_search 0.0.1'

##########################################################################
class MainDoc(object):
    ''' This will hold the main document that will be writen '''
    ################################################################################################
    def __init__(self, isearch):
        self.filename = ffix_fn("food_com_results_for_({})".format(isearch))+'.html'
        self.url = 'http://www.food.com/services/mobile/fdc/search/all?pn={}&searchTerm={}'
        self.recipes = []
        self.header = ''
        self.footer = ('<hr class="copy"/><hr class="copy"/><hr class="copy"/><hr class="copy"/>'+
                       '\n</div>\n</body>\n</html>\n')
        self.search = isearch.replace(' ', '+')

    ################################################################################################
    def do_something(self):
        ''' This will generate the header for the file '''
        pass

    ################################################################################################
    def generate_header(self):
        ''' This will generate the header for the file '''
        head = ''
        head += '<!DOCTYPE html>\n<html>\n<head lang="en">\n<meta charset="UTF-8">\n'
        head += '<title>Search results for {0} on food.com</title>\n'.format(self.search)
        head += '<style type="text/css">\n/*<![CDATA[*/\n'
        head += 'p {text-align: justify; font-family: "Times New Roman", sans-serif;}\n'
        head += '.story { width: 99%; padding: 4pt; background-color: black; color: #F0F8FF; }\n'
        head += 'BODY { color: #F0F8FF; background-color: black; font-family: "Times New Roman", '
        head += 'sans-serif; font-size:25pt; }\n'
        head += 'h1, h2, h3, h4, h5 { color: orange; font-family: Ringbearer, sans-serif; '
        head += 'font-weight:100; text-align: center; }\n'
        head += 'h1 {font-size:2em;}\nh2 {font-size:1.4em;}\nh3 {font-size:1.25em;}\nh4 {font-size:'
        head += '1.10em;}\nh5 {font-size:.7em;margin:0px;}\n'
        head += 'blockquote {margin-left:1em;margin-right:1em;}\n'
        head += '.center, .c {text-align: center;}\n.italic, .i {font-style:italic;}\n'
        head += '.bold, .b {font-weight:bold;}\n.underline, .u {text-decoration:underline;}\n'
        head += '.notice, .end-note { font-size:60%; background-color: grey; border:1px dotted '
        head += 'silver; margin:0px;}\n.notice p { font-family:"Times New Roman"; color:#D2D2D2;}\n'
        head += '.notice td { font-family: "Times New Roman", sans-serif; color: #D2D2D2;}\n'
        head += '.notice th { font-family: "Times New Roman", sans-serif; color: #D2D2D2; '
        head += 'font-weight: bold;}\nA:link { color: yellow}\nA:visited { color: blue}\n'
        head += 'A:hover { color: blue; text-decoration: underline; background-color: teal;}\n'
        head += 'a:visited:hover { color: #FFF; background-color: teal;}\n'
        head += 'a:active { color: yellow; background-color: teal;}\n'
        head += 'a:visited:active { color: yellow; background-color: teal; }\n'
        head += '.copy {font-size:.85em; color: #5A5A5A; margin: 0px; }\n'
        head += '.myOtherTable, .TOC { border-collapse: collapse; width: 100%; }\n'
        head += '.myOtherTable td, .myOtherTable th { padding:5px;border:0; }\n'
        head += '.myOtherTable td { font-size: .85em; }\n/*]]>*/\n'
        head += '</style>\n</head>\n<body>\n<div class="story">\n'
        head += '<h1>Search results for {} on food.com</h1>\n'.format(self.search)
        return head

####################################################################################################
def get_page(page):
    '''
    This will download the url from the web and return the data
    '''
    try:
        page_data = requests.get(page)
        page_data.raise_for_status()
    except requests.exceptions.HTTPError as html_error:
        if html_error.response.status_code == 404:
            println(' >>>>>>>>>> 404: Page Not Found <<<<<<<<<<')
            return '404'
        else:
            println(html_error)
            return '999'
    return page_data.text

####################################################################################################
def write_file(docum, filename):
    ''' This will write the file to the disk '''
    fullpath = os.path.join(r'C:\Stan\Recipies', filename)
    if os.path.isfile(fullpath):
        println('')
        prompt = '### The file "{0}" is already created. Do you wish to overwrite it?:'.format(
            filename)
        answer = raw_input(prompt)
        if answer == 'y' or answer == 'Y':
            println('')
            println(' Writing file: {0}'.format(fullpath))
            with open(fullpath, 'wt') as outfile:
                outfile.write(docum)
        else:
            println(" Didn't save the file")
    else:
        println('')
        println(' Writing file: {0}'.format(fullpath))
        with open(fullpath, 'wt') as outfile:
            outfile.write(docum)
    return

####################################################################################################
def get_total_pages(tresults):
    ''' this will calculate the pages that need to be retreived '''
    pages = tresults / 10
    if tresults % 10 != 0:
        pages += 1
    return pages

####################################################################################################
def get_results(tbl, doc, pages, total):
    '''This will retrieve the recipes from the site and return the list'''

    results = []
    ress = tbl['results']
    for res in ress:
        results.append([res['record_url'], res['modtime'], res['latest_modtime']])

    for i in range(1, pages):
        if len(results) >= total:
            break
        println(_format_output('Retrieving Page:', str(i+1), ""))
        data = get_page(doc.url.format(i, doc.search))
        if data == '404' or data == '999':
            return
        tbl = json.loads(data)['response']

        results2 = tbl['results']
        for result in results2:
            res = [result['record_url'], result['modtime'], result['latest_modtime']]
            results.append(res)
            if len(results) == total:
                break

    return results


####################################################################################################
def generate_recipe_list(res, total):
    ''' this will generate the html code that will be printed in the file '''
    recipe_list = []

    for i, result in enumerate(res):
        arec = Recipe(result[0])

        println(' Getting recipe {:>4}... {}'.format(i+1, arec.url))
        response = get_page(arec.url)
        if response == '404' or response == '999':
            return

        soup = bs(response, 'html5lib')

        arec.date_posted = result[1]
        arec.date_updated = result[2]
        arec.category = arec.format_category(soup.find('div', {'class':'breadcrumbs'}))
        arec.title = my_clean_string(unicode(soup.find('h1').get_text()))
        arec.author = arec.format_author(soup.find('ul', {'class':'fd-byline'}).findAll(
            'span')[1])
        arec.total_time = arec.format_total_time(soup.find('div', {'class':'recipe-time'}))
        arec.recipe_notes = arec.format_recipe_notes(soup.find('div', {'class':'recipe-notes'}))
        arec.ingredients = arec.format_ingredients(soup.find('div', {'class':'ingredients'}))
        arec.directions = arec.format_directions(soup.find('div', {'class':'directions'}))
        doc = arec.create_recipe()
        recipe_list.append(doc)
        if i == total-1:
            break
    return recipe_list

##########################################################################
def save_recipes(isearch, total):
    ''' This is where the recipes will be saved to the disk '''
    println(' Searching for {0}...'.format(isearch))

    docum = MainDoc(isearch)

    println(' Searching document for recipes...')

    data = get_page(docum.url.format(1, isearch))
    if data == '404' or data == '999':
        return

    tables = json.loads(data)['response']

    total_results = int(tables['totalResultsCount'])
    println(_format_output('Total Results:', total_results, ''))

    pages = get_total_pages(total_results)
    println(_format_output('Pages:', pages, ''))

    results = get_results(tables, docum, pages, total)
    println(_format_output('Results:', len(results), ''))
    println('')
    println('-' * 163)

    recipe_list = generate_recipe_list(results, total)

    doc = docum.generate_header()
    for recipe in recipe_list:
        doc += recipe
    doc += docum.footer

    write_file(doc, docum.filename)
    return

##########################################################################
def main():
    '''
    This is the main function for the code
    '''
    parser = argparse.ArgumentParser(description=PROG_DESC, version=PROG_VER)
    parser.add_argument('-i', '--input', nargs=1, type=str, default=False,
                        help='a item to search for on food.com')
    parser.add_argument('-t', '--total', action='store', type=int, default=False,
                        help='The total number of recipes to return')
    args = parser.parse_args()

    print '#' * (LINE_WIDTH + 6)
    println(' Starting Process - {0}'.format(PROG_VER))
    println('#' * LINE_WIDTH)
    save_recipes(args.input[0], args.total)

    println('#' * LINE_WIDTH)
    println(' Completed Process - {0}'.format(PROG_VER))
    print '#' * (LINE_WIDTH + 6)
    return

##########################################################################
if __name__ == '__main__':
    main()
