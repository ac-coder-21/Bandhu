import pymongo
import gridfs


client = pymongo.MongoClient('localhost', 27017)
db = client.test_mc
collection = db.score

name = 'Aston Martin-01-04-2024-General Mental Health Assesment.pdf'
location = 'D:\Bandhu-A-mental-chatbot-app\\' + name
file_Data = open(location, 'rb')
data = file_Data.read()
fs = gridfs.GridFS(db)
fs.put(data=data, filename = name)
print('upload completed')

data = db.fs.files.find_one({'filename': name})
my_id = data['_id']
outputdata = fs.get(my_id).read()
download_loc = "C:/Users/AC/Downloads//" + name
output = open(download_loc, 'wb')
output.write(outputdata)
output.close()
print('Download Complete')
