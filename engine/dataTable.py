import sys
sys.path.append("../")
from libraries.libraries import *
# from engine.tempTable import *


original_directory = os.getcwd()
os.chdir("..")
file_path = os.getcwd() + "/temp/" + "playertable.csv"

os.chdir(original_directory)

record_list = []

with open(file_path) as file:
	reader = csv.reader(file)
	next(reader)
	for i, row in enumerate(reader):
		if i >= 5:
			break
		record_list.append(row)


for record in record_list:
	raw_data = requests.get(record[2:][0])
	raw_html = raw_data.text

	soup = BeautifulSoup(raw_html, "html.parser")

	for a_tag in soup.find_all("a", string="Matches Detail"):
		match_details = a_tag["href"]
		raw_data = requests.get(match_details)
		raw_html = raw_data.text

		soup = BeautifulSoup(raw_html, "html.parser")

		match_types = ["TEST matches", "First-class matches", "ODI matches", "List A matches", "T20I matches", "T20 matches", "Four Day matches", "Three Day matches", "Two Day matches", "One Day matches"]
			
		for match_type in match_types:
			for a_tag in soup.find_all("a", string=match_type):
				format_link = a_tag["href"]
				print(format_link)