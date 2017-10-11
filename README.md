# ml

## A simple implementation of tensorflow model saver



# Usage

import storage_client as sc

ms = sc.ModelStorage()
### save model by

model_id = sc.saveModel(tf_session)

### load model by

tf_session = ms.loadModel(model_id)
 
