
import pickle
import os
os.chdir('/home/pi/Desktop/Jakrota/')
pickle_in = open('Auth_mail_id.pickle', 'rb+')
mail_dict = pickle.load(pickle_in)


c = input("TO ADD OR EDIT, PRESS A OR TO DELETE, PRESS D: ")
k = input("ENTER THE WING AND FLAT NUMBER (eg. A201):")
if c.upper() == "A" :
    v = input("ENTER THE NEW MAIL ID:") 
    mail_dict[k] = mail_dict.get(k,v)
if c.upper() == "D":
    mail_dict.pop(k)
print(mail_dict)

AMid_file = open('Auth_mail_id.pickle', 'wb')
pickle.dump(mail_dict, AMid_file)
AMid_file.close()
  
#print("Something went wrong")
