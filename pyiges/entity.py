#!/usr/bin/env python
import os
from pyiges.constants import line_font_pattern

def process_global_section(global_string):
    print(global_string)


class Entity():

    def __init__(self, iges):
        self.d = dict()
        self.parameters = []
        self.iges = iges

    def add_section(self, string, key, type='int'):
        string = string.strip()
        if type == 'string':
            self.d[key] = string
        else:
            if len(string) > 0:
                self.d[key] = int(string)
            else:
                self.d[key] = None

    def __str__(self):
        s = "----- Entity -----" + os.linesep
        s += str(self.d['entity_type_number']) + os.linesep
        s += str(self.d['parameter_pointer']) + os.linesep
        s += str(self.d['structure']) + os.linesep
        s += line_font_pattern[self.d['line_font_pattern']] + os.linesep
        s += str(self.d['level']) + os.linesep
        s += str(self.d['view']) + os.linesep
        s += str(self.d['transform']) + os.linesep
        s += str(self.d['label_assoc']) + os.linesep
        s += str(self.d['status_number']) + os.linesep
        s += str(self.d['line_weight_number']) + os.linesep
        s += str(self.d['color_number']) + os.linesep
        s += str(self.d['param_line_count']) + os.linesep
        s += str(self.d['form_number']) + os.linesep
        s += str(self.d['entity_label']) + os.linesep
        s += str(self.d['entity_subs_num'])

        return s

    def _add_parameters(self, parameters):
        self.parameters.append(parameters)
