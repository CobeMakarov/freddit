class misc:
    @staticmethod
    def objinlist(key, val, list):
        found = False

        for obj in list:
            found = getattr(obj, key) == val

            if found:
                break

        return found