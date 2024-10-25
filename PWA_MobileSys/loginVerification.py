class loginVerify():

    def verifyUser(db, input_username, input_password):
        # variables
        matched_username = False
        matched_password = False

        collection = db.User_Logins

        x = collection.distinct("username")
        for usernames in x:
            print(str(usernames) + " " + str(input_username))
            if str(input_username) == str(usernames):
                matched_username = True
        
        y = collection.distinct("password")
        for passwords in y:
            print(passwords + " " + input_password)
            if str(input_password) == str(passwords):
                matched_password = True

        if matched_username and matched_password:
            print("returned true")
            return True
        else:
            print("returned false")
            return False