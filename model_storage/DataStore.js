var mongo = require('mongodb');
var zlib = require('zlib');
var fs = require('fs');
var MongoClient = mongo.MongoClient;

var url = "mongodb://localhost:27017/mydb";

MongoClient.connect(url, function(err, db){
	  if(err) throw err;
    var filepath = "/home/fani/hack/ml/my_model/genesis.tar";
    var iBson = fs.readFile(filepath, function(err, data){
      if(err){ 
          db.close();    
          throw err;
      };
      var myobj = {author: "me", model: data};
      db.collection("testBinary").insertOne(myobj, function(err, res){
        if(err){
          db.close();
          throw err;
        };
        console.log("model successfully inserted");
      });
      db.close();    
    });
});

