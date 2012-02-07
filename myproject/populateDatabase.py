from inkle.models import *
import shutil

def load_members():
    for line in open("databaseData/members.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        m = Member(first_name = data[0], last_name = data[1], username = data[2], email = data[3], birthday = datetime.date(day = int(data[4]), month = int(data[5]), year = int(data[6])), gender = data[7], verified = data[8])
        m.set_password("password")
        m.update_verification_hash()
        m.save()
        if (data[7] == "Male"):
            shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")
        else:
            shutil.copyfile("inkle/static/media/images/main/woman.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")


def load_following(from_member_id, to_member_id):
    if (from_member_id != to_member_id):
        try:
            from_member = Member.objects.get(pk = from_member_id)
            to_member = Member.objects.get(pk = to_member_id)
    
            from_member.accepted.add(to_member)
            from_member.following.add(to_member)
            to_member.followers.add(from_member)
        except Member.DoesNotExist:
            return


def load_followings():
    load_following(1, 2)
    load_following(1, 3)
    load_following(1, 4)
    load_following(1, 5)
    load_following(1, 6)
    load_following(1, 7)
    load_following(1, 8)
    load_following(1, 9)
    load_following(1, 10)

    load_following(2, 1)
    load_following(2, 3)
    load_following(2, 5)
    load_following(2, 7)
    load_following(2, 9)
    load_following(2, 11)
    load_following(2, 13)
    load_following(2, 15)
    load_following(2, 16)


def load_locations(filename):
    for line in open(filename, "r"):
        data = [x.strip() for x in line.split("|")]
        l = Location.objects.create(name = data[0], category = data[1], street = data[2], city = data[3], state = data[4], zip_code = data[5], phone = data[6], website = data[7])
        shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")


def load_dorms():
    load_locations("databaseData/notreDameDorms.txt")
    load_locations("databaseData/saintMarysDorms.txt")
    load_locations("databaseData/holyCrossDorms.txt")


def load_campus_locations():
    load_locations("databaseData/notreDameCampusLocations.txt")
    load_locations("databaseData/saintMarysCampusLocations.txt")
    load_locations("databaseData/holyCrossCampusLocations.txt")

def load_bars():
    load_locations("databaseData/bars.txt")

def load_clubs():
    load_locations("databaseData/clubs.txt")

def load_restaurants():
    load_locations("databaseData/restaurants.txt")

def load_apartments():
    load_locations("databaseData/apartments.txt")

def load_networks():
    for line in open("databaseData/networks.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        s = Network.objects.create(name = data[0])
        shutil.copyfile("inkle/static/media/images/main/network.jpg", "inkle/static/media/images/networks/" + str(s.id) + ".jpg")


def populate_dev_database():
    load_members()
    load_followings()
    load_bars()
    load_clubs()
    load_restaurants()
    load_apartments()
    load_dorms()
    load_campus_locations()
    load_networks()


def populate_prod_database():
    load_restaurants()
    load_bars()
    load_clubs()
    load_apartments()
    load_dorms()
    load_campus_locations()
    load_networks()
