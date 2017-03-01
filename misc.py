from random import randint

class misc:
    @staticmethod
    def obj_exists_key(key, val, list):
        found = False

        for obj in list:
            found = (getattr(obj, key) == val)

            if found:
                break

        return found

    @staticmethod
    def get_obj_key(key, val, list):
        res = None

        for obj in list:
            if getattr(obj, key) == val:
                res = obj

        return res

    @staticmethod
    def get_objs_key(key, val, list):
        res = []

        for obj in list:
            if getattr(obj, key) is val:
                res.append(obj)

        return res

    @staticmethod
    def remove_by_key(key, val, list):
        index = 0

        for obj in list[:]:
            if getattr(obj, key) is val:
                break
            index += 1

        index -= 1

        del list[index]

    @staticmethod
    def parse_media(media):
        if "youtube.com/watch?v=" in media:  #youtube video
            return '<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="' +\
                   media + '"></iframe></div>'

