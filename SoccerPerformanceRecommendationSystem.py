# Program by Montana Merkle
# 11/14/2024
# CS 470
# Program creates GUI that displays results of training random forest classifier using
#   previous UNA soccer players game data, clustering current players (from file) into
#   similar groups, and predicting the class of each cluster (the recommended drill category)
# References for classifying and clustering:
#             base code for using random forest classifier taken from Dr. Terwilliger's AI class (10/1)
#             base code for clustering taken from Dr. Terwilliger's AI class (10/3)
#             base code for using the label encoder taken from Dr. Terwilliger's AI class (9/17)
#             https://www.geeksforgeeks.org/numpygenfromtxt/
#             https://www.freecodecamp.org/news/python-find-in-list-how-to-find-the-index-of-an-item-or-element-in-a-list/
#             https://scikit-learn.org/dev/modules/generated/sklearn.preprocessing.LabelEncoder.html
#             https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
#             https://numpy.org/doc/stable/reference/generated/numpy.unique.html
#             https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
#             https://www.geeksforgeeks.org/how-to-convert-numpy-array-to-list/
#             https://pythontextbook.com/chapter-5/
#             https://www.geeksforgeeks.org/python-find-most-frequent-element-in-a-list/
#             https://www.geeksforgeeks.org/numpy-vstack-in-python/?ref=next_article
#             https://www.codecademy.com/learn/ida-3-introduction-to-numpy/modules/ida-3-2-numpy-syntax/cheatsheet
# References for tkinter GUI:
#             https://stackoverflow.com/questions/14267900/drag-and-drop-explorer-files-to-tkinter-entry-widget
#             https://pythontextbook.com/chapter-13/
#             https://www.geeksforgeeks.org/python-gui-tkinter/
#             https://www.geeksforgeeks.org/tkinter-fonts/
#             https://www.tutorialspoint.com/how-to-change-the-size-of-text-on-a-label-in-tkinter
#             https://www.geeksforgeeks.org/how-to-get-the-tkinter-label-text/
#             https://www.tutorialspoint.com/python/string_endswith.htm
#             https://www.geeksforgeeks.org/python-string-strip/
#             https://www.geeksforgeeks.org/python-tkinter-listbox-widget/
#             https://www.tutorialspoint.com/how-to-fully-change-the-color-of-a-tkinter-listbox
#             https://www.geeksforgeeks.org/python-grid-method-in-tkinter/
#             https://pythonistaplanet.com/python-file-io-exercises/
#             https://www.tutorialspoint.com/how-to-make-the-tkinter-text-widget-read-only
#             https://www.geeksforgeeks.org/horizontally-center-a-widget-using-tkinter/
#             https://www.geeksforgeeks.org/python-tkinter-text-widget/
#             https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html
#             https://www.geeksforgeeks.org/change-the-color-of-a-tkinter-label-programmatically/
#             https://www.geeksforgeeks.org/python-program-to-get-the-file-name-from-the-file-path/

#import tkinter module and necessary libraries
from tkinter import *
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter.font as tkFont
import os

#import libraries for clustering and classifying
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

#define function for finding most frequent item in list, returns most common int in list
#***code taken from geeksforgeeks.org***
def most_frequent(List):
    return max(set(List), key=List.count)

#define function to get file name, returns just the file name from file path
def getFileName():
    #get current index of last item in list box and store file name
    file_name = listbox.get(listbox.size() - 1)
    #strip file name of curly brackets
    file_name = file_name.strip("{}")
    #get file name out of file path
    file_name = os.path.basename(file_name)
    return file_name

#define function that handles file dropped event
def file_dropped(event):
    #will allow file inserted if it is the first time or an error prior
    if listbox.size() == 0 or listbox.cget("background") != colorsList[2]:

        #insert file into list box and store name
        listbox.insert(tk.END, event.data)
        file_name = getFileName()
        
        #confirm listbox is given file that ends in csv
        if file_name.endswith(".csv"):
            #confirm file is in current directory
            if os.path.isfile(file_name):
                #change listbox to convey file accepted
                listbox.configure(background=colorsList[2], foreground="white")
                #change instructions
                instrLabel.config(text="File Accepted!")
            else:
                #change instructions if error
                instrLabel.config(text="ERROR - file must be in working directory")
        else:
            #change instructions if error
            instrLabel.config(text="ERROR - must be a csv file")

