import sys
import re

def write_to_c(filename, outfile):

    def add_to_list(lst, x):
        try:
            int(x)
            float(x)
            numerical = True
        except:
            numerical = False
        if x not in lst and not numerical:
            lst.append(x)
        return lst

    variables = []

    fout = open(outfile, 'w')
    print("#include <stdio.h>", file=fout)
    print("\nint main()", file=fout)
    print("{", file=fout)

    with open(filename, 'r', encoding="utf-8") as file:
        for s in file:
            s = s.replace(':=', "#").replace(":", ',')
            words = s.split(',')
            for i, w in enumerate(words):
                words[i] = w.strip().replace('#', ':=').replace('@', '$')
            if len(words) < 2:
                continue  # skip lines that aren't valid quads
            if words[1] == ':=':
                variables = add_to_list(variables, words[2])
                variables = add_to_list(variables, words[4])
            if words[1] in ['+', '-', '*', '/']:
                variables = add_to_list(variables, words[2])
                variables = add_to_list(variables, words[3])
                variables = add_to_list(variables, words[4])
            if words[1] in ['=', '<>', '<=', '>=', '>', '<']:
                variables = add_to_list(variables, words[2])
                variables = add_to_list(variables, words[3])

    for x in variables:
        print("int", x, ';', file=fout)
    print(file=fout)

    # Re-open the file and write the corresponding C code based on the lines
    with open(filename, 'r', encoding="utf-8") as file:
        for s in file:
            s = s.replace(':=', "#").replace(":", ',')
            words = s.split(',')
            for i, w in enumerate(words):
                words[i] = w.strip().replace('#', ':=').replace('@', '$')
            print('L' + words[0] + ': ', end='', file=fout)
            if words[1] == ':=':
                print(words[4] + '=' + words[2] + ';', end='', file=fout)
            elif words[1] == '+':
                print(words[4] + '=' + words[2] + '+' + words[3] + ';', end='', file=fout)
            elif words[1] == '-':
                print(words[4] + '=' + words[2] + '-' + words[3] + ';', end='', file=fout)
            elif words[1] == '*':
                print(words[4] + '=' + words[2] + '*' + words[3] + ';', end='', file=fout)
            elif words[1] == '/':
                print(words[4] + '=' + words[2] + '/' + words[3] + ';', end='', file=fout)
            elif words[1] == 'jump':
                print('goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '=':
                print('if (' + words[2] + ' == ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '<>':
                print('if (' + words[2] + ' != ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '<=':
                print('if (' + words[2] + ' <= ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '>=':
                print('if (' + words[2] + ' >= ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '>':
                print('if (' + words[2] + ' > ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == '<':
                print('if (' + words[2] + ' < ' + words[3] + ') goto L' + words[4] + ';', end='', file=fout)
            elif words[1] == 'out':
                print('printf("%d\\n",' + words[2] + ');', end='', file=fout)
            elif words[1] == 'in':
                print('scanf("%d",&' + words[2] + ');', end='', file=fout)
            elif words[1] in ['begin_block', 'end_block', 'halt']:
                pass
            elif words[1] in ['par', 'call', 'retv', 'ret']:
                print('functions not supported:', words[1])
                sys.exit(1)
            else:
                print('unknown operator:', words)
                sys.exit(1)
            print(file=fout)
    print('}\n', file=fout)
    fout.close()

if __name__ == '__main__':
    from pathlib import Path
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        outfile = filename[:-3]+'c'
        file_path = Path(filename)
        if file_path.exists():
            write_to_c(filename,outfile)
        else:
            print(f"Error: File '{filename}' does not exist.")
            sys.exit(-1)
    elif len(sys.argv) > 2:
        print(f"More commands line arguments than expected.")
        sys.exit(-1)
    else:
        print("Error: No filename provided.")
        sys.exit(-1)
