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
    def user_exists():
        return None

    @staticmethod
    def parse_media(media):
        image_types = (".jpg", ".jpeg", ".png", ".gif")

        if "youtube.com/watch?v=" in media:  #youtube video not in embed format
            media = media.replace("https://", "").replace("http://", "").replace("youtube.com/watch?v=", "youtube.com/embed/")
            return '<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="//' +\
                   media + '"></iframe></div>'
        elif "youtube.com/embed" in media:  #youtube video in embed format
            media = media.replace("https://", "").replace("http://", "")
            return '<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="//' + \
                   media + '"></iframe></div>'
        elif "imgur.com" in media:  #imgur
            if "/gallery/" in media or "/a/" in media:  #imgur gallery
                simple_link = media.replace("/gallery/", "/").replace("/a/", "/")
                imgur_id = media[len(media) - 5 : len(media)]

                return '<blockquote class="imgur-embed-pub" lang="en" data-id="a/' + imgur_id + '"><a href="' + simple_link + '"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>'
            elif "i.imgur.com" in media:  #imgur in embed format
                if media.endswith(".gifv") or media.endswith(".mp4") or media.endswith(".webm"):  #gif
                    simple_link = media.replace("https://", "").replace("http://", "").replace("www.", "").replace("i.", "").replace(".gifv", "").replace(".mp4", "").replace(".webm", "")
                    imgur_id = simple_link[len(simple_link) - 7: len(simple_link)]

                    return '<blockquote class="imgur-embed-pub" lang="en" data-id="' + imgur_id + '"><a href="//' + simple_link + '"></a></blockquote><script async src="//s.imgur.com/min/embed.js" charset="utf-8"></script>'
                    #return '<video preload="auto" autoplay="autoplay" loop="loop" style="width: 200px; height: 200px;"><source src="//i.' + simple_link + '.webm" type="video/webm"></source></video>'
                else:
                    return '<img src="' + media + '.jpg" class="img-responsive" />'
            else:
                if media.endswith(".gifv") or media.endswith(".mp4") or media.endswith(".webm"):
                    return '<video><source src="' + media.replace("imgur.com", "i.imgur.com") + '" type="video/webm"></video>'
                else:
                    return '<img src="' + media.replace("imgur.com", "i.imgur.com") + '.jpg" class="img-responsive" />'
        elif "gfycat.com" in media:
            return '<div style="position:relative;padding-bottom:57%"><iframe src="' + media.replace("gfycat.com/", "gfycat.com/ifr/") + '" frameborder="0" scrolling="no" width="100%" height="100%" style="position:absolute;top:0;left:0;" allowfullscreen></iframe></div>'
        elif media.endswith(image_types):
            return '<img src="' + media + '" class="img-responsive" />'

