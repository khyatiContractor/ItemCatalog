from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('sqlite:///catalogcatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", 
             email="tinnyTim@udacity.com",
             picture="")
session.add(User1)
session.commit()

# catalog for SanowBoarding
catalog1 = Catalog(user_id=1, name="Sanowboarding")
session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Snowboard", description="A flat profile lends stability, balance and edge control; the tip and tail kick up with an early rise outside your feet. Symmetrical shaping lets you jib, spin, stomp and butter with freestyle mobility, whether you're riding regular or switch. FSC-Certified wood core is lightweight and loaded with pop; stiffer zones are positioned outside your feet and enable a smooth flex between your bindings. Wood grains are positioned along the toe and heel edges in 2 continuous zones, providing consistent edge hold and added strength",
                     price="$200.99", catalog=catalog1)
session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Googles", description="Full-perimeter channel venting circulates air and reduces fogging. Sleek, low-profile strap outriggers hinge to create a flush fit that minimizes gaps and comfortably distributes pressure evenly across the face. 3-layer face foam is constructed of a dense base, a plush mid layer and a soft fleece top layer; design ensures a tight seal, good moisture management and maximum comfort",
                     price="$70.50", catalog=catalog1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Boots", description="Insulated Imprint 2 liners with Lock-Up cuffs, hook-and-loop closures and Man Fur provide warmth even when wet. DynoGRIP outsoles with B3 gel in the heels and rubber toe/heel reinforcements offer effective cushioning. GripLITE backstays and 1:1 medium-flex PowerUP tongues ensure consistent flex and response. Total Comfort construction, snow-proof internal gussets and Level 1 molded EVA footbeds deliver sweet comfort with a broken-in feel right out of the box",
                     price="$150.50", catalog=catalog1)
session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Helmets", description="Lightweight in-mold construction and an adjustable Dial Fit System (DFS2) deliver protection and a personalized fit. While most helmets protect only against direct impact, MIPS technology reduces rotational forces when the helmet gets hit at an angle AirEvac technology lets air flow to pull warm, fog-causing air out of your goggles; warm air exhausts out the top of your goggles to flow through the helmet's AirEvac system",
                     price="$50.99", catalog=catalog1)
session.add(catalogItem4)
session.commit()




# catalog for Rock Climbing
catalog2 = Catalog(user_id=1, name="Rock Climbing")
session.add(catalog2)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Shoes ", description="Unlined leather offers the maximum amount of comfort and ensures the shoes will mold to your feet. Synthetic overlay and lace closure system guarantees fit and performance for the gym and outside on the rock",
                     price="$70.99", catalog=catalog2)
session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Ropes",
                     description=" Since leftover yarns cannot be planned in advance, each batch is different than the last giving you a rope that is one of a kind. Thermo Shield treatment employs a heat process to stabilize individual yarns, ensuring the rope stays supple throughout its working lifetime. Kernmantle design features a stretchy core protected by a durable outer sheath which combine for strength and good handling", 
                     price="$125", catalog=catalog2)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Chalk Bags", description="Blend of tough nylon fabrics endures regular encounters with rock; polyester fleece-lined interior helps contain chalk. Loop on side stows a brush for cleaning holds (brush not included). External zippered pocket stows small essentials, such as tape or a knife. Integrated bottle opener helps you unwind after a hard day of climbing. Drawstring with cordlock closes chalk bag when not in use ",
                     price="35", catalog=catalog2)
session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Harnesses ", description="Momentum features 4 gear loops, trakFit-adjustable leg loops and an ultra-comfortable waistbelt. Pre-threaded Speed Adjust waistbelt buckle. Bullhorn-shaped waistbelt built using Dual Core Construction.Patent-pending trakFit adjustment allows easy leg-loop customization. Adjustable rear elastic riser. 4 pressure-molded gear loops",
                     price="32", catalog=catalog2)
session.add(catalogItem4)
session.commit()



# catalog for Panda Garden
catalog3 = Catalog(user_id=1, name="Cycle")
session.add(catalog3)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Bikes", description="Aluminum alloy frame offers exceptional stiffness, durability and smoothness, striking a balance between race-level quickness and confidence-inspiring stability. Shimano Altus drivetrain deftly moves through the 18 gears for smooth shifting. Hydraulic disc brakes offer superb speed management. Small frame sizes have 27.5 in. tires; Medium, Large and Extra-Large frames have 29 in. tires. Specs are subject to change",
                     price="$500", catalog=catalog3)
session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Cycling shoes", description="ompatible with single-release SPD cleats (note: SPD cleats are necessary to connect to a bike and are sold separately). Recessed plate makes walking on floors easier. Adjustable hook-and-loop straps offer midfoot support. Synthetic, no-sew overlays offer support from start to finish",
                     price="$126.99",  catalog=catalog3)
session.add(catalogItem2)
session.commit()



# catalog for Thyme for that
catalog4 = Catalog(user_id=1, name="Yoga")
session.add(catalog4)
session.commit()


catalogItem1 = CatalogItem(user_id=1, name="Mats", description="Slip-resistant fabriclike top surface does not get sticky, even when wet with perspiration. High-density, closed-cell foam provides cushion on all surfaces; closed-cell foam does not absorb moisture. Dot pattern on the bottom keeps the mat from sliding on many different surfaces. Mat rolls up compactly for easy transportation",
                     price="$82.99",  catalog=catalog4)
session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Props", description="Made from 50 - 75% recycled post-industrial and post-consumer EVA foam; firm foam has a grippy feel. Use the block to support back bends or place it under your hands in standing poses. Edges are rounded for comfort",
                     price="$15.99",  catalog=catalog4)
session.add(catalogItem2)
session.commit()



print "added catalog items!"