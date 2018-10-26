import sys
import metapy

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building index...')
    idx = metapy.index.make_inverted_index(cfg)
    if idx:
        print('Index creation is successful !')
