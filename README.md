# Financial_analysis_tools
Personal Project for tools comparing and confirming Airbnb transaction CSV data

Run with "python Financial_Analysis_Checker.py path/to/Airbnb_CSV_Data path/to/bank_CSV_Data"

Output will be the following format:

[amount] [Confirmation Status] -- [date Airbnb sent payment] -> [date bank received payment] ([processing time] days)
		Subsequent rows indented indicate makeup of amount sent.
		|--> $ [amount] [type of transaction] -- [confirmation code] -- [guest name] -- [checkin date] FOR [duration of stay] NIGHTS

Example:

758.51 Record Confirmed. --  01/14/2018  ->  01/15/2018 ( 1  days)
		|--> $ 315.00 reservation  --  HM2AJK78F1  --  Jimmy Terrace  --  01/14/2018  FOR  2  NIGHTS
		|--> $ 104.00 Co-hosting Payout  --  HMNE3DAP0T  --  Kahn Door  --  01/14/2018  FOR  3  NIGHTS
		|--> $ 439.51 Co-hosting Payout  --  HM2UV61VNZ  --  Lerry Fisher  --  01/13/2018  FOR  10  NIGHTS


Notes: 
1. Manual inspection may be necessary to ensure accuracy. Duplicates in bank CSV data (2 transactions for the exact same amount) will always use the most recent. Looking for unusually long periods of processing time can spot obvious cases of this error.
2. The bank data is expected in the form "Date","Amount". No other information is necessary. Clearing the bank CSV of non-Airbnb related entries may help reduce false-positives.