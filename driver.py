from User import User

if __name__ == "__main__":
    # usr = User.newUser("tongliu18", '1234')
    # print(User.usr_pswd.getSerial(("tongliu18", "1234")))
    # usr = User.newUser("tongliu18", '1234')
    # print(User.usr_pswd.hasUser(("tongliu18", "1234")))
    # x = User.fromLogin("tongliu18", "1234")
    # print("loaded:", x is not None)
    # print(x, x.__dict__)
    # print(x.username)
    # print(x.password)


    User.usr_pswd.usr_pswd = {("tongliu18", "1234"): 1}
    User.usr_pswd.addUser("t0","t0", 0)

    u = User.mangoLoad(1)
    print(u)
    print(u.id)
    print(u.__dict__)