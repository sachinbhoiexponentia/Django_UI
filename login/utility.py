import os
import pandas as pd
from django.http import HttpResponse


# Needs file name from request
def downloadCSV(request,filename):
  results = pd.read_csv(f'{os.getcwd()}/upload_csv_files/{filename}_local_data.csv')

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = f'attachment; filename={filename}.csv'

  results.to_csv(path_or_buf=response)
  return response