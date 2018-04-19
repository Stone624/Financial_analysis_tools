import csv
import sys
sys.stdout.flush()
import datetime

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

airbnb_csv_data = []
with open(sys.argv[1],'rb') as csvfile:
	reader = csv.DictReader( csvfile )
	for row in reader:
		airbnb_csv_data.append(row)

bank_data = []
with open(sys.argv[2],'rbU') as csvfile:
	reader = csv.reader(csvfile, delimiter=',',dialect=csv.excel_tab)
	for row in reader:
		bank_data.append(row)


#set statistics counters
airbnb_records_processed = 0
airbnb_payout_records_processed = 0
airbnb_records_matched = 0
airbnb_records_failed = 0
amount_confirmed = 0
amount_unconfirmed = 0

# Loop through Airbnb CSV Data
for airbnb_data_row in airbnb_csv_data:
	airbnb_records_processed += 1
	# print "DEBUG: PROCESSING RECORD ",airbnb_records_processed
	#find 'payments' type records
	if(airbnb_data_row['Type'] == "Payout"):
		airbnb_payout_records_processed += 1
		# print "DEBUG: PAYMENT FOUND. SEARCHING BANK DOCUMENTS FOR MATCHING RECORD."
		sys.stdout.write( airbnb_data_row['Paid Out']+' ' )
		#loop through Bank data
		found=False
		for record in bank_data:
			#find record with same payout, Report days taken
			if(isclose(float(airbnb_data_row['Paid Out']),float(record[1]))):  # (airbnb_data_row['Paid Out'] == record[1]):
				# print "DEBUG: COMPARING ",type(airbnb_data_row['Paid Out']),airbnb_data_row['Paid Out']," WITH ",type(record[1]),record[1]," : ", (airbnb_data_row['Paid Out'] == record[1])
				# print "DEBUG: MATCHING RECORD FOUND."
				airbnb_records_matched += 1
				amount_confirmed += float(record[1])
				d0 = datetime.datetime.strptime(airbnb_data_row['\xef\xbb\xbfDate'],"%m/%d/%Y").date()
				d1 = datetime.datetime.strptime(record[0],"%m/%d/%Y").date()
				delta = d1 - d0
				print "Record Confirmed. -- ",airbnb_data_row['\xef\xbb\xbfDate']," -> ",record[0],"(",delta.days," days)"
				found=True
				break
		#if find none, report NOT YET PAID error		
		if(not found):
			print "***NO MATCH FOUND IN BANK RECORDS FOR AIRBNB PAYOUT AMOUNT ",airbnb_data_row['Paid Out'],"."
			amount_unconfirmed += float(airbnb_data_row['Paid Out'])
	#If not found, add to composure of previously reported item ** Implies reverse ordering from Airbnb, known to be true.
	else:
		print "\t\t|--> $",airbnb_data_row['Amount'],airbnb_data_row['Type']," -- ",airbnb_data_row['Confirmation Code']," -- ",airbnb_data_row['Guest']," -- ",airbnb_data_row['Start Date']," FOR ",airbnb_data_row['Nights']," NIGHTS"

print "\n\n"
print "******************************"
print "airbnb_records_processed",airbnb_records_processed
print "airbnb_payout_records_processed",airbnb_payout_records_processed
print "airbnb_records_matched",airbnb_records_matched
print "airbnb_records_failed",airbnb_records_failed
print "amount_confirmed",amount_confirmed
print "amount_unconfirmed",amount_unconfirmed
print "******************************"

# PROBLEMS WITH DUPLICATES #