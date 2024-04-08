""" Database schema """
from datetime import datetime, timezone
from flask_login import UserMixin, AnonymousUserMixin
from uuid import uuid4
from levelUP import db


class User(db.Model, UserMixin, AnonymousUserMixin):
    """ Database table: user
        each user account setting/properties defined here.

        #Attribute:
            uname -> username (unique),\n
            fname -> firstname, \n
            alias -> alias (not null),\n
            password -> password, \n
        """
    __tablename__ = "user"
    userID = db.Column(db.String(), unique=True, primary_key=True)
    uname = db.Column(db.String(26), unique=True)  # username
    fname = db.Column(db.String(56))  # firstname
    alias = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String())
    dnaID = db.Column(db.String(), default=str(uuid4()), unique=True)
    createdAt = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __str__(self):
        return self.uname

    def get_id(self):
        return (self.userID)

    # @property
    # def isMe(self) -> bool:
    #     if not current_user.is_authenticated:
    #         # return current_app.login_manager.unauthorized()
    #         return False
    #     elif current_user.is_authenticated and (current_user.uname == 'luke'):
    #         return True
    #     return False

    # Should be implemented with cookie or session instead
    # def setLang(self, lang:str="EN"): # "TH" || "EN"
    #     if (lang != "EN" or lang != "TH"):
    #         self.fname = "EN"
    #     self.langPref = lang

    # @property
    # def getLangPref(self):
    #     return self.langPref
