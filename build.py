import os.path
import re
import subprocess
import sys

USER_AGENTS = [
    ['Chrome', 'Windows'], ['Firefox', 'Windows'], ['Edge', 'Windows'],
    ['Chrome', 'macOS'], ['Firefox', 'macOS'], ['Safari', 'macOS'],
    ['Chrome', 'Linux'], ['Firefox', 'Linux']
]
OS_LIST = ['Windows', 'macOS', 'Linux']
OS_UAS = []
for os_name in OS_LIST:
    count = 0
    for ua in USER_AGENTS:
        if ua[1] == os_name:
            count += 1
    OS_UAS.append([os_name, count])





class Parser():
    """Parser for uievents-code spec."""

    TABLE_TYPE_EVENT_SEQUENCE = 'event-sequence'
    TABLE_TYPE_EVENT_DEFINITION = 'event-definition'

    def __init__(self):
        self.in_table = False
        self.custom_in_table = False
        self.table_type = ''
        self.table_header_data = []
        self.table_column_format = []
        self.table_row_data = []
        self.is_header_row = False

        self.code = None
        self.opt = ''
        self.desc = ''

        # Only used for IMPL tables
        self.in_impl_table = False
        self.impl_info = {}
        self.impl_notes = ''
        self.impl_section = False
        self.impl_section_name = ''

    def table_row(self):
        if self.code == None:
            return ''

        req = "Yes"
        if self.opt:
            req = "No"
        return (
            '<tr>'
            '<td class="code-table-code"><code class="code" id="code-%s">"%s"</code></td>\n'
            '<td class="code-table-required">%s</td>'
            '<td>%s</td>'
            '</tr>\n') % (self.code, self.code, req, self.desc)
    
    def event_type(self, type):
        if type == '' or type == '...':
            return type
        return '<a><code>' + type + '</code></a>'
    
    def error(self, msg):
        print('---当前行数---', self.line)
        print('Error: %s' % (msg))
        sys.exit(1)

    # Handle a table row for the implementation report.
    def table_row_impl(self):
        if self.impl_section:
            return '<tr><td style="background-color: #B9C9FE" colspan="%d">%s</td></tr>\n' % (len(USER_AGENTS) + 2, self.impl_section_name)

        if self.code == None:
            return ''

        result = '<tr><td>'
        result += '<a href="https://w3c.github.io/uievents-code/#code-%s">' % self.code
        result += '<code class="code">"%s"</code>' % self.code
        result += '</a>'
        result += '</td>\n'
        for ua in USER_AGENTS:
            ua_os = ''.join(ua)
            value = self.impl_info[ua_os]
            data = ''
            if value == 'Y':
                data = '<span class="code-impl-yes">Pass</span>'
            elif value == 'F':
                data = '<span class="code-impl-no">Fail</span>'
            elif value == '?':
                data = '<span>?</span>'
            elif value == '-':
                data = '<span>N/A</span>'
            else:
                print("ERROR processing impl table:", value)
                data = '<span>?</span>'
            suffix = ''
            if ua[1] == 'Windows' or ua[1] == 'Linux':
                suffix = '-dark'
            result += '<td class="code-impl-data%s">%s</td>' % (suffix, data)
        notes = self.impl_notes
        if notes == None:
            notes = ''
        result += '<td>%s</td>' % notes
        result += '</tr>\n'
        return result

    def process_text(self, desc):
        has_newline = False
        if desc[-1:] == '\n':
            has_newline = True

        m = re.match(r'^(.*)CODE{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = '%s<code class="code">"<a href="#code-%s">%s</a>"</code>%s' % (
                pre, name, name, post)

        m = re.match(r'^(.*)CODE_NOLINK{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = pre + '<code class="code">"' + name + '"</code>' + post

        m = re.match(r'^(.*)KEY{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = '%s<code class="key">"<a href="http://www.w3.org/TR/uievents-key/#key-%s">%s</a>"</code>%s' % (
                pre, name, name, post)

        m = re.match(r'^(.*)KEY_NOLINK{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = '%s<code class="key">"%s"</code>%s' % (pre, name, post)

        m = re.match(r'^(.*)KEYCAP{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = pre + '<code class="keycap">' + name + '</code>' + post

        m = re.match(r'^(.*)GLYPH{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = pre + '<code class="glyph">"' + name + '"</code>' + post

        m = re.match(r'^(.*)UNI{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            if name[0:2] != 'U+':
                self.error('Invalid Unicode value (expected U+xxxx): %s\n' % name)
            desc = pre + '<code class="unicode">' + name + '</code>' + post

        m = re.match(r'^(.*)PHONETIC{(.+?)}(.*)$', desc)
        if m:
            pre = self.process_text(m.group(1))
            name = m.group(2)
            post = self.process_text(m.group(3))
            desc = pre + '<span class="unicode">' + name + '</span>' + post

        if has_newline and desc[-1:] != '\n':
            desc += '\n'
        return desc
    # 自定义处理文本
    def custom_process_text(self, desc):
        m = re.match(r'^(.*)EVENT{(.+?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = pre + self.event_type(name) + post

        m = re.match(r'^(.*)CODE{(.*?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = '%s<code class="code">"<a href="http://www.w3.org/TR/uievents-code/#code-%s">%s</a>"</code>%s' % (
                pre, name, name, post)

        m = re.match(r'^(.*)KEY{(.+?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = '%s<code class="key">"<a href="http://www.w3.org/TR/uievents-key/#key-%s">%s</a>"</code>%s' % (
                pre, name, name, post)

        m = re.match(r'^(.*)KEY_NOLINK{(.+?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = '%s<code class="key">"%s"</code>%s' % (pre, name, post)
    
        m = re.match(r'^(.*)KEYCAP{(.+?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = pre + '<code class="keycap">' + name + '</code>' + post

        m = re.match(r'^(.*)GLYPH{(.*?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            desc = pre + '<code class="glyph">"' + name + '"</code>' + post

        m = re.match(r'^(.*)UNI{(.+?)}(.*)$', desc)
        if m:
            pre = self.custom_process_text(m.group(1))
            name = m.group(2)
            post = self.custom_process_text(m.group(3))
            if name[0:2] != 'U+':
                self.error(
                    'Invalid Unicode value (expected U+xxxx): %s\n' % name)
            desc = pre + '<code class="unicode">' + name + '</code>' + post

        return desc

    def custom_table_row(self):
        # Don't print header row for event-definition.
        if self.is_header_row and self.table_type == Parser.TABLE_TYPE_EVENT_DEFINITION:
            return ''

        if self.is_header_row:
            self.table_row_data = self.table_header_data

        if len(self.table_row_data) == 0:
            return ''
        if self.is_header_row:
            row = '<thead><tr>'
        else:
            row = '<tr>'
        for i in range(0, len(self.table_row_data)):
            data = self.table_row_data[i]
            colname = self.table_header_data[i]
            align = self.table_column_format[i]
            style = ''
            if align == 'right':
                style = ' style="text-align:right"'
            elif align == 'center':
                style = ' style="text-align:center"'
            pre = '<td%s>' % style
            post = '</td>'
            if self.is_header_row or colname == '%':
                pre = '<th%s>' % style
                post = '</th>'
            if colname == '#':
                pre = '<td class="cell-number"%s>' % style
                if self.is_header_row:
                    data = ''
            if not self.is_header_row and data != '':
                if colname == 'Event Type':
                    data = self.event_type(data)
                if colname == 'DOM Interface':
                    data = '{{' + data + '}}'
            row += pre + self.custom_process_text(data) + post
        if self.is_header_row:
            row += '</tr></thead>\n'
        else:
            row += '</tr>\n'
        return row
    
    def process_table_line(self, line):
        if self.custom_in_table:
            # Header rows begin with '=|'
            
            m = re.match(r'^\s*\=\|(.*)\|$', line)
            if m:
                self.table_header_data = [x.strip()
                                          for x in m.group(1).split('|')]
                self.is_header_row = True
                return ''

            # New data rows begin with '+|'
            m = re.match(r'^\s*\+\|(.*)\|$', line)
            if m:
                result = self.custom_table_row()
                self.table_row_data = [x.strip()
                                       for x in m.group(1).split('|')]
                self.is_header_row = False
                return result

            # Separator lines begin with ' +' and end with '+'
            # They may only contain '-', '+' and 'o'.
            m = re.match(r'^\s* \+([\-\+o]+)\+', line)
            if m:
                # Separator lines may contain column formatting info.
                num_columns = len(self.table_header_data)
                format_data = [x.strip() for x in m.group(1).split('+')]
                if len(format_data) != num_columns:
                    self.error('Unexpected number of columns (%d) in row (expected %d):\n%s'
                               % (len(format_data), num_columns, line))
                for i in range(0, len(self.table_header_data)):
                    align = 'left'
                    if len(format_data[i]) != 0:
                        if format_data[i][0] == 'o':
                            align = 'left'
                        elif format_data[i][-1] == 'o':
                            align = 'right'
                        elif 'o' in format_data[i]:
                            align = 'center'
                    self.table_column_format.append(align)
                return ''

            # Row continued from previous line: ' |'
            m = re.match(r'^\s*\|(.*)\|', line)
            if m:
                num_columns = len(self.table_header_data)
                extra_data = [x.strip() for x in m.group(1).split('|')]
                if len(extra_data) != num_columns:
                    self.error('Unexpected number of columns (%d) in row (expected %d):\n%s'
                               % (len(extra_data), num_columns, line))
                for i in range(0, len(self.table_header_data)):
                    if len(extra_data[i]) != 0:
                        if self.is_header_row:
                            self.table_header_data[i] += ' ' + extra_data[i]
                        else:
                            self.table_row_data[i] += ' ' + extra_data[i]
                return ''
            # Tables end with: '++--'
            m = re.match(r'^\s*\+\+\+(.*)\+', line)
            if m:
                self.custom_in_table = False
                return self.custom_table_row() + '</table>\n'

            self.error('Expected table line: ' + line)
            return('')

        # Tables begin with: ++---+----+-------+
        # m = re.match(r'^\s*\+\+--[\-\+]*\+(?P<class> [\-a-z_0-9]+)?$', line)
        # if m:
        #     table_class = m.group('class')
        #     if table_class == None:
        #         table_class = 'event-sequence-table'
        #         self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
        #     else:
        #         table_class_list = table_class[1:].split("_")
        #         # 自定义表格类名，多个类名使用_隔开
        #         table_class = " ".join(table_class_list) 
        #         try:
        #             table_class_list.index("event-sequence-table")
        #             self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
        #         except ValueError:
        #             self.table_type = Parser.TABLE_TYPE_EVENT_DEFINITION
        #     self.custom_in_table = True
        #     #self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
        #     self.table_header_data = []
        #     self.table_column_format = []
        #     self.table_row_data = []
        #     return '<table class="%s">\n' % table_class

        return self.custom_process_text(line.rstrip()) + '\n'

    def process_line(self, line):
        m = re.match(r'^.*CODE(_OPT)? (\w+)\s*(.*)$', line)
        if m:
            # Write out previous code.
            result = self.table_row()
            self.opt = m.group(1)
            self.code = m.group(2)
            self.desc = self.process_text(m.group(3))
            return result

        m = re.match(r'^.*BEGIN_CODE_TABLE ([a-z0-9-]+) \"(.*)\"', line)
        if m:
            self.code = None
            self.in_table = True
            name = m.group(1)
            caption = m.group(2)
            return (
                '<table id="table-key-code-%s" class="data-table full-width">\n'
                '<caption>%s</caption>\n'
                '<thead><tr>'
                '<th style="width:20%%">{{KeyboardEvent}} {{KeyboardEvent/code}}</th>'
                '<th style="width:10%%">Required</th>'
                '<th style="width:70%%">Notes (Non-normative)</th>'
                '</tr></thead>\n'
                '<tbody>\n') % (name, caption)

        m = re.match(r'^.*END_CODE_TABLE', line)
        if m:
            result = self.table_row()
            self.code = None
            self.in_table = False
            return result + '</tbody></table>\n'

        pattern = r'^\s*CODE_IMPL(?P<nolink>_NOLINK)? (?P<code>[\w-]+)'
        for ua in USER_AGENTS:
            ua_os = ''.join(ua)
            pattern += r'\s+(?P<%s>[YF\?\-])' % ua_os
        pattern += r'\s*(?P<Notes>\w.*)?$'
        m = re.match(pattern, line)
        if m:
            # Write previous row.
            result = self.table_row_impl()
            self.code = m.group('code')
            self.nolink = m.group('nolink')
            self.impl_info = {}
            self.impl_section = False
            for ua in USER_AGENTS:
                ua_os = ''.join(ua)
                self.impl_info[ua_os] = m.group(ua_os)
            self.impl_notes = m.group('Notes')
            return result

        m = re.match(r'^\s*CODE_IMPL_SECTION (.+)$', line)
        if m:
            result = self.table_row_impl()
            self.code = None
            self.impl_section = True
            self.impl_section_name = m.group(1)
            return result

        m = re.match(r'^\s*BEGIN_CODE_IMPL_TABLE ([a-z0-9-]+)', line)
        if m:
            self.code = None
            self.in_impl_table = True
            name = m.group(1)
            header = '<thead><tr><th rowspan=2>[=code attribute value=]</th>'
            for os in OS_UAS:
                header += '<th class="code-impl-data" colspan=%d>%s</th>' % (
                    os[1], os[0])
            header += '<th rowspan=2>Notes</th></tr>\n'
            header += '<tr>'
            for ua in USER_AGENTS:
                header += '<th class="code-impl-data">%s</th>' % ua[0]
            header += '</tr></thead>\n'
            return (
                '<table id="code-table-%s" class="data-table full-width">\n'
                '%s'
                '<tbody>\n') % (name, header)

        m = re.match(r'^\s*END_CODE_IMPL_TABLE', line)

        if m:
            result = self.table_row_impl()
            self.code = None
            self.in_impl_table = False
            return result + '</tbody></table>\n'

        if self.in_table:
            self.desc += self.process_text(line)
            return ''

        if self.in_impl_table:
            m = re.match(r'^(\s*)(<!--.+-->)?(\s*)$', line)
            if m:
                return ''
            print('*** ERROR *** unrecognized line in IMPL table: ' + line)
            return ''
        #  匹配自定义表格
        m = re.match(r'^\s*\+\+--[\-\+]*\+(?P<class> [\-a-z_0-9]+)?$', line)

        if m:
            table_class = m.group('class')
            if table_class == None:
                table_class = 'event-sequence-table'
                self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
            else:
                table_class_list = table_class[1:].split("_")
                # 自定义表格类名，多个类名使用_隔开
                table_class = " ".join(table_class_list) 
                try:
                    table_class_list.index("event-sequence-table")
                    self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
                except ValueError:
                    self.table_type = Parser.TABLE_TYPE_EVENT_DEFINITION
            self.custom_in_table = True
            #self.table_type = Parser.TABLE_TYPE_EVENT_SEQUENCE
            self.table_header_data = []
            self.table_column_format = []
            self.table_row_data = []
            return '<table class="%s">\n' % table_class
        
        if self.custom_in_table:
            return self.process_table_line(line)
            

        return self.process_text(line)

    def process(self, src, dst):
        if not os.path.isfile(src):
            self.error('File "%s" doesn\'t exist' % src)

        try:
            infile = open(src, 'r', -1, 'utf-8')
        except IOError as e:
            self.error('Unable to open "%s" for reading: %s' % (src, e))

        try:
            outfile = open(dst, 'w', -1, 'utf-8')
        except IOError as e:
            self.error('Unable to open "%s" for writing: %s' % (dst, e))

        self.line = 0
        for line in infile:
            self.line += 1
            new_line = self.process_line(line)
            outfile.write(new_line)

        outfile.close()
        infile.close()


def main():
    files = [
            ['index-source.txt', 'index.bs'],
            ['impl-report.txt', 'impl-report.bs'],
    ]

    # Generate the full bikeshed file.
    parser = Parser()
    for f in files:
        src = f[0]
        dst = f[1]

        print('Pre-processing %s -> %s' % (src, dst))
        parser.process(src, dst)

        print('Bikeshedding %s...' % dst)
        subprocess.call(["bikeshed", "spec", dst])


if __name__ == '__main__':
    main()
