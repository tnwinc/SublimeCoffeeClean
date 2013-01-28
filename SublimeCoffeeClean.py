import sublime_plugin


class CoffeeCleanCommand(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        if len(view.file_name()) > 0 and view.file_name().endswith((".coffee")):
            edit = view.begin_edit()

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

            for replacement in replacements:
                find = replacement[0]
                replace = replacement[1]

                regions = view.find_all(find)

                if regions:
                    for region in reversed(regions):
                        view.replace(edit, region, replace)

            view.end_edit(edit)
