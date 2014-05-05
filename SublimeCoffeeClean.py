import sublime_plugin
import string
import re

part_in_quotes = re.compile(r"([\"'])(?:\\\1|.)*?\1")

replacements = [
    # missing spaces
    ['(?<=\S),(?=\S)', ', '],
    [':(?=[(@=\'"-])', ': '],
    ['=\{', '= {'],
    ['=\[', '= ['],
    ['=\(', '= ('],
    ['=\(', '= ('],
    ['=\'', '= \''],
    ['="', '= "'],
    ['(?<=[a-zA-Z0-9\'"])=', ' ='],

    # extra spaces
    ['[ \t]+=[ \t]+', ' = '],
    ['(?<=\S)[ \t]+,', ','],
    ['\[[ \t]+(?=\S)', '['],
    ['(?<=\S)[ \t]+\]', ']'],
    ['\([ \t]+(?=\S)', '('],
    ['(?<=\S)[ \t]+\)', ')'],
    ['\)\s+->', ')->'],
    ['\)\s+=>', ')=>'],

    # ensure a space before a lambda in parens
    ['\((?=\([a-zA-Z0-9,]+\)-)', '( '],
    ['\((?=\([a-zA-Z0-9,]+\)=)', '( '],

    # quotes
    ['""', "''"],

    # misc
    ["'use strict';", "'use strict'"],
    ['"use strict";', "'use strict'"],
    ['@$', 'this']
]


def is_between_quotes(region, view):
    segment = view.substr(region)
    line = view.substr(view.line(region))
    match = re.search(part_in_quotes, line)

    if not match:
        return False

    return match.group(0) in segment


class CoffeeCleanCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        if len(view.file_name()) > 0 and view.file_name().endswith((".coffee")):

            for replacement in replacements:
                find = replacement[0]
                replace = replacement[1]

                regions = view.find_all(find)

                if regions:
                    for region in reversed(regions):
                        if not is_between_quotes(region, view):
                            view.replace(edit, region, replace)


class CoffeeCleanOnSaveCommand(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.window().run_command('coffee_clean')
