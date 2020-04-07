#This code will train a model
from churnexplainer import train
from churnexplainer.data import dataset, load_dataset
import cdsw, os

print(sys.argv[1])
print(sys.argv[2])

if len(sys.argv) > 1:
  os.environ['CHURN_MODEL_TYPE'] = sys.argv[1]
  os.environ['CHURN_DATASET'] = sys.argv[2]
  
else:
  os.getenv('CHURN_MODEL_TYPE','linear')
  os.getenv('CHURN_DATASET', 'telco')

print(os.getenv('CHURN_MODEL_TYPE'))
  
train_score, test_score, model_path = train.experiment_and_save()

cdsw.track_metric("train_score",round(train_score,2))
cdsw.track_metric("test_score",round(test_score,2))
cdsw.track_metric("model_path",model_path)
cdsw.track_file(model_path)
