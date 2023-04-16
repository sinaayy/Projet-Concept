import pickle

def save_objects(objects, filename):
    dump = pickle.dumps(objects)
    with open(filename, "wb") as b_file:
        b_file.write(dump)

def read_objects(filename):
    objects = None
    with open(filename, "rb") as b_file:
        objects = pickle.loads(b_file.read())
    return objects
