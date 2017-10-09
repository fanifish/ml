var mongo = require('mongodb');

var MongoClient = mongo.MongoClient;

var url = "mongodb://localhost:27017/mydb";

MongoClient.connect(url, function(err, db){
	if(err) throw err;
	var query = {address: /^S/};	
	db.collection("customers").find(query).toArray(function(err, res){
	  if(err) throw err;
	  console.log(res);
	  db.close();
	});
});
