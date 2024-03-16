class GlobalOptions:
    def __init__(self, token, ya_usr_id, tg_key, bot_tag, tg_admin_id = None, dev_mode = None):
        self.token          = token
        self.ya_usr_id      = ya_usr_id
        self.tg_key         = tg_key
        self.bot_tag        = bot_tag
        self.tg_admin_id    = tg_admin_id
        self.dev_mode       = dev_mode
        
    def print_prefs(self):
        print(self.token, self.ya_usr_id, self.tg_key, self.bot_tag, self.tg_admin_id, self.dev_mode)
        
    def get_mode(self):
        return self.dev_mode