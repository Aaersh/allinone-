from django.shortcuts import render
from django.http import HttpResponse
from mainapi.models import hbDatanew
from django.db.models import F, ExpressionWrapper, DecimalField
# Create your views here.
import csv

def is_number(value):
    """Check if a value is a number."""
    try:
        float(value)  # Try to convert to a float
        return True
    except ValueError:
        try:
            int(value)  # Try to convert to an integer
            return True
        except ValueError:
            return False
        
def chk(lst):
    for item in lst:
        if '-' in item:
            return False
    return True
def preprocess_csv_file(csv_file_path):
    raw_data = []

    with open(csv_file_path, "r", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            raw_data.append(row)

    # Determine the datatype of each column
    column_types = []
    for col in range(len(raw_data[1])):
        # if(chk(list(row[col]))==False):
        #     print('bkl')
        #     column_types.append("string")
        if(col ==8 or col==9 or col == 10 or col==34 or col==37 or col==38):
            print('bkl')
            column_types.append("string")
        elif all(is_number(row[col]) for row in raw_data if row[col]):
            column_types.append("number")
        else:
            column_types.append("string")

    # Preprocess values based on their column type
    preprocessed_data = []

    for row in raw_data:
        preprocessed_row = []
        for col, value in enumerate(row):
            if not value:  # Missing or empty value
                if column_types[col] == "number":
                    preprocessed_row.append(0)
                else:
                    preprocessed_row.append("N.A")
            elif column_types[col]=='string' :
                if '-' in value:
                    # Split the value by the hyphen and retain the part before the hyphen
                    value = value.split('-')[0].strip()
                preprocessed_row.append(str(value))
            elif is_number(value):
                preprocessed_row.append(float(value))
            else:
                
                preprocessed_row.append(str(value))
        preprocessed_data.append(preprocessed_row)

    return preprocessed_data

# Example usage:

# csv_file_path = "Book1.csv"
# preprocessed_data = preprocess_csv_file(csv_file_path)


def add_preprocessed_data_to_database(request):

  # Get the preprocessed data.
  preprocessed_data = preprocess_csv_file("H-1B_Disclosure_Data_FY16.csv")

  # Insert the preprocessed data into the database.
  for index, row in enumerate(preprocessed_data):
    if index<1:
      continue
    my_model = hbDatanew(field1=row[0], field2=row[1], field3=row[2], field4=row[3], field5=row[4], field6=row[5], field7=row[6], field8=row[7], field9=str(row[8]), field10=row[9], field11=1, field12=row[11], field13=row[12], field14=row[13], field15=row[14], field16=row[15], field17=str(row[16]), field18=row[17], field19=row[18], field20=row[19], field21=row[20], field22=5028, field23=1, field24=row[23], field25=row[24], field26=row[25], field27=row[26], field28=2015def is_number(value):
    """Check if a value is a number."""
    try:
        float(value)  # Try to convert to a float
        return True
    except ValueError:
        try:
            int(value)  # Try to convert to an integer
            return True
        except ValueError:
            return False, field29=row[28], field30=row[29], field31=row[30], field32=row[31], field33=row[32], field34=row[33], field35=str(row[34]), field36=str(row[35]), field37=row[36], field38=2, field39=row[38])
    my_model.save()

  # Return a response to the user.
  return render(request, "hello.html")


from django.db.models import F, Case, When, Value, FloatField
def updating(request):
    hbDatanew.objects.update(
    field25=Case(
        When(field26='Hour', then=F('field25') *24*365),
        default=F('field25'),
        output_field=FloatField()
    )
)
    hbDatanew.objects.update(
        field25=Case(
            When(field26='Week', then=F('field25') *52),
            default=F('field25'),
            output_field=FloatField()
        )
)
def number_ofrecords(request):
  # hbData.objects.filter(field26='Hour').update(field25=)
#   hbDatanew.objects.update(
#     field25=Case(
#         When(field26='Week', then=F('field25') *52),
#         default=F('field25'),
#         output_field=FloatField()
#     )
# )
  
  record_count=hbDatanew.objects.count()
  
  print("No. of records",record_count)
  return record_count

from django.db.models import Avg
def analysis_2(request):
  mean_salary = hbDatanew.objects.all().aggregate(avg_salary=Avg('field25'))

# The result is a dictionary with the key 'avg_salary' containing the mean salary
  avg_salary = mean_salary['avg_salary']

  print("Mean Salary of H1B Applicants:", avg_salary)
  return avg_salary
  
def analysis_3(request):  

  # Step 1: Filter H1B applicants
  h1b_applicants = hbDatanew.objects.order_by('field25')

  # Step 2: Calculate the count of H1B applicants
  count = h1b_applicants.count()

  # Step 3: Calculate the median salary
  if count % 2 == 1:
      median_salary = h1b_applicants[count // 2].field25
  else:
      lower_salary = h1b_applicants[(count - 1) // 2].field25
      upper_salary = h1b_applicants[count // 2].field25
      median_salary = (lower_salary + upper_salary) / 2

  print("Median Salary of H1B Applicants:", median_salary)
  return median_salary

def analysis_4(request):
    h1b_applicants = hbDatanew.objects.order_by('field25')
    rank = (int)((number_ofrecords(request) + 1)/4)
    return h1b_applicants[rank].field25

def analysis_5(request):
    h1b_applicants = hbDatanew.objects.order_by('field25')
    rank = (int)(((number_ofrecords(request) + 1)*3)/4)
    x=h1b_applicants[rank]
    
    return x.field25

def home(request):
    return render(request,'hello.html')
def oneapi(request):
    add_preprocessed_data_to_database(request)
    updating(request)
    noOfRecords = number_ofrecords(request)
    mean = analysis_2(request)
    median = analysis_3(request)
    per_25 = analysis_4(request)
    per_75 = analysis_5(request)
    context={"mean_s":mean,"median_s":median, "number": noOfRecords, "per25": per_25, "per75": per_75}
    # hbDatanew.objects.all().delete()
    return render(request, '2016.html',context)
    
    
    