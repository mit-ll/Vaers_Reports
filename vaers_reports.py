
# import os.path
import string
import sys
from InputFile import InputFile

################################################################################
class VaersData():

################################################################################
  def __init__( self ):
    self.data = {}

################################################################################
  def read_csv( self, filename ):
    rows = []
    with open(filename, encoding="ascii", errors='ignore') as csvfile:
      reader = csv.DictReader( csvfile )
      for row in reader:
        rows.append( row )
    return rows    

################################################################################
  def read_data( self, filename, ages ):
    select_age = {}
    for age in ages:
      select_age[age] = True

    df = InputFile()
    df.setFileName( filename )
    df.openFile()
    line = df.nextLine()
    header = line.split( "," )
    while ( df.isEndOfFile() == 0 ):
      line = df.nextLine()
      if ( line != "" ):
        tokens = df.splitLine( "," )
        row = {}
        for i in range(0, len(header)):
          row[ header[i] ] = tokens[i]

        id = int(row["VAERS_ID"])
        age = -1
        if len(row["AGE_YRS"]) > 0:
          age = int(float(row["AGE_YRS"]))

        # Add this vaccine record for this individual
        if (age in select_age):

          # Check for new individual
          if (id in self.data.keys()) == False:
            self.data[id] = {}

          self.data[id]["data"] = row

    # Close the data file.
    df.closeFile()

################################################################################
  def read_list( self, filename ):
    symptoms = []
    df = InputFile()
    df.setFileName( filename )
    df.openFile()
    while ( df.isEndOfFile() == 0 ):
      line = df.nextLine()
      if ( line != "" ) and (len(line) > 0):
        symptoms.append( line )

    # Close the data file.
    df.closeFile()

    return symptoms

################################################################################
  def read_symptoms( self, filename ):
    df = InputFile()
    df.setFileName( filename )
    df.openFile()
    line = df.nextLine()
    header = line.split( "," )
    while ( df.isEndOfFile() == 0 ):
      line = df.nextLine()
      if ( line != "" ):
        tokens = df.splitLine( "," )
        row = {}
        for i in range(0, len(header)):
          row[ header[i] ] = tokens[i]

        id = int(row["VAERS_ID"])

        # Check if individual is selected
        if (id in self.data.keys()):

          # Check for first symptoms for this individual
          if ("aes" in self.data[id].keys()) == False:
            self.data[id]["aes"] = []
            self.data[id]["ae"] = {}
  
          # Add this vaccine record for this individual
          self.data[id]["aes"].append( row )
  
          # Make the symptoms easily searchable by name
          names = ["SYMPTOM1", "SYMPTOM2", "SYMPTOM3", "SYMPTOM4", "SYMPTOM5"]
          for name in names:
            symptom = row[name]
            if len(symptom) > 0:
              self.data[id]["ae"][symptom] = True

################################################################################
  def read_vax( self, filename ):
    df = InputFile()
    df.setFileName( filename )
    df.openFile()
    line = df.nextLine()
    header = line.split( "," )
    while ( df.isEndOfFile() == 0 ):
      line = df.nextLine()
      if ( line != "" ):
        tokens = df.splitLine( "," )
        row = {}
        for i in range(0, len(header)):
          row[ header[i] ] = tokens[i]

        id = int(row["VAERS_ID"])

        # Check if individual is selected
        if (id in self.data.keys()):

          # Check for first vaccine for this individual
          if ("vax" in self.data[id].keys()) == False:
            self.data[id]["vax"] = []
  
          # Add this vaccine record for this individual
          self.data[id]["vax"].append( row )
        
################################################################################
  def tally_symptoms( self, symptoms ):
    tally = {}
    tally_type = {}
    vax_count = {}
    vax_count["name"] = {}
    vax_count["type"] = {}
    for id in self.data.keys():
      for symptom in symptoms:
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()) and (symptom in self.data[id]["ae"].keys()):
          for vax in self.data[id]["vax"]: 
            vax_name = vax["VAX_NAME"]
            if vax_name in tally:
              tally[vax_name] += 1
            else:
              tally[vax_name] = 1

            vax_type = vax["VAX_TYPE"]
            if vax_type in tally_type:
              tally_type[vax_type] += 1
            else:
              tally_type[vax_type] = 1

      # Total up the vaccines administered
      for vax in self.data[id]["vax"]: 
        vax_name = vax["VAX_NAME"]
        if vax_name in vax_count["name"].keys():
          vax_count["name"][vax_name] += 1
        else:
          vax_count["name"][vax_name] = 1

        vax_type = vax["VAX_TYPE"]
        if vax_type in vax_count["type"].keys():
          vax_count["type"][vax_type] += 1
        else:
          vax_count["type"][vax_type] = 1

    print("Vaccine code report")
    print( "Vaccine name\tSymptoms\tAdministered\tFrequency")
    for name in tally_type.keys():
      freq = 0.0
      if vax_count["type"][name] > 0:
        freq = (tally_type[name] * 100000) / vax_count["type"][name]
      print(name + "\t" + str(tally_type[name]) + "\t" + str(vax_count["type"][name]) + "\t" + str(int(freq)))

    print("\nVaccine name report")
    print( "Vaccine name\tSymptoms\tAdministered\tFrequency")
    for name in tally.keys():
      freq = 0.0
      if vax_count["name"][name] > 0:
        freq = (tally[name] * 100000) / vax_count["name"][name]
      print(name + "\t" + str(tally[name]) + "\t" + str(vax_count["name"][name]) + "\t" + str(int(freq)))
        
################################################################################
  def age_report( self, symptoms ):
    vax_total = {}
    for id in self.data.keys():
      for vax in self.data[id]["vax"]: 
        if ("data" in self.data[id].keys()):
          # vax_name = vax["VAX_NAME"]
          vax_type = vax["VAX_TYPE"]
          data = self.data[id]["data"]
          age = data["AGE_YRS"]
          if len(age) < 1:
            age = "-1"
          else:
            age = str(int(float(age)))
  
          # Check if new vaccine name.
          if (vax_type in vax_total.keys()) == False:
            vax_total[vax_type] = {}
  
          # Check if first of this age for this vaccine name.
          if (age in vax_total[vax_type].keys()) == False:
            vax_total[vax_type][age] = {}
  
          vax_total[vax_type][age][id] = True	# Avoid double counting for multiple doses

    tally = {}
    for id in self.data.keys():
      for symptom in symptoms:
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()) and (symptom in self.data[id]["ae"].keys()):
          for vax in self.data[id]["vax"]: 
            # vax_name = vax["VAX_NAME"]
            vax_type = vax["VAX_TYPE"]
            data = self.data[id]["data"]
            age = data["AGE_YRS"]
            if len(age) < 1:
              age = "-1"
            else:
              age = str(int(float(age)))

            # Check if new vaccine name.
            if (vax_type in tally.keys()) == False:
              tally[vax_type] = {}

            # Check if first of this age for this vaccine name.
            if (age in tally[vax_type].keys()) == False:
              tally[vax_type][age] = {}

            tally[vax_type][age][id] = True	# Avoid double counting for multiple doses

    print( "\nAge report:" )
    # Print the report header line.             
    print( "Age", end="" )
    for vax_type in tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for age in range(-1, 121):
      print( str(age), end="")
      for vax_type in tally.keys():
        count = 0
        freq = 0
        total = 0
        if str(age) in tally[vax_type].keys():
          count = len(tally[vax_type][str(age)].keys())
          total = len(vax_total[vax_type][str(age)].keys())
          if total > 0:
            freq = int( (count * 100000) / total)
          
        print( "\t" + str(count), end="" )
      print()

    print( "\nAge report: count|total|freq/100K" )
    # Print the report header line.             
    print( "Age", end="" )
    for vax_type in tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for age in range(-1, 121):
      print( str(age), end="")
      for vax_type in tally.keys():
        count = 0
        freq = 0
        total = 0
        if str(age) in tally[vax_type].keys():
          count = len(tally[vax_type][str(age)].keys())
        if str(age) in vax_total[vax_type].keys():
          total = len(vax_total[vax_type][str(age)].keys())
          if total > 0:
            freq = int( (count * 100000) / total)
          
        print( "\t" + str(count) + "|" + str(total) + "|" + str(freq), end="" )
      print()
        
