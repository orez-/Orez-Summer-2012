import hashlib
import os

from board import Board, TileFeature


class LevelSave(object):
    @staticmethod
    def save(full_filename, board, start):
        #full_filename = LevelLoad.full_path(filename)
        if os.path.isfile(full_filename):
            return False
        with open(full_filename, "w") as f:
            stri = '\n'.join([''.join([hex(elem)[2:] for elem in row])
                for row in board.data])
            stri += "\n^" + str(start.x) + "," + str(start.y) + "\n"

            did = []
            reverse = {v:k for k, v in board.stuff.items()}
            for d in board.stuff.items():
                i, s = LevelSave.write_feature(did, reverse, *d)
                stri += s
            f.write(stri)
        return True

    @staticmethod
    def save_level(filename, board, start):
        return LevelSave.save(LevelLoad.full_path(filename), board, start)

    @staticmethod
    def save_draft(filename, board, start):
        return LevelSave.save(LevelLoad.full_path_draft(filename), board, start)

    @staticmethod
    def write_feature(did, data, (y, x), feature):
        stri = ""
        optional = ""
        if feature in did:  # did already
            return did.index(feature), ""
        if feature.CAN_LINK:
            ny, nx = data[feature.linked]
            i, s = LevelSave.write_feature(did, data, (ny, nx), feature.linked)
            stri += s
            optional = "," + str(i)
        did.append(feature)
        return len(did) - 1, stri + ','.join(map(str,
            (y, x, TileFeature.object_to_id(feature)))) + optional + "\n"

class LevelLoad(object):
    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            step = 0
            tiles = []
            stuff = {}
            stuff_list = []

            for line in f:
                if step == 0:   # tiles
                    if line[0] == "^":  # player loc
                        board_toR = Board(tiles)
                        player_start = map(int, line[1:].split(","))
                        step = 1
                        continue
                    tiles.append(map(int, line.rstrip()))
                if step == 1:
                    # "2,3,2,1
                    # "2,3,4
                    splat = line.split(",")
                    item_data = map(int, splat[:3])
                    item = TileFeature.id_to_item(item_data[2])
                    optional = splat[3:]
                    if optional:
                        if optional[0] and optional[0][0] == '"':  # pass as string
                            optional = (','.join(optional))[1:]
                            item = item(board_toR, optional)
                        else:   # these are currently the only options :|
                            item = item(board_toR, stuff_list[int(optional[0])])
                    else:
                        item = item(board_toR)
                    stuff_list.append(item)
                    stuff[(item_data[0], item_data[1])] = item
            board_toR.add_stuff(stuff)
            return player_start, board_toR
            # handle data

    @staticmethod
    def check_hash(filename, md5):
        with open(filename, r) as f:
            return hashlib.md5(f.read()) == md5  # probably the same file

    @staticmethod
    def full_path(*args):
        return "maps/" + (''.join(map(str, args))) + ".skb"

    @staticmethod
    def full_path_draft(*args):
        return "draft/" + (''.join(map(str, args))) + ".skb"

    @staticmethod
    def load_level(filename, md5=None):
        full_filename = LevelLoad.full_path(filename)
        if md5 is not None:  # your friend wants to load his map: do you have it?
            if os.path.isfile(full_filename):   # you have a file of that name
                if check_hash(full_filename, md5):   # same hash!
                    return LevelLoad.load(full_filename)
                # making it here means the file exists but the hash is wrong.
                # we still want to download the new data into this file, but
                # we don't want to lose the old data. So we store the old in
                # the next filename (#)
                i = 0
                new_filename = full_filename
                while os.path.isfile(new_filename):
                    i += 1
                    new_filename = LevelLoad.full_path(filename, " (", i, ")")
                os.rename(full_filename, new_filename)
            # TODO: ask to download the file, and then do so.
            pass
        return LevelLoad.load(full_filename)
