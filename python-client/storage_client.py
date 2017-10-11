#!/usr/bin/env python

from pymongo import MongoClient
import tensorflow as tf
import datetime
import uuid
import os
from subprocess import call
import bson
from bson.binary import Binary, UUIDLegacy, STANDARD
from bson.codec_options import CodecOptions
import json

class ModelStorage:
    """
        Implementation of model storage client for tensorflow
        to persist a trained model on a mongo database
    """

    def __init__(self):
        self.url = 'mongodb://localhost:27017/'
        self.client = MongoClient(self.url)
    
    def createDB(self, db_name):
        db = self.client[db_name]
        return db

    def getCollection(self, db_name, collection):
        db = self.client[db_name]
        return db[collection]
    
    def insertDoc(self, db_name, collection, data):
        col = self.getCollection(db_name, collection)
        insert_id = col.insert_one(data).inserted_id
        return insert_id
    
    def saveModel(self, sess, info):
        """
            @tf_model is the trained tensorflow graph
            @info is meta data describing the graph (i.e. score, dataset, parameters used)
        """
        uid = str(uuid.uuid1())
        export_dir = "/var/tmp/models/export_model_"+uid
        builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
        tag_constants = tf.saved_model.tag_constants
        builder.add_meta_graph_and_variables(sess,[tag_constants.TRAINING])
        builder.save()
        model_name="model_"+uid
        call(["tar", "-cvzf", "/var/tmp/models/"+model_name+".tar", "-C", export_dir, "."])
        filepath="/var/tmp/models/"+model_name+".tar"
        f = open(filepath, 'r')
        
        post = {"author": "faniel",
                "desc": "model trained on mnist 10k",
                "score": "0.917",
                "model_id": model_name,
                "model": Binary(f.read()),
                "team" : "eve"
                }
        self.insertDoc('models', 'tf_models', post)
        # clean up the temporary stored model archive
        call(["rm", "-r", "/var/tmp/models/"+model_name])
        call(["rm", "-r", export_dir])
        print("model : " + model_name + " successfuly uploaded\n")

    def loadModel(self, model_id):
        """ 
            Load a model identified by the model ID
            returns a session
        """
        query={'model_id':model_id}
        coll = self.getCollection('models', 'tf_models')
        cur = coll.find(query)
        data = []
        for doc in cur:
            data.append(doc)
        print(data, len(data))
        model_binary = data[0][u'model']
        f = open("/var/tmp/models/"+model_id+".tar", 'w+')
        f.write(model_binary)
        f.flush()
        f.close()
        print('temp archive file written to /var/tmp/models/'+model_id+"\n")
        call(["mkdir", "/var/tmp/models/"+model_id])
       # call(["gunzip", "/var/tmp/models/"+model_id+".tar", ">", "/var/tmp/models/"+model_id+".tar"])
        call(["tar", "-xvzf", "/var/tmp/models/"+model_id+".tar", "-C", "/var/tmp/models/"+model_id])
        print(os.path.isdir("/var/tmp/models/"+model_id))
        
        load_dir="/var/tmp/models/"+model_id
        tag_constants = tf.saved_model.tag_constants
        load_sess = tf.InteractiveSession()
        tf.saved_model.loader.load(load_sess, [tag_constants.TRAINING], load_dir)
        call(["rm", "-r", "/var/tmp/models/"+model_id])
        print("model load complete\n")
    #   return None
        print(load_sess)
        return load_sess
        
def main():
    print('model storage client')
    ms = ModelStorage()
    model_id = "model_5f8ec0dc-adf6-11e7-b7d8-000c29421ad5"
    load_sess = ms.loadModel(model_id)
    print('Done')

if __name__ == "__main__":
    main()


