import pickle

with open('output/models/kitti/VirConv-T/default/eval/epoch_60/val/default/result.pkl', 'wb') as f:
   pickle.dump(obj_name, f)