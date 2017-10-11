# ml

## A simple implementation of tensorflow model saver



# Usage

import storage_client as sc

### save model by

sc.saveModel(tf_session)

### load model by

ms = sc.ModelStorage()

tf_session = ms.loadModel($MODELNAME)
 
