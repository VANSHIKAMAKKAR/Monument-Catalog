from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Places, Base, PopularLocations, User

engine = create_engine('sqlite:///itemcatalogappwithlogin.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

place1 = Places(id =0 , name="Agra")

TajMahal=PopularLocations(name="Taj Mahal",description="Come, Walk along the pathway beside the reflecting pool with fountains upto the mausoleum crafted in soft & pure marble and jewelled with semi precious stones, where in the serenity of paradise rests the Queen in peace with her King. Come to unfold the pages from the past to churn the charm out of its mystique and enrich your imagination about this marvel of an epic in stone, The Taj!" ,year =1631 ,founder="Shah Jahan",places_id=0, places = place1)
session.add(TajMahal)
session.commit()
# Locations for Agra
agrafort=PopularLocations(name="Agra Fort",description="The Agra Fort, also known as the Lal Qila, Fort Rouge or Qila-i-Akbari, is the highlight of the city of Agra, then capital of the Mughal Sultanate . A symbol of power, strength and resilience, as it stands today in full glory." ,year =1575 ,founder="Akbar",places_id=0, places = place1)
session.add(agrafort)
session.commit()


# Locations for Jaipur
place2 = Places(id=1 ,name="Jaipur")

session.add(place2)
session.commit()


location1 = PopularLocations(name="Hawa Mahal",description="Hawa Mahal (English translation Palace of Winds or Palace of the Breeze) is a palace in Jaipur, India. It is constructed of red and pink sandstone. The palace sits on the edge of the City Palace, Jaipur, and extends to the zenana, or women's chambers.",year=1799,founder=" Maharaja Sawai Pratap Singh",places_id=1, places= place2)
session.add(location1)
session.commit()

location2 = PopularLocations(name="Amber Palace", description="This magnificent fort comprises an extensive palace complex, built from pale yellow and pink sandstone, and white marble, and is divided into four main sections, each with its own courtyard. It is possible to visit the fortress on elephant-back, but animal welfare groups have criticised the keeping of elephants at Amber because of reports of abuse, and because carrying passengers can cause lasting injuries to the animals.",year=1614, founder="Meenas",places_id=1, places =place2)
session.add(location2)
session.commit()


# Locations for Manali
place3 = Places(id = 2, name="Manali")
session.add(place3)
session.commit()


location3 = PopularLocations(name="Hidimba Devi Temple", description="Hidimba Devi Temple, locally known as Dhungari Temple, also known variously as the Hadimba Temple, is located in Manali. It is an ancient cave temple dedicated to Hidimbi Devi, wife of Bhima, a figure in the Indian epic Mahabharata. The sanctuary is built over a huge rock jutting out of the ground which was worshiped as an image of the deity." ,year=1553 ,founder ="Maharaja Bahadur Singh",places_id=2,places = place3)
session.add(location3)
session.commit()

location4 = PopularLocations(name="Manu Temple", description="This magnificent temple is dedicated to the sage Manu, who is said to be the creator of the world and the writer of Manusmriti. The Manu Temple is located in old Manali, at a distance of three kilometers from the main market. Though this area is quite congested, the presence of the River Beas adds to its attraction. The temple is one of the prime attractions in Manali and is believed to be the same place where sage Manu meditated after stepping on earth. This place has a distinct historical background that appeals to most of the people who visit Manali. The popularity of this majestic temple lies in the fact that it is the only temple dedicated to Manu." ,year="1992",founder="Manusmriti",places_id=2, places = place3)
session.add(location4)
session.commit()



print "added locations!"