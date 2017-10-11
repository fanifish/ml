var mongo = require('mongodb');
var zlib = require('zlib');
var fs = require('fs');


var MongoClient = mongo.MongoClient;

var url = "mongodb://localhost:27017/mydb";

MongoClient.connect(url, function(err, db){
    if(err) throw err;
    db.collection("testBinary").findOne({}, function(err, result){
      if(err) throw err;
      fs.writeFile("me.tar", result.model.buffer, function(err){
        if(err) throw err;
        console.log('successfuly loaded to file!');
      });
    });
    db.close();
});