#define function to create text box with description of drill and label of recommended drill category
def drillDescription(i,predClass):
    #create text box to store drill category description
    drillText = Text(window, height=5, width=95, font=('Helvetica',10))
    drillText.grid(pady=10,row = 5 + 2*i,column=1)

    #create empty temp variable to store full drill category name
    actualCName = ""

    #depending on predicted class, convert abbreviation into full class name and insert description into text box
    if predClass == "R":
        actualCName = "Rondo Drills"
        drillText.insert(END, "Rondo drills improve decision making and passing\n")
        drillText.insert(END, "Examples include:\n")
        drillText.insert(END, "   3v1 - three players keep the ball away from one\n")
        drillText.insert(END, "   Rondo to Attack - a team must reach a number of passes before going to goal\n")
        drillText.insert(END, "   Two Team Possession - one team keeps the ball away from the other, passes for points")
    elif predClass == "C":
        actualCName = "Cone Dribbling Drills"
        drillText.insert(END, "Cone dribbling drills improve footwork and ball control\n")
        drillText.insert(END, "Examples include (all using a single line of cones):\n")
        drillText.insert(END, "   Straight Dribbling - dribble through the line of cones\n")
        drillText.insert(END, "   Foundation - dribble through the line of cones only using inside of the foot\n")
        drillText.insert(END, "   Inside Outside - dribble through the line of cones using inside and then outside of the foot")
    elif predClass == "A":
        actualCName = "Acceleration Drills"
        drillText.insert(END, "Acceleration drills improve top speed and ability to change directions\n")
        drillText.insert(END, "Examples include:\n")
        drillText.insert(END, "   18yrd Repeats - run to the 18yrd box and back in 5 sets of 1 minute (constant down and back)\n")
        drillText.insert(END, "   10 Jog,Sprint,Walks - jog till the outside of the box, sprint till other half's box, walk rest\n")
        drillText.insert(END, "   5 Full Field Sprint - 60% sprint till the half, then 90% for the rest of the field")
    elif predClass == "SDPP":
        actualCName = "Short Distance Passing Pattern Drills"
        drillText.insert(END, "Short distance passing pattern drills improve passing speed and quality\n")
        drillText.insert(END, "Examples include (all using set up patterns of cones with a player at each):\n")
        drillText.insert(END, "   Box Drill - players pass around the box (cones 5yds apart) opening with right/left foot\n")
        drillText.insert(END, "   Diamond Drill - players pass around a diamond (cones 10yds apart) opening with right/left foot\n")
        drillText.insert(END, "   Turning Drill - 3 cones are 10yds apart, pass to the player in the middle cone who turns and plays the other side")
    elif predClass == "LDPP":
        actualCName = "Long Distance Passing Pattern Drills"
        drillText.insert(END, "Long distance passing pattern drills improve passing quality and endurance\n")
        drillText.insert(END, "Examples include (all using set up patterns of cones with a player at each):\n")
        drillText.insert(END, "   Formation Passing - players pass around the current formation utilized by the team, following the pass as they go\n")
        drillText.insert(END, "   One Two Passing - two lines of players, one line player to the other and gets it back for a forward run (at least 20yds)\n")
        drillText.insert(END, "   Through Ball Passing - 2 cones 40yds apart, one line plays the player at the other in the air and then replaces them")

    #set state of text box to disabled (read-only)
    drillText.config(state= DISABLED)
        
    #create label for the recommended drill class
    recommendLabel = Label(window, text=f"Recommended Category: {actualCName}", font=('Helvetica',15), fg=colorsList[i])
    recommendLabel.grid(pady=10,row = 4 + 2*i,column=1)

