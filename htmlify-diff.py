
import re
import sys

html_lines = []

css = '''
<style>
body {
	    background-color: linen;
}

.hunkBox {
    display: block;
    border: dotted;
    border-width: thin;
}
.hunk {
    display: block;
}
.identicalHunk {
    display: none;
}

</style>
'''

javascript = '''
<script>

function toggleVisibility(elt){
    var children = elt.children;
    for (i = 0; i < children.length; i++) {
        var s = children[i].style;
        s.display = s.display==='block' ? 'none' : 'block';
    }
}

</script>
'''


# Insert css at end of <head>
for line in sys.stdin:
    line = line.strip()
    html_lines.append(line)
    if '</head>' in line:
        html_lines.append(css)
        html_lines.append(javascript)
        html_lines.append(line)
        break

# Read until <pre>
for line in sys.stdin:
    line = line.strip()
    html_lines.append(line)
    if '<pre>' in line:
    	html_lines.append('<div class="beginning">')
    	break


hunk_start_regex = re.compile('<span.*>@@ -\d+,\d+ \+\d+,\d+ @@.*$')

hunk_div = '''
<div class="hunkBox" onclick="toggleVisibility(this)">
<div class="hunk">'''
identical_hunk_div = '''
<div class="hunkBox" onclick="toggleVisibility(this)">
<div class="identicalHunk">'''
close_hunk_div = '''</div></div>'''

# Read in all the lines
identical_hunk = False
for line in sys.stdin:
    line = line.strip()
    if "@IdenticalHunk@:" in line:
        identical_hunk = True
        continue # Drop this line.

    if hunk_start_regex.search(line) != None:
    	html_lines.append(close_hunk_div)
        html_lines.append(line)
        if identical_hunk:
            html_lines.append(identical_hunk_div)
        else:
            html_lines.append(hunk_div)
    elif line == '</pre>':
    	html_lines.append(close_hunk_div)
        html_lines.append(line)
        break
    else:
        html_lines.append(line)
    identical_hunk = False # reset

for line in sys.stdin:
    line = line.strip()
    html_lines.append(line)

for line in html_lines:
    print line

