from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()
db = SQLAlchemy(model_class=Base)


class Account(db.Model):
    __tablename__ = "riot_accounts"

    riot_puu_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    game_name: Mapped[str] = mapped_column(db.String(17))
    tag_line: Mapped[str] = mapped_column(db.String(6))
    summoner_level: Mapped[int] = mapped_column(db.Integer)
    profile_icon: Mapped[int] = mapped_column(db.Integer)

    def __repr__(self):
        return (f"Account(riot_puu_id:{self.riot_puu_id},"
                f"game_name:{self.game_name}), tag_line:{self.tag_line},"
                f"summoner_level:{self.summoner_level},"
                f"profile_icon:{self.profile_icon})")
