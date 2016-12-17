''' This is the class for a recipe '''
import sys
from my_clean_string import my_clean_string

##########################################################################
class Recipe(object):
    ''' This is the respository for the class information '''
    def __init__(self, url):
        self.url = url
        self.title = ''
        self.author = ''
        self.total_time = ''
        self.recipe_notes = ''
        self.ingredients = ''
        self.directions = ''
        self.category = ''
        self.date_posted = ''
        self.date_updated = ''

    ################################################################################################
    def do_something(self):
        ''' This will generate the header for the file '''
        pass

    ################################################################################################
    def create_recipe(self):
        ''' This creates the text that will be written to the file '''
        head = ''
        head += '<div class="recipe-entry">'
        head += '<hr class="copy"/><hr class="copy"/><hr class="copy"/><hr class="copy"/>\n'
        head += '<h2><a href="{0}">{1}</a></h2>\n'.format(self.url, self.title)
        head += '<h3>by<br>{0}</h3>\n<hr class="copy"/>\n'.format(self.author)
        head += '{0}\n<hr class="copy"/>\n'.format(self.format_posted(
            self.date_posted, self.date_updated))
        head += '{0}\n<hr class="copy"/>\n'.format(self.category)
        ## this is the total time
        head += '{0}\n<hr class="copy"/>\n'.format(self.total_time)
        ## this is the recipe notes
        if self.recipe_notes != '':
            head += '{0}\n<hr class="copy"/>\n'.format(self.recipe_notes)
        head += '<table class="myOtherTable">\n'
        head += '<colgroup><col style="width:50%"/><col style="width:50%"/></colgroup>\n'
        head += '<tr>\n<td valign="top">\n'
        ## this is the ingredients
        head += '{0}\n'.format(self.ingredients)
        head += '</td>\n<td valign="top">\n'
        ## this is the directions
        head += '{0}\n'.format(self.directions)
        head += '</td>\n</tr>\n</table>\n'
        head += '<hr class="copy"/><hr class="copy"/><hr class="copy"/><hr class="copy"/>\n'
        head += '</div>\n'
        return head

    ##########################################################################
    def format_total_time(self, tsoup):
        ''' I'm going to reformat the time secton so it looks better '''
        total_time1 = tsoup.find('div', {'class':'total-time'})
        if 'strong' in str(total_time1):
            total_time_n = total_time1.find('strong').get_text()
            total_time_m = total_time1.find('strong').nextSibling
        else:
            total_time_n = ''
            total_time_m = ''
        prep_time_t = tsoup.find('div', {'class':'prep-time'}).find('small').get_text()
        cook_time_t = tsoup.find('div', {'class':'cook-time'}).find('small').get_text()
        ttime = '<div id="recipe-time">\n'
        ttime += '<table class="myOtherTable">\n<tr>\n<th><strong>Total Time</strong></th>\n'
        ttime += '<th><strong>Prep Time</strong></th>\n'
        ttime += '<th><strong>Cook Time</strong></th>\n</tr>\n'
        ttime += '<tr>\n<td id="total-time" class="c">{0}</td>\n'.format(
            total_time_n + ' ' + total_time_m)
        ttime += '<td id="prep-time" class="c">{0}</td>\n'.format(prep_time_t)
        ttime += '<td id="cook-time" class="c">{0}</td>\n</tr>\n</table>\n</div>'.format(
            cook_time_t)
        return ttime.encode('utf-8', 'ignore')

    ##########################################################################
    def format_ingredients(self, isoup):
        ''' removing tags that I do not want '''
        for tag in isoup.findAll('div', {
                'class':'relevant-slideshow'}) + isoup.findAll('div', {
                    'class':'fd-ad'}) + isoup.findAll('div', {
                        'class':'deals'}) + isoup.findAll('div', {
                            'class':'top-cat-recipe'}) + isoup.findAll('div', {
                                'class':'extras'}):
            tag.extract()
        for tag in isoup.findAll('a'):
            if 'units' in str(tag):
                tag.extract()
            elif 'nutrition' in str(tag):
                tag.parent.extract()

        del isoup['data-module']
        del isoup['class']
        isoup['id'] = 'ingredients'
        serving = isoup.find('a', {'class':'servings'})
        if serving:
            del serving['data-popup-id']
            del serving['data-target']
            del serving['data-toggle']
        return my_clean_string(unicode(isoup).encode('utf-8', 'ignore'))

    ##########################################################################
    def format_directions(self, dsoup):
        ''' removing tags that I do not want '''
        for tag in dsoup.findAll('div', {'class':'recipe-tools'}):
            tag.parent.extract()

        del dsoup['data-module']
        del dsoup['class']
        dsoup['id'] = 'directions'

        ostring = my_clean_string(unicode(dsoup).encode('utf-8', 'ignore'))
        ostring = ostring.replace('<li>', '<p>').replace('</li>', '</p>')
        ostring = ostring.replace('<ol>', '').replace('</ol>', '')
        return my_clean_string(ostring)

    ##########################################################################
    def format_recipe_notes(self, rsoup):
        ''' fixing the format for the recipe notes '''
        if rsoup:
            del rsoup['data-module']
            rsoup['class'] = 'recipe-notes'
            return my_clean_string(unicode(rsoup).encode('utf-8', 'ignore'))
        else:
            return None

    ##########################################################################
    def format_category(self, csoup):
        ''' formatting the category section '''
        if csoup:
            csoup['class'] = 'category'
            cat = unicode(csoup).replace('<span class="separator"></span>', ' / ')
            return my_clean_string(cat.encode('utf-8', 'ignore'))
        else:
            return None

    ##########################################################################
    def format_author(self, asoup):
        ''' formats the author name correctly '''
        author_name = repr(asoup.get_text())
        author_name = my_clean_string(author_name).strip().replace("u'", '')[:-1]
        return author_name

    ##########################################################################
    def format_posted(self, pdate, udate):
        '''This will format the posted and updated times '''
        div = '<p><b>Posted Date:</b> {}<br/>'.format(pdate)
        div += '<b>Updated Date:</b> {}</p>'.format(udate)
        return div
