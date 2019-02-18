import re
from .base import Base
from deoplete.util import getlines

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'ComradeIntelliJ-complete'
        self.mark = '[Cde]'
        self.filetypes = ['java']
        self.rank = 100
        self.max_pattern_length = 100
        self.is_bytepos = True
        self.input_pattern = '[^. \t0-9]\.\w*'
        self.is_debug_enabled = True

    def get_complete_position(self, context):
        m = re.search(r'\w*$', context['input'])
        return m.start() if m else -1


    def gather_candidates(self, context):
        #self.print_error(context)
        buf_id = context["bufnr"]
        buf_changedtick = self.vim.request("nvim_buf_get_changedtick", buf_id)
        buf_name = self.vim.request("nvim_buf_get_name", buf_id)
        win = self.vim.current.window

        row = win.cursor[0] - 1
        col = win.cursor[1]
        ret = {
            "buf_id" : buf_id,
            "buf_name" : buf_name,
            "buf_changedtick" : buf_changedtick,
            "row" : row,
            "col" : col};
        results = self.vim.call("ComradeRpcRequest", "comrade_complete", ret)
        context["is_async"] = not results["is_finished"]
        return results["candidates"]
