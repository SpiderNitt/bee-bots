import pickle
import sys

filename = "coords.pickle"


def retrieve_state(filename):
    dbfile = open(filename, "rb")
    db = pickle.load(dbfile)
    dbfile.close()
    return db


if __name__ == "__main__":
    port = sys.argv[1]

