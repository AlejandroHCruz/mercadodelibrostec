__author__ = 'Alejandro H. Cruz'
import requests
import json
import time
import csv

listEntry = []
superList = []
publicationIds = []

accesToken = 'CAACEdEose0cBADZBOslhdOYyf6un781ZBwKSwb2xEqVrzDrrul74K8GLRtqJVMIGaj6XxYBysRMKSDkKNKe8NmNbOUTcWUV0IPjj8ptuvbmHGAX9bKT8yxLSqLVxZAOXXRhAD0FG6XDJVgiTHDDGPvEmNqHOOUCh1ZBiRBBSKwur74A8kYRSGgogb2QDUzD3xNoXgw7RtgZDZD'
feedUrl = 'https://graph.facebook.com/141058865925000/feed?limit=100&access_token='+accesToken
feed = requests.get(feedUrl)
feedAsJSON = feed.json()

if feedAsJSON:

    # Get first 100 posts/publications
    print("Getting first 100 publications")
    j = 0
    data = feedAsJSON['data']
    for publication in data:
        publicationId = publication['id']
        publicationIds.append(publication['id'])
        publicationUpdatedTime = publication['updated_time']
        try:
            publicationMessage = publication['message']
        except:
            publicationMessage = ""

        # save data to superList
        listEntry = [publicationId, publicationUpdatedTime, publicationMessage]
        superList.append(listEntry)


        j+=1

    # Getting more posts/publications

    pageCount = 0
    try:
        nextPageExists = feedAsJSON['paging']['next']
    except:
        nextPageExists = None

    while nextPageExists is not None:
        pageCount+=1
        try:
            print("Getting page: " + str(pageCount))
            paging = feedAsJSON['paging']
            nextPage = paging['next']
            feed = requests.get(nextPage)
            feedAsJSON = feed.json()
            if feedAsJSON:
                data = feedAsJSON['data']
                for publication in data:
                    publicationId = publication['id']
                    publicationUpdatedTime = publication['updated_time']
                    try:
                        publicationMessage = publication['message']
                    except:
                        publicationMessage = ""

                # save data to superList
                listEntry = [publicationId, publicationUpdatedTime, publicationMessage]
                superList.append(listEntry)

                j+=1
                time.sleep(1)

        except:
            nextPageExists = None
            print('Completed')

    print("superList: ")
    print(superList)

    # Get comments for every post/publication

    i = 0
    commentsList = []
    for publicationId in publicationIds:
        i += 1
        commentsUrl = 'https://graph.facebook.com/' + publicationId + '/comments?summary=true&access_token=' + accesToken
        feed = requests.get(commentsUrl)
        feedAsJSON = feed.json()
        if feedAsJSON:
            commentsCount = feedAsJSON['summary']['total_count']
            commentsList.append(str(commentsCount))
            print('total comments: ' + str(commentsCount))

#Save data to files

with open("publications.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(superList)

print("commentsList: ")
print(commentsList)

with open("comments.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(commentsList)