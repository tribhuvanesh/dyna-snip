import sublime
import sublime_plugin
import urllib
import urllib2
import threading
import re

from dyna_snip_helpers import get_snippet_list, inc_snippet_object

COMMENT_MARKER_JAVA = '//'
COMMENT_MARKER_PYTHON = "#"

class PrefixrCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit

        # Extract the user query from the comment on the current line
        query_region = self.view.sel()[0] # No selection == single region
        query_line = self.view.line(query_region) # Make region span line
        query_line_contents = self.view.substr(query_line)
        self.pos = query_line.end()
        
        # Get the language from the filename extension
        filename = self.view.file_name()
        if filename.endswith('.java'):
            comment_marker = COMMENT_MARKER_JAVA
            lang = 'java'
        else:
            comment_marker = COMMENT_MARKER_PYTHON
            lang = 'python'

        query = query_line_contents.replace(comment_marker, '').strip()
        self.snippet_list = get_snippet_list(query, lang)

        self.snippet_list = sorted(self.snippet_list, key=lambda x: x['score'], reverse=True)

        """
        self.snippet_list = [{'source': 'source1', 'snippet': 'def snippet1:\n\tprint "snippet1"', 'score': 10},
                             {'source': 'source2', 'snippet': 'def snippet2:\n\tprint "snippet2"', 'score': 9},
                             {'source': 'source3', 'snippet': 'def snippet3:\n\tprint "snippet3"', 'score': 8}]
                             """
        self.snippet_titles = [item['title'] + ' (' + item['source'] + ') ' for item
                               in sorted(self.snippet_list, key=lambda x: x['score'], reverse=True)]
        self.snippets = [item['snippet'] for item
                         in sorted(self.snippet_list, key=lambda x: x['score'], reverse=True)]

        self.view.window().show_quick_panel(self.snippet_titles,\
                                            self.insert_snippet,\
                                            sublime.MONOSPACE_FONT)
        return

    def insert_snippet(self, choice):
        if '_id' in self.snippet_list[choice]:
            inc_snippet_object(self.snippet_list[choice]['_id'])
        self.view.insert(self.edit, self.pos, '\n' + self.snippets[choice])
