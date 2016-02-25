import server

pwd = raw_input("Password :")
res = server.get_password(pwd)
print "Result :", res
