from __future__ import unicode_literals, print_function

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from style import StyleFactory
from completer import KubectlCompleter
from lexer import KubectlLexer

import os
import click
import sys
import subprocess


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


class Kubeshell(object):
    def __init__(self, refresh_resources=True):
        self.history = FileHistory(os.path.expanduser('~/.kube-shell/history'))
        self.completer = KubectlCompleter()
        if not os.path.exists(os.path.expanduser("~/.kube-shell/")):
            os.makedirs(os.path.expanduser("~/.kube-shell/"))
        pass
    def run_cli(self):
        while 1:
            user_input = prompt('kube-shell> ',
                        history=self.history,
                        auto_suggest=AutoSuggestFromHistory(),
                        style=StyleFactory("vim").style,
                        lexer=KubectlLexer,
                        completer=self.completer)
            if user_input == "clear":
                click.clear()
            elif user_input == "exit":
                sys.exit()
            if user_input:
                if '-o' in user_input and 'json' in user_input:
                    user_input = user_input + ' | pygmentize -l json'
                p = subprocess.Popen(user_input, shell=True)
                p.communicate()
