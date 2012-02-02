from inkle.models import *
import shutil

def load_members():
    m = Member(first_name = "Jacob", last_name = "Wenger", username = "jwenger@nd.edu", email = "jwenger@nd.edu", birthday = datetime.date(day = 20, month = 5, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Chad", last_name = "Heise", username = "cheise@nd.edu", email = "cheise@nd.edu", birthday = datetime.date(day = 14, month = 1, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Jane", last_name = "Obringer", username = "jobring2@nd.edu", email = "jobring2@nd.edu", birthday = datetime.date(day = 7, month = 7, year = 1990), gender = "Female", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "David", last_name = "Ulery", username = "dulery@nd.edu", email = "dulery@nd.edu", birthday = datetime.date(day = 3, month = 8, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Andy", last_name = "Schroeder", username = "aschroeder@nd.edu", email = "aschroeder@nd.edu", birthday = datetime.date(day = 23, month = 8, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Nick", last_name = "Galvez", username = "ngalvez@nd.edu", email = "ngalvez@nd.edu", birthday = datetime.date(day = 23, month = 12, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Matt", last_name = "Roe", username = "mroe@nd.edu", email = "mroe@nd.edu", birthday = datetime.date(day = 10, month = 10, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Chrissy", last_name = "Grant", username = "cgrant@nd.edu", email = "cgrant@nd.edu", birthday = datetime.date(day = 28, month = 2, year = 1990), gender = "Female", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Brian", last_name = "Greaney", username = "bgreaney@nd.edu", email = "bgreaney@nd.edu", birthday = datetime.date(day = 22, month = 11, year = 1989), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Mason", last_name = "Roberts", username = "mroberts@nd.edu", email = "mroberts@nd.edu", birthday = datetime.date(day = 30, month = 10, year = 1989), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "John", last_name = "Goedert", username = "jgoedert@nd.edu", email = "jgoedert@nd.edu", birthday = datetime.date(day = 3, month = 3, year = 1990), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "John", last_name = "Johnson", username = "jjohnson@nd.edu", email = "jjohnson@nd.edu", birthday = datetime.date(day = 4, month = 4, year = 1970), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Johnny", last_name = "Walker", username = "jwalker@nd.edu", email = "jwalker@nd.edu", birthday = datetime.date(day = 10, month = 4, year = 1984), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "John", last_name = "Kennedy", username = "jkennedy@nd.edu", email = "jkennedy@nd.edu", birthday = datetime.date(day = 3, month = 10, year = 1956), gender = "Male", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/man.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Danielle", last_name = "Duva", username = "dduva@nd.edu", email = "dduva@nd.edu", birthday = datetime.date(day = 5, month = 4, year = 1990), gender = "Female", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/woman.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")

    m = Member(first_name = "Megan", last_name = "Martis", username = "mmartis@nd.edu", email = "mmartis@nd.edu", birthday = datetime.date(day = 2, month = 7, year = 1956), gender = "Female", verified = True)
    m.set_password("password")
    m.update_verification_hash()
    m.save()
    shutil.copyfile("inkle/static/media/images/main/woman.jpg", "inkle/static/media/images/members/" + str(m.id) + ".jpg")


def load_dorms():
    l = Location.objects.create(name = "Alumni Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")

    l = Location.objects.create(name = "Badin Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Breen Phillips Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Carroll Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Cavanaugh Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Dillon Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Duncan Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Farley Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Fisher Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Howard Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Keenan Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Keough Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Knott Hall", category = "Dorm", street = "Mod Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Lewis Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Lyons Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "McGlinn Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Morrissey Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "O'Neill Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Pangborn Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Pasquerilla East Hall", category = "Dorm", street = "Mod Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")

    l = Location.objects.create(name = "Pasquerilla West Hall", category = "Dorm", street = "Mod Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Ryan Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "St. Edward's Hall", category = "Dorm", street = "South Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Siegfried Hall", category = "Dorm", street = "Mod Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Sorin Hall", category = "Dorm", street = "Main Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Stanford Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Walsh Hall", category = "Dorm", street = "Main Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l =Location.objects.create(name = "Welsh Family Hall", category = "Dorm", street = "West Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Zahm Hall", category = "Dorm", street = "North Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")


def load_spheres():
    s = Sphere.objects.create(name = "University of Notre Dame")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")

    s = Sphere.objects.create(name = "University of Notre Dame - Class of 2012")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")

    s = Sphere.objects.create(name = "University of Notre Dame - Class of 2013")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")

    s = Sphere.objects.create(name = "University of Notre Dame - Class of 2014")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")

    s = Sphere.objects.create(name = "University of Notre Dame - Class of 2015")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")

    s = Sphere.objects.create(name = "South Bend - Mishawaka")
    shutil.copyfile("inkle/static/media/images/main/sphere.jpg", "inkle/static/media/images/spheres/" + str(s.id) + ".jpg")


def load_campus_locations():
    l = Location.objects.create(name = "LaFortune Student Center", category = "Other", street = "Main Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
    
    l = Location.objects.create(name = "Joyce Athletic and Convocation Center (JACC)", category = "Arena", street = "Main Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")

    l = Location.objects.create(name = "Notre Dame Stadium", category = "Arena", street = "Main Quad", city = "Notre Dame", state = "IN", zip_code = "46556", phone = "", website = "")
    shutil.copyfile("inkle/static/media/images/main/location.jpg", "inkle/static/media/images/locations/" + str(l.id) + ".jpg")