################################################################################
  def onset_report( self, symptoms ):
    print( "\nOnset report:" )
    tally = {}
    for id in self.data.keys():
      for symptom in symptoms:
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()) and (symptom in self.data[id]["ae"].keys()):
          for vax in self.data[id]["vax"]: 
            # vax_name = vax["VAX_NAME"]
            vax_type = vax["VAX_TYPE"]
            data = self.data[id]["data"]
            numdays = data["NUMDAYS"]
            if len(numdays) < 1:
              numdays = "-1"

            # Check if new vaccine name.
            if (vax_type in tally.keys()) == False:
              tally[vax_type] = {}

            # Check if first of this onset for this vaccine name.
            if (numdays in tally[vax_type].keys()) == False:
              tally[vax_type][numdays] = {}

            tally[vax_type][numdays][id] = True	# Avoid double counting for multiple doses

    # Print the report header line.             
    print( "Onset", end="" )
    for vax_type in tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for onset in range(-1, 121):
      print( str(onset), end="")
      for vax_type in tally.keys():
        count = ""
        if str(onset) in tally[vax_type].keys():
          count = str(len(tally[vax_type][str(onset)].keys()))
        print( "\t" + count, end="" )
      print()
        
################################################################################
  def shots_report( self, symptoms ):
    total = {}
    kids = {}
    for id in self.data.keys():
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()):
          shots = len(self.data[id]["vax"])
          for vax in self.data[id]["vax"]: 
            # vax_name = vax["VAX_NAME"]
            vax_type = vax["VAX_TYPE"]
            data = self.data[id]["data"]
            age = -1
            if len(data["AGE_YRS"]) > 0:
              age = int(float(data["AGE_YRS"]))

            # Check if new vaccine name.
            if (vax_type in total.keys()) == False:
              total[vax_type] = {}
              kids[vax_type] = {}

            # Check if first of this onset for this vaccine name.
            if (shots in total[vax_type].keys()) == False:
              total[vax_type][shots] = {}
              kids[vax_type][shots] = {}

            total[vax_type][shots][id] = True	# Avoid double counting for multiple doses
            if (age >= 0) and (age < 6):
              kids[vax_type][shots][id] = True	# Avoid double counting for multiple doses

    tally = {}
    kid_tally = {}
    for id in self.data.keys():
      for symptom in symptoms:
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()) and (symptom in self.data[id]["ae"].keys()):
          shots = len(self.data[id]["vax"])
          for vax in self.data[id]["vax"]: 
            # vax_name = vax["VAX_NAME"]
            vax_type = vax["VAX_TYPE"]
            data = self.data[id]["data"]
            age = -1
            if len(data["AGE_YRS"]) > 0:
              age = int(float(data["AGE_YRS"]))

            # Check if new vaccine name.
            if (vax_type in tally.keys()) == False:
              tally[vax_type] = {}
              kid_tally[vax_type] = {}

            # Check if first of this onset for this vaccine name.
            if (shots in tally[vax_type].keys()) == False:
              tally[vax_type][shots] = {}
              kid_tally[vax_type][shots] = {}

            tally[vax_type][shots][id] = True	# Avoid double counting for multiple doses
            if (age >= 0) and (age < 6):
              kid_tally[vax_type][shots][id] = True	# Avoid double counting for multiple doses

    print( "\nShots report:" )
    # Print the report header line.             
    print( "Shots", end="" )
    for vax_type in tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for shots in range(1, 26):
      print( str(shots), end="")
      for vax_type in tally.keys():
        count = ""
        if shots in tally[vax_type].keys():
          count = str(len(tally[vax_type][shots]))
        print( "\t" + count, end="" )
      print()

    print( "\nShots frequency report: count|total|frequency/100K" )
    # Print the report header line.             
    print( "Shots", end="" )
    for vax_type in tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for shots in range(1, 26):
      print( str(shots), end="")
      for vax_type in tally.keys():
        count = ""
        freq = 0
        shots_total = 0
        if shots in tally[vax_type].keys():
          count = len(tally[vax_type][shots])
          shots_total = len(total[vax_type][shots])
          freq = int((count * 100000) / shots_total)

        print( "\t" + str(count) + "|" + str(shots_total) + "|" + str(freq), end="" )
      print()

    print( "\nChildren age 0-5 shots frequency report: count|total|frequency/100K" )
    # Print the report header line.             
    print( "Shots", end="" )
    for vax_type in kid_tally.keys():
      print( "\t" + vax_type, end="" )
    print()

    for shots in range(1, 26):
      print( str(shots), end="")
      for vax_type in kid_tally.keys():
        count = ""
        freq = 0
        shots_total = 0
        if shots in kid_tally[vax_type].keys():
          count = len(kid_tally[vax_type][shots])
          shots_total = len(kids[vax_type][shots])
          if shots_total > 0:
            freq = int((count * 100000) / shots_total)

        print( "\t" + str(count) + "|" + str(shots_total) + "|" + str(freq), end="" )
      print()
        
