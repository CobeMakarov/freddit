class flair:
    def __init__(self, id, text, label, subfreddit):
        self.id = id
        self.text = text
        self.label = label
        self.subfreddit = subfreddit

    def html(self):
        return '<div style="padding-bottom: 3%"><div class="label ' + self.label + '">' + self.text + '</div><button type="button" class="btn btn-link remove_flair" id="' + str(self.id) + '" style="padding: 0;">remove</button></div>'

    def simple_html(self):
        return '<div class="label ' + self.label + '">' + self.text + '</div>'
