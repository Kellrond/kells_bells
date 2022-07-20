

class Home:
    def __init__(self, ui, h, w) -> None:
        self.height = h
        self.width  = w
        self.ui     = ui 

    def draw(self):
        self.line_list = [
            'Email admin',
            '',
            'Select a menu from the left by typing the name',
            '',
            'Users:  Each user represents an email address',
            ' - list users',
            ' - add/remove users',
            ' - edit user',
            ' - update user password',
            '',
            'Aliases:  Forwards emails from foo@bar.com to bar@foo.com etc.',
            ' - list aliases',
            ' - add/remove alias',
            ' - edit alias',
            '',
            'Domains:  The domains which are hosted on this mail server eg foo.com, bar.com',
            ' - list domains',
            ' - add/remove domain',
            ' - edit domain',
        ]
        return self.line_list


class Users:
    def __init__(self, ui, h, w) -> None:
        self.height = h
        self.width  = w
        self.ui     = ui 

    def draw(self):
        self.line_list = [
            'Email users',
            '',

        ]
        return self.line_list

class Aliases:
    def __init__(self, ui, h, w) -> None:
        self.height = h
        self.width  = w
        self.ui     = ui 

    def draw(self):
        self.line_list = [
            'Email aliases',
            '',

        ]
        return self.line_list

class Domains:
    def __init__(self, ui, h, w) -> None:
        self.height = h
        self.width  = w
        self.ui     = ui 

    def draw(self):
        self.line_list = [
            'Email domains',
            '',

        ]
        return self.line_list