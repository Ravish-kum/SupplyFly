import pandas as pd
import os
from backend.models import *
from authentication.models import User

def export_to_csv(instance, file_name, file_path):

    if not os.path.exists(file_path):
            os.mkdir(file_path)
    file_path = os.path.join(file_path, file_name)
    
    df = pd.DataFrame(instance)
    df.to_csv(file_path, mode='w')
    return True

