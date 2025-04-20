class science:
    def __init__(self):
        self.full_name = None
        self.tags = None
        self.role = None
        self.telephone = None
        self.fax = None
        self.mail = None
        self.positions = None
        self.interests = None
        self.publications = None
        self.rewards = None
        self.profiles = None
        self.key_words= []
        self.current_place = None

    def ret_slov(self):
        return {
            "ФИО": self.full_name,
            "Роль": self.role,
            "Роли": self.tags,
            "Телефон": self.telephone,
            "Факс": self.fax,
            "Mail": self.mail,
            "Должности": self.positions,
            "Ключевые слова": self.key_words,
            "Профили": self.profiles
        }