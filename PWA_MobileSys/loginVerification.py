class loginVerify():

    def verifyUser(db, input_username, input_password):
        # variables
        matched_username = False
        matched_password = False

        # get an instance of the collection
        collection = db.User_Logins

        # check if usernames match
        x = collection.distinct("username")
        for usernames in x:
            if str(input_username) == str(usernames):
                matched_username = True
        
        #check if passwords match
        y = collection.distinct("password")
        for passwords in y:
            if str(input_password) == str(passwords):
                matched_password = True

        if matched_username and matched_password:
            # if match is found
            return True
        else:
            # if no match is found
            return False