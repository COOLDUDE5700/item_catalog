#import modules
from database_setup import Base, User, Item, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///item_catalog.db')

#creating a session
Session = sessionmaker(bind=engine)

session = Session()

#populating the database
User1 = User( name = "aditya sabu",
             email = "adi.sabu@outlook.com",
             picture = "https://goo.gl/images/7VkS1H")

session.add(User1)
session.commit()


User2 = User(name = "sanatsathay",
             email = "sunny.shine@outlook.com",
             picture = "https://goo.gl/images/RiEUwr")

session.add(User2)
session.commit()


User3 = User(name = "gaydeokar",
             email = "pj.g@gmail.com",
             picture = "https://goo.gl/images/eFydrm")

session.add(User3)
session.commit()


User4 = User(name = "doctor rudy",
             email = "dr.rudraprabh@yahoo.com",
             picture = "https://goo.gl/images/Bz47ZM")

session.add(User4)
session.commit()


User5 = User(name = "NIKHIL VARMA",
             email = "gotiscratch.nihksiminaj@gmail.com",
             picture = "https://goo.gl/images/253D4q")

session.add(User5)
session.commit()


Category1 = Category(
            name = "cricket",
            user_id = 2)

session.add(Category1)
session.commit()


Category2 = Category(
            name = "Tennis",
            user_id = 4)

session.add(Category2)
session.commit()


Category3 = Category(
            name = "hockey",
            user_id = 1)

session.add(Category3)
session.commit()


Category4 = Category(
            name = "table tennis",
            user_id = 5)

session.add(Category4)
session.commit()


Category5 = Category(
            name = "soccer",
            user_id = 3)

session.add(Category5)
session.commit()


Item1 = Item(name="cricket bat",
             description="magical wooden bat can smash any ball out of the park",
             picture="https://goo.gl/images/NaHV6k",
             category_id=3,
             user_id=2)

session.add(Item1)
session.commit()


Item2 = Item(name="tennis racket",
             description="this racket will win you any rally",
             picture="https://goo.gl/images/YnJHQQ",
             category_id=5,
             user_id=4)

session.add(Item2)
session.commit()


Item3 = Item(name="hockey stick",
             description="easy to score a goal and beat someone up",
             picture="https://goo.gl/images/y311AF",
             category_id=4,
             user_id=5)

session.add(Item3)
session.commit()


Item4 = Item(name="table tennis ball",
             description="usually gets smashed between two rackets",
             picture="https://goo.gl/images/PjH8zz",
             category_id=2,
             user_id=3)

session.add(Item4)
session.commit()


Item5 = Item(name="goalkeeper helmet",
             description="to save youself from a hit and might be used to hide your identity",
             picture="https://goo.gl/images/LZaCFF",
             category_id=1,
             user_id=2)

session.add(Item5)
session.commit()
