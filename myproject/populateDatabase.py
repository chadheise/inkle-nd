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


def load_spheres():
    for line in open("databaseData/spheres.txt", "r"):
        data = [x.strip() for x in line.split("|")]
        s = Sphere.objects.create(name = data[0])
        shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")


def populate_dev_database():
    load_members()
    load_dorms()
    load_campus_locations()
    load_spheres()


def populate_prod_database():
    load_dorms()
    load_campus_locations()
    load_spheres()