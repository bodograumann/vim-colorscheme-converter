#!/usr/bin/env python

import sys

def parse_rgb(hex_color):
    if len(hex_color) != 6:
        raise ValueError('Invalid color! Must consist of 6 characters')
    return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
            )

def format_rgb(rgb):
    return '#%02x%02x%02x' % rgb

def rgb_luma(rgb):
    return sum(x * y for x, y in zip(rgb, (0.299, 0.587, 0.114)))

def invert_rgb(rgb):
    luma = rgb_luma(rgb)
    delta = max(-rgb[0], -rgb[1], -rgb[2],
            min(255 - rgb[0], 255 - rgb[1], 255 - rgb[2],
                255 - 2 * luma
                ))
    return tuple(x + delta for x in rgb)

def invert_luma(line):
    indent = ''
    for char in line:
        if char != '\t' and char != ' ':
            break
        indent += char

    tokens = line.split()
    if not tokens:
        return line

    command = tokens[0].rstrip('!')
    if command != 'highlight'[:len(command)]:
        return line

    new_tokens = []
    for token in tokens:
        if token.startswith('guifg=#'):
            hex_color = token.partition('guifg=#')[2]
            rgb = parse_rgb(hex_color)
            inverse = invert_rgb(rgb)
            new_tokens.append('guifg=%s' % format_rgb(inverse))

        elif token.startswith('guibg=#'):
            hex_color = token.partition('guibg=#')[2]
            rgb = parse_rgb(hex_color)
            inverse = invert_rgb(rgb)
            new_tokens.append('guibg=%s' % format_rgb(inverse))

        else:
            new_tokens.append(token)

    return indent + ' '.join(new_tokens) + '\n'

def main():
    if len(sys.argv) < 3:
        print('usage: %s in.vim out.vim' % sys.argv[0])
        exit(1)

    with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:
        output.writelines(map(invert_luma, input))

if __name__ == '__main__':
    main()
