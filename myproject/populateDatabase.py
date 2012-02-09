from inkle.models import *
import shutil

def load_members():
    for line in open("databaseData/members.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        m = Member(first_name = data[0], last_name = data[1], username = data[2], email = data[3], birthday = datetime.date(day = int(data[4]), month = int(data[5]), year = int(data[6])), gender = data[7], verified = data[8], is_staff = data[9])
        m.set_password("password")
        m.update_verification_hash()
        m.save()
        if (data[7] == "Male"):
            shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")
        else:
            shutil.copyfile("inkle/static/media/images/main/woman.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")


def load_member_followings():
    for line in open("databaseData/memberFollowings.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        if (data[0] != data[1]):
            from_member = Member.objects.get(pk = data[0])
            to_member = Member.objects.get(pk = data[1])
    
            from_member.accepted.add(to_member)
            from_member.following.add(to_member)
            to_member.followers.add(from_member)


def load_member_networks():
    for line in open("databaseData/memberNetworks.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        member = Member.objects.get(pk = data[0])
        network = Network.objects.get(pk = data[1])
    
        member.networks.add(network)


def load_locations(filename):
    for line in open(filename, "r"):
        data = [x.strip() for x in line.split("|")]
        if (len(data) != 8):
            print data
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


def load_miscellaneous():
    load_locations("databaseData/miscellaneous.txt")


def load_networks():
    for line in open("databaseData/networks.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        s = Network.objects.create(name = data[0])
        shutil.copyfile("inkle/static/media/images/main/network.jpg", "inkle/static/media/images/networks/" + str(s.id) + ".jpg")


def populate_dev_database():
    load_members()
    load_member_followings()
    load_bars()
    load_clubs()
    load_restaurants()
    load_apartments()
    load_miscellaneous()
    load_dorms()
    load_campus_locations()
    load_networks()
    load_member_networks()


def populate_prod_database():
    load_restaurants()
    load_bars()
    load_clubs()
    load_apartments()
    load_miscellaneous()
    load_dorms()
    load_campus_locations()
    load_networks()
