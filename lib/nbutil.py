from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import IPython


def hide_axes(axes):
    axes.set_frame_on(False)
    [n.set_visible(False) for n in axes.get_xticklabels() + axes.get_yticklabels()]
    [n.set_visible(False) for n in axes.get_xticklines() + axes.get_yticklines()]


def pycat(filename):
    with open(filename) as f:
        code = f.read()

    formatter = HtmlFormatter()
    return IPython.display.HTML(
        '<style type="text/css">{}</style>{}'.format(
            formatter.get_style_defs(".highlight"),
            highlight(code, PythonLexer(), formatter)))
