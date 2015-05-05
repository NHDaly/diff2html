
import re
import sys
import subprocess

def get_output_from_command(command_string):
    return subprocess.check_output(command_string.split())


content_lines = []
# Read in all the lines
for line in sys.stdin:
    content_lines.append(line)

diff_line = content_lines[0]
diff_words = diff_line.split()
files = diff_words[-2], diff_words[-1]

index_line = content_lines[1]
index_words = index_line.split()
blobs = index_words[-2].split('..')

hunk_start_regex = re.compile('^@@ -(\d+),(\d+) \+(\d+),(\d+) @@.*$')

hunks = [(idx, int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for idx, l in enumerate(content_lines) for m in [hunk_start_regex.search(l)] if m]


full_files = (get_output_from_command('git cat-file -p ' + blobs[0]).splitlines(True),
              get_output_from_command('git cat-file -p ' + blobs[1]).splitlines(True))

def write_line(out_lines, line):
    out_lines.append(line)
    sys.stdout.write(out_lines[-1])
    
out_lines = []
i,j = 0,0
a_i, b_i = 0,0
# Insert preamble diff content lines until first hunk.
while i < hunks[j][0]:
    write_line(out_lines, content_lines[i])
    i+=1

while j < len(hunks):
    # Copy unchanged portion
    hunk_len = hunks[j][1] - a_i - 1
    if a_i < hunks[j][1] - 1:
        write_line(out_lines, '\n@IdenticalHunk@:\n@@ -%d,%d +%d,%d @@\n' % (a_i + 1, hunk_len, b_i + 1, hunk_len))
    while a_i < hunks[j][1] - 1:
        write_line(out_lines, ' ' + full_files[0][a_i])
        a_i+=1
        b_i+=1

    # Insert diff content lines until next hunk.
    extra_lines = 1 # Don't double count the diff lines (one "-" and one "+").
    while i < hunks[j][0] + hunks[j][2] + extra_lines:
        write_line(out_lines, content_lines[i])
        if (content_lines[i][0] == "-"):
        	extra_lines += 1;
        i+=1

    # update unchanged portion marker to after diff hunk.
    a_i += hunks[j][2]
    b_i += hunks[j][4]
    j+=1

# Print out any unchanged lines after the last hunk.
# Copy unchanged portion
j-=1
hunk_len = len(full_files[0]) - a_i;
if a_i < len(full_files[0]):
    write_line(out_lines, '\n@IdenticalHunk@:\n@@ -%d,%d +%d,%d @@\n' % (a_i + 1, hunk_len, b_i + 1, hunk_len))
while a_i < len(full_files[0]):
    write_line(out_lines, ' ' + full_files[0][a_i])
    a_i+=1
    b_i+=1

#for line in out_lines:
    #sys.stdout.write(line)