#define function that handles start button being pushed (starts clustering and classifying)
def startButtonClick():
    #if file has been verified and button hasn't been pressed before continue, else do nothing
    if listbox.cget("background") == colorsList[2] and startButton.cget("text") != "Complete!":

        #if file for previous player data in current directory continue
        #else change button text into error message
        if os.path.isfile("trainingData.csv"):
            
            #reset instruction label if needed (to get rid of error message
            # if previous player data not in current directory)
            instrLabel.config(text="File Accepted!")

            #*****************Begin Clustering******************
            
            #get verified file name
            file_name = getFileName()

            #load input data from players data sheet given by user
            Xcurrent = np.loadtxt(file_name, delimiter=',', skiprows=1, usecols=(2,3,4,5,6,7))
            players = np.genfromtxt(file_name, delimiter=',', dtype=str, skip_header=1, usecols=(0))

            #set number of clusters
            num_clusters = 3  
            
            #create KMeans object
            kmeans = KMeans(init='k-means++', n_clusters=num_clusters, n_init=10)

            #train the KMeans clustering model using player data given by user
            kmeans.fit(Xcurrent)

            #create variable that contains each player's cluster
            labels=kmeans.labels_

            #get list of unique players from player list
            uniquePlayers = np.unique(players)
            
            #create list to store cluster assignments for each player
            clustersAssigned = []

            #iterate through players list
            for player in uniquePlayers:
                # add empty list for each player that can be filled with cluster numbers assigned
                clustersAssigned.append([])

            #fill cluster list at each players unique index with cluster numbers assigned to that player
            #must use enumerate here so that index from the players list can be used
            for i, player in enumerate(players):
                
                #find the index of the player from unique players list
                uniqueIndex = list(uniquePlayers).index(player)     #must turn np array to list to find index of player, from geeksforgeeks.org
                
                #add the cluster number (i) assigned to player at the unique index of clusters assigned list
                clustersAssigned[uniqueIndex].append(int(labels[i]))

            #create list to store dominant cluster for each player
            domClusters = []

            #iterate through players list and add dominant cluster to list at player index
            for i in range(len(uniquePlayers)):
                domClusters.append(most_frequent(clustersAssigned[i]))
            
            #create list to store averages for each cluster (cluster number is index of list)
            clusterAvgs = []

            #iterate through each cluster
            for num in range(num_clusters):
                
                #for each cluster create array to store all data for each player
                clusterData = []

                #create label for each cluster
                clusterLabel = Label(window, text=f"Cluster {num+1}", font=('Helvetica',15), bg=colorsList[num], fg="white")
                clusterLabel.grid(pady=10,row = 4 + 2*num)

                #create listbox for each cluster to be filled with player names
                clusterListbox = tk.Listbox(window, width=20, height=5, font=('Helvetica',12))
                clusterListbox.grid(pady=10,row = 5 + 2*num,column=0)

                #iterate through players list; if dominant cluster is current cluster being iterated, add player name to cluster listbox
                for i in range(len(uniquePlayers)):
                    if domClusters[i] == num:
                        
                        #add player to cluster listbox based on current index (how many already filled)
                        currIndex = clusterListbox.size() - 1
                        clusterListbox.insert(currIndex, uniquePlayers[i])
                        
                        #get and add all the data from player into cluster data array
                        playerData = Xcurrent[players == uniquePlayers[i]]
                        clusterData.append(playerData)

                #create stack of arrays into one array (so able to use np mean function, from geeksforgeeks.org)
                clusterData = np.vstack(clusterData)

                #calculate cluster average
                clusterMean = np.mean(clusterData, axis=0)  #axis set to 0 to find average of all columns, from codecademy.com
                
                #add the cluster average into list of all cluster averages (first convert np array to list, from geeksforgeeks.org)
                clusterAvgs.append(list(clusterMean))

            #*****************End Clustering******************

            #*****************Begin Classifying******************

            #load input data from previous players data sheet (already verified it is in cd)
            input_file = 'trainingData.csv'
            #use metrics for each previous player for Xprev
            Xprev = np.loadtxt(input_file, delimiter=',', skiprows=1, usecols=(2,3,4,5,6,7))
            #use drill performed by previous players for labels
            labels = np.genfromtxt(input_file, delimiter=',', dtype=str, skip_header=1, usecols=(8))
            
            #create label encoder and fit labels
            encoder = preprocessing.LabelEncoder()
            encoder.fit(labels)

            #encode labels/drills using encoder and set as y
            y = encoder.transform(labels)

            #turn np array into list, from geeksforgeeks.org
            classes = list(encoder.classes_)

            #random forest classifier
            params = {'n_estimators': 100, 'random_state': 0, 'max_depth': 20}
            classifier = RandomForestClassifier(**params)
            
            #use all previous player data to train the classifier
            classifier.fit(Xprev, y)

            #loop through each cluster (using i as cluster number)
            for i, cluster in enumerate(clusterAvgs):
                #predict the probabilities of cluster classified as each class
                probabilities = classifier.predict_proba([cluster])[0]

                #store and get index of highest probability
                encoded_predicted_class = int(np.argmax(probabilities))
                
                #decode the encoded class name, must have array as parameter
                predicted_class = encoder.inverse_transform([encoded_predicted_class])

                #add description text box and label for recommended drill of each cluster to window
                drillDescription(i, predicted_class[0])
                
            #once done, inform the user that the application is done
            startButton.config(text="Complete!")

            #*****************End Classifying******************

        #if previous player data file not in current directory error message
        else:
            instrLabel.config(text="ERROR - need training data file in current directory")
            

#create Tk object named window
window = TkinterDnD.Tk()

#set window title
window.title("Soccer Performance Recommendation System")
#set minimum size of window
window.minsize(1000,800)

#create list of colors to use throughout program
colorsList = ["deep sky blue", "purple4", "dark turquoise", "medium blue"]

#configure grid to allow centering
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)

#create label for title
titleLabel = Label(window, text="Welcome to the Soccer Performance Recommendation System", font=('Helvetica',20), fg=colorsList[3])
titleLabel.grid(padx=10,pady=10,columnspan=2)

#create label for instructions on drag and drop box
instrLabel = Label(window, text="Drag your file of current players and metrics HERE:", font=('Helvetica',15), fg=colorsList[3])
instrLabel.grid(pady=10,columnspan=2)

#create listbox to take in file
listbox = tk.Listbox(window, width=80, height=3)
listbox.grid(padx=10,pady=10,columnspan=2)

#register listbox as target for drag and drop
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', file_dropped)
        
#create start button
startButton = Button(window, text="Start Analyzing File",font=('Helvetica',15),command=startButtonClick,width = 25)
startButton.grid(padx=100,pady=20,columnspan=2)

#look for events until program exited
window.mainloop()