################################################################################
  def details_report( self, symptoms ):
    print( "\nDetails report:" )
    print( "VAERS ID\tVaccine Code\tVaccine Name\tVax lot\tVax series\tVax route\tAge\tGender\tOnset")
    for id in self.data.keys():
      for symptom in symptoms:
        if ("data" in self.data[id].keys()) and ("ae" in self.data[id].keys()) and (symptom in self.data[id]["ae"].keys()):
          for vax in self.data[id]["vax"]: 
            vax_name = vax["VAX_NAME"]
            vax_type = vax["VAX_TYPE"]
            vax_series = vax["VAX_DOSE_SERIES"]
            vax_lot  = vax["VAX_LOT"]
            vax_route = vax["VAX_ROUTE"]
            data = self.data[id]["data"]
            age = data["AGE_YRS"]
            gender = data["SEX"]
            numdays = data["NUMDAYS"]
            print(str(id) + "\t" + vax_type + "\t" + vax_name + "\t" + vax_lot + "\t" + vax_series + "\t" + vax_route + "\t" + age + "\t" + gender + "\t" + numdays)

################################################################################
  def read_vaers( self, name, ages ):
    self.read_data( name + "VAERSDATA.csv", ages )
    self.read_vax( name + "VAERSVAX.csv" )
    self.read_symptoms( name + "VAERSSYMPTOMS.csv" )

################################################################################

arg_count = len(sys.argv)
if ( arg_count >= 1 ):
  sym_file = sys.argv[1]
  app = VaersData()

  # Read in the symptoms
  symptoms = app.read_list( sym_file )
  print( symptoms )
 
  # Data selections
  # ages = range( 0, 6 )
  ages = range( -1, 121 )
  years = range( 1990, 2024 )
  
  # Read in the VAERS data files
  for year in years:
    app.read_vaers( str(year), ages )
  app.read_vaers( "NonDomestic", ages )
  
  # Generate the reports
  app.tally_symptoms( symptoms )
  app.age_report( symptoms )
  app.onset_report( symptoms )
  app.shots_report( symptoms )
  app.details_report( symptoms )
else:
  print( "usage: python vaers_reports.py <symptoms list file>" )
