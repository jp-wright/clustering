from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import IPython


def pycat(filename):
    with open(filename) as f:
        code = f.read()

    formatter = HtmlFormatter()
    return IPython.display.HTML(
        '<style type="text/css">{}</style>{}'.format(
            formatter.get_style_defs(".highlight"),
            highlight(code, PythonLexer(), formatter)))
