import argparse
from fretboard_scale_image import make_fretboard, get_note_locations, get_note_highlights, draw_guitar_scale

def parse_args():
    parser = argparse.ArgumentParser(description='Simplified scale creator', add_help=False)
    parser.add_argument('--help', action='help')
    
    # required arguments
    parser.add_argument('-s', '--num-strings', 
                        help='Number of strings on your fretted instrument',
                        type=int,
                        default=6)      # reaslistically we will only want ot use this for standard guitar

                        # default to 16, since after 12 we repeat ourselves but we want to be able to see the relation between the notes below and above fret 12 within usable range
    parser.add_argument('-f', '--num-frets',
                        help='Number of frets on your fretted instrument',
                        type=int,
                        default=16)

# TODO: Make enum of common guitar tunings, use as argument instead of comma separated list
    parser.add_argument('-t', '--tuning',
                        help='Comma separated list of notes your instrument is tuned to starting from lowest string',
                        type=str,
                        default="e,a,d,g,b,e")

    parser.add_argument('--scale',
                        help='Name of your scale, e.g. g, amin, bmaj, cmin, d, etc...',
                        type=str,
                        default='c')
    
    parser.add_argument('--scale-notes',
                        help='Comma separated list of notes in your scale, if present will use instead of the --scale option',
                        default=None,
                        type=str)

    parser.add_argument('-p', '--save-path',
                        help='File path to save image to. Can be a .pdf, .png, or .svg file.',
                        default='scale.png',
                        type=str)
    

    color_map = 'a:g,a#:c,b:l,b#:m,c:r,c#:o,d:y,d#:p,e:z,f:b,f#:t,g:k,g#:n'
    parser.add_argument('-c', '--note-colors',
                        type=str,
                        default=color_map)

    parser.add_argument('-w', '--im-width', 
                        help='Output image width',
                        type=int,
                        required=False,
                        default=1040)
    parser.add_argument('-h', '--im-height',
                        help='Output image height',
                        type=int,
                        required=False,
                        default=500)
    parser.add_argument('-m', '--marker-radius-multiplier',
                        help='Multiplier for note marker radius.',
                        type=float,
                        required=False,
                        default=1.0)
    
    def str2bool(v):
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')
    parser.add_argument('-r', '--realistic-spacing',
                        help='Turn realistic fretboard spacing on or off',
                        type=str2bool, nargs='?',
                        const=True, default=True,
                        required=False)
    parser.add_argument('-d', '--dark-mode',
                        type=str2bool, nargs='?',
                        help='Enable dark mode.',
                        const=True, default=False,
                        required=False)
    args = parser.parse_args()


    if args.scale_notes is None:
        notes = ['a', 'a#', 'b', 'c', 'c#','d', 'd#','e', 'f', 'f#', 'g', 'g#']
        major_offsets = [2,2,1,2,2,2,1]
        minor_offsets = [2,1,2,2,1,2,2]

        note = args.scale[0]
        if len(args.scale) > 1 and args.scale[1] == '#':
            note += '#'

        pattern = major_offsets
        args.scale_notes = note

        if args.scale.find('min') != -1:
            pattern = minor_offsets

        for offset in pattern:
            note = notes[ (notes.index(note) + offset) % 12]
            args.scale_notes += ','
            args.scale_notes += note
    
    return args

def main():
    args = parse_args()
    
    if args.marker_radius_multiplier <= 0:
        raise ValueError('Marker size multiplier (-m) must be greater than 0.')
    
    # ridiculous that argparse doesn't support CSV input lists
    args.tuning = [n.lower() for n in args.tuning.split(',')]
    args.scale_notes = [n.lower() for n in args.scale_notes.split(',')]
    
    # make badass images
    fretboard = make_fretboard(args)
    note_locations = get_note_locations(fretboard)
    note_highlights = get_note_highlights(args)
    draw_guitar_scale(args, fretboard, note_locations, note_highlights)
    
if __name__ == "__main__":
    main()
