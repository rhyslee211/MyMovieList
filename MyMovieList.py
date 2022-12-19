import getpass
from os.path import exists
import http.client
import requests

username = ""
password = ""

def getUser():
    global username 
    tempUsername = input("Username:")

    if(exists(tempUsername + ".txt")):
        testPassword(tempUsername)        

    else:
        yesNo = input("Username not found \nCreate new account?")
        
        if(yesNo.lower() == "yes"):
            newPass = input("Create Password:")
            userfile = open(tempUsername + ".txt", "w")
            userfile.write(newPass)
            userfile.close()
            username = tempUsername
        elif(yesNo.lower() == "no"):
            print("Returning you to main page")
            main()
    main()

def testPassword(tempUsername):
    global username 
    password = getpass.getpass("Password:").strip()
    userfile = open(tempUsername + ".txt")
    filePass = userfile.readline().strip()


    if(password == filePass):
        print("Logged in!")
        username = tempUsername
    else:
        yesNo = input("Incorrect password! \nTry a different password?")
        
        if(yesNo.lower == "yes"):
            testPassword(tempUsername)
        elif(yesNo.lower == "no"):
            main()
        else:
            print("Unknown command; Returning to Main Screen")
            initialScreen()

def rateMovie():
    movieName = input("Movie Name: ")
    movieScore = input("Movie Score(Out of 10): ")
    while(int(movieScore) < 1 or int(movieScore) > 10):
        movieScore = input("Please Score the movie between 1 and 10")
    movieReview = input("Write a small review(Optional): ")

    movieDict  = {
        "Name": movieName,
        "Score": movieScore + "/10",
        "Review": movieReview
    }

    reviewFile = open(username + "reviews.txt", "a")
    for key, value in movieDict.items(): 
        reviewFile.write('%s:%s\n' % (key, value))
    reviewFile.close()
    main()


def myReviews():

    if(exists(username + "reviews.txt")):
        reviewFile = open(username + "reviews.txt")
        reviewsList = reviewFile.readlines()

        for i in reviewsList:
            i = i[0:i.__len__()-1]
            if(i[0:6] == "Review"):
                print(i+"\n")
            else:
                print(i)

        reviewFile.close()
    else:
        print("You do not have any movie reviews yet")
    main()

def searchMyReviews():
    
    searchedMovie = input("Enter movie title: ").strip()

    reviewFile = open(username + "reviews.txt")
    moviesList = reviewFile.readlines()

    notinList = True

    for i in moviesList:
        if(i == "Name:" + searchedMovie + "\n"):
            index = moviesList.index("Name:" + searchedMovie + "\n")
            print(moviesList[index] + moviesList[index + 1] + moviesList[index + 2])
            notinList = False
    if(notinList):
        print("Movie not found in records")

    main()

def searchOthersReviews():

    searchedUser = input("Enter username: ").strip()

    if(exists(searchedUser + "reviews.txt")):
    
        searchedMovie = input("Enter movie title: ").strip()

        reviewFile = open(searchedUser + "reviews.txt")
        moviesList = reviewFile.readlines()

        notinList = True

        for i in moviesList:
            if(i == "Name:" + searchedMovie + "\n"):
                index = moviesList.index("Name:" + searchedMovie + "\n")
                print(moviesList[index] + moviesList[index + 1] + moviesList[index + 2])
                notinList = False
        if(notinList):
            print("Movie not found in records")
    else:
        print("User not found")

    main()
            

def usersReviews():

    otherUser = input("Enter username: ")

    if(exists(otherUser + "reviews.txt")):
        reviewFile = open(otherUser + "reviews.txt")
        reviewsList = reviewFile.readlines()

        for i in reviewsList:
            i = i[0:i.__len__()-1]
            if(i[0:6] == "Review"):
                print(i+"\n")
            else:
                print(i)

        reviewFile.close()
    else:
        print("User not found")
    main()

def searchMovie():

    movietitle = input("What movie would you like to search for? ")


    try:
        url = "https://ott-details.p.rapidapi.com/search"

        querystring = {"title":movietitle,"page":"1"}

        headers = {
            "X-RapidAPI-Key": "f02518403fmsh19a5da995def9b5p10ce65jsn686002427174",
            "X-RapidAPI-Host": "ott-details.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        movieinfojson = response.json()

        for i in movieinfojson["results"]:
            if(i["title"] ==  movietitle):
                movieinfo = i
                movieid = i["imdbid"]
                break


        imdburl = "https://imdb-api.com/API/Ratings/k_akrjj09k/"

        imdbresponse = requests.get(imdburl + movieid)

        imdbinfojson = imdbresponse.json()

        movierating = imdbinfojson["imDb"]

        print("Movie Name: " + str(movieinfo["title"]) + "\nYear Released: " + str(movieinfo["released"]) + "\nGenre(s): " + str(movieinfo["genre"]) + "\nIMDB Rating: " + str(movierating))
        
    except:
        yesNo = input("Could not find that movie. Search again?")
        if(yesNo.lower() == "yes"):
            searchMovie()
    main()

def logout():
    global username
    global password

    username = ""
    password = ""

    main()

def loggedInScreen():
    choice = input("Select an option: \n 1. View your movie reviews \n 2. Review a movie \n 3. Search for one of your reviews \n 4. See another users reviews \n 5. Search another users reviews \n 6. Search for a movie \n 7. Logout \n 8. Exit \n")

    match choice:

        case "1":
            myReviews()
        case "2":
            rateMovie()
        case "3":
            searchMyReviews()
        case "4":
            usersReviews()
        case "5":
            searchOthersReviews()
        case "6":
            searchMovie()
        case "7":
            logout()
        case "8":
            quit()

def initialScreen():
    choice = input("Select an option: \n 1. Log in \n 2. Search for a movie \n 3. Search for a users reviews \n 4. Exit \n")

    match choice:
        case "1":
            getUser()
        case "2":
            searchMovie()
        case "3":
            usersReviews()
        case "4":
            quit()


    

def main():
    
    if(username == ""):
        initialScreen()
    else:
        loggedInScreen()

if __name__ == "__main__":
    main()