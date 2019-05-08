# import modules
from database_setup import Base, User, Item, Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://item_catalog:item_catalog@localhost/item_catalog')

# creating a session
Session = sessionmaker(bind=engine)

session = Session()

# populating the database
User1 = User(name="aditya sabu",
             email="adi.sabu@outlook.com",
             picture="https://goo.gl/images/7VkS1H")

session.add(User1)
session.commit()


User2 = User(name="sanatsathay",
             email="sunny.shine@outlook.com",
             picture="https://goo.gl/images/RiEUwr")

session.add(User2)
session.commit()


User3 = User(name="gaydeokar",
             email="pj.g@gmail.com",
             picture="https://goo.gl/images/eFydrm")

session.add(User3)
session.commit()


User4 = User(name="doctor rudy",
             email="dr.rudraprabh@yahoo.com",
             picture="https://goo.gl/images/Bz47ZM")

session.add(User4)
session.commit()


User5 = User(name="NIKHIL VARMA",
             email="gotiscratch.nihksiminaj@gmail.com",
             picture="https://goo.gl/images/253D4q")

session.add(User5)
session.commit()


Category1 = Category(
            name="Winterfell",
            user=User2)

session.add(Category1)
session.commit()


Category2 = Category(
            name="King's Landing",
            user=User4)

session.add(Category2)
session.commit()


Category3 = Category(
            name="Pyke",
            user=User1)

session.add(Category3)
session.commit()


Category4 = Category(
            name="Dragonstone",
            user=User5)

session.add(Category4)
session.commit()


Category5 = Category(
            name="The WALL",
            user=User3)

session.add(Category5)
session.commit()


Item1 = Item(name="Ned Stark",
             description='''In A Game of Thrones, Ned Stark is
             introduced as the virtuous and honorable patriarch
             of House Stark and the father of six children. The
             moral compass of the story, he is content to remain
             far from courtly intrigues and is unwavering in his
             view of loyalty and honor.His family name, Stark,
             serves as an indication of his resistance to moral
             compromise, but his boundaries are increasingly
             tested over the course of the novel.Finding himself
             a key player in the escalating political intrigue of
             King's Landing, Ned struggles as his own sense of honor
             draws him into corrupt goings-on at court.As the story
             progresses, he begins to see the importance of moral
             and practical compromises to achieve a just end,
             and is ultimately forced to choose between the safety
             of his family and doing what is right.''',
             picture="https://images.app.goo.gl/HRtCNhhYnh9QNXgQ8",
             category_id=1,
             user_id=2)

session.add(Item1)
session.commit()


Item2 = Item(name="Jaime Lannister",
             description='''Introduced in A Game of Thrones, Jaime
             is a knight of the Kingsguard and a member of House
             Lannister, one of the wealthiest and most powerful
             families in the fictional kingdom of Westeros.
             Although he first appears to be unscrupulous and
             immoral, he later proves to be far more complex,
             honorable and sympathetic.''',
             picture="https://images.app.goo.gl/PKccABuE5QQZmM8b6",
             category_id=2,
             user_id=4)

session.add(Item2)
session.commit()


Item3 = Item(name="Theon Greyjoy",
             description='''Ten years before the events of The game
             of thrones, Theon was taken hostage by Eddard Stark.He
             would have been executed had his father Balon displeased
             King Robert Baratheon. Theon was raised at Winterfell
             with the Stark children and developed a close friendship
             with Robb Stark. As an adult, Theon was arrogant, cocky,
             and proud until being imprisoned by Ramsay Snow, who is
             the eldest and bastard son of Roose Bolton. During the
             imprisonment, Ramsay severely tortured Theon physically
             and psychologically before emasculating him and mockingly
             changing his name to "Reek".''',
             picture="https://images.app.goo.gl/55G7JK3HvmwoD3Vx7",
             category_id=3,
             user_id=1)

session.add(Item3)
session.commit()


Item4 = Item(name="Daenerys Targaryen",
             description='''In A Game of Thrones, Daenerys is sold
             off by her brother Viserys and Illyrio Mopatis to marry
             Khal Drogo, a Dothraki warlord, in exchange for an army
             for Viserys.Shortly thereafter, Drogo is wounded in a
             fight, and the cut festers. With Drogo ill, his warriors
             mutiny and abandon him. In desperation, Daenerys recruits
             an enslaved Lhazareen priestess, Mirri Maz Duur, to save
             Drogo with blood magic. However, despite being saved by
             Daenerys from being raped by the tribe's warriors, the
             priestess betrays her trust, and the magic ritual leads
             to Daenerys' unborn child being stillborn and leaves Drogo
             in a catatonic state. Daenerys does not want her husband
             to suffer any longer and euthanizes him with a pillow. She
             burns the priestess in Drogo's funeral pyre and climbs into
             the flame with her three dragon eggs. When the pyre dies out
             the following morning, Daenerys emerges alive and unburnt from
             the ashes with three hatched dragons.''',
             picture="https://images.app.goo.gl/aAebFQ8DVY6uouJX6",
             category_id=4,
             user_id=5)

session.add(Item4)
session.commit()


Item5 = Item(name="Jon Snow",
             description='''Jon Snow is first introduced in A Game of Thrones,
              as he and his five siblings adopt six orphaned direwolf cubs.
              Known by all as Ned Stark's illegitimate son and with Ned's
              wife Catelyn despising him, Jon has always felt removed from
              the rest of the Stark family. He resolves to join the Night's
              Watch, as his status as a bastard prevents him from holding
              lands or marrying into a good family. At The Wall, the other
              recruits resent Jon's aura of superiority, but he makes amends
              by helping them master swordplay. He also befriends Samwell
              Tarly,a cowardly lordling who,despite being helpless with weapons
              displays an aptitude for book learning. Jon's independence and
              his compassion for the recruits invite the ire of the harsh
              master-at-arms Alliser Thorne, who sees Jon as a threat to his
              authority. Jon gains the notice of the Lord Commander, Jeor
              Mormont, who names Jon his personal squire and grooms Jon for
              command. After learning of his father's execution, Jon resolves
              to desert the Night's Watch and join his half brother Robb, but
              the other recruits convince Jon to remain loyal to his Night's
              Watch vows. The next night, Jon saves Mormont's life by killing
              an undead wight. Mormont then orders a Great Ranging beyond the
              Wall to learn more of this new threat.The season 7 finale episode
              "The Dragon and the Wolf" confirmed that Jon is indeed the
              legitimate son of Rhaegar and Lyanna, and that his birth name
              is actually Aegon Targaryen''',
             picture="https://images.app.goo.gl/X6mnXmjUC5a9NWUK6",
             category_id=5,
             user_id=3)

session.add(Item5)
session.commit()
