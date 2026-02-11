from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = "groups"
    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    cfg: Mapped[list["Configuration"]] = relationship(back_populates='grp', uselist=True, secondary="cfg_group")
    quest: Mapped[list["Question"]] = relationship(back_populates='categ', uselist=True)

class Question(Base):
    __tablename__ = "questions"

    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    idname: Mapped[int] = mapped_column(ForeignKey('groups.tid', ondelete='CASCADE'))
    body: Mapped[str] = mapped_column(String(150))
    difflvl: Mapped[int] = mapped_column(index=True)

    categ: Mapped["Group"] = relationship(back_populates='quest', uselist=False)


    def __repr__(self):
        return super().__repr__()
    
class CfgGroup(Base):
    __tablename__ = 'cfg_group'
    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    cfg_fk: Mapped[int] = mapped_column(ForeignKey('configurations.tid'))
    group_fk: Mapped[int] = mapped_column(ForeignKey('difficults.tid'))

class Configuration(Base):
    __tablename__ = "configurations"
    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    grp: Mapped[list["Group"]] = relationship(back_populates='cfg', uselist=True, secondary="cfg_group")
    # diffa: Mapped[list["Difficult"]] = relationship(back_populates='cfgarr', uselist=True)

class Difficult(Base):
    __tablename__ = "difficults"
    tid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    cfgarr: Mapped[int] = mapped_column(ForeignKey("configurations.tid"))
    # grp: Mapped[list["Configuration"]] = relationship(back_populates='diffarr', uselist=True)

