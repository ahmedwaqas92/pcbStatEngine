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
		if i >= 100:
			break
		record_list.append(row)


for record in record_list:
	raw_data = requests.get(record[2:][0])
	raw_html = raw_data.text

	soup = BeautifulSoup(raw_html, "html.parser")

	for divBlock in soup.find_all("div", {"class": "excerpt"}):
		p_tags = divBlock.find_all("p")

		time.sleep(1)
		
		if p_tags[1].contents[1].strip() == "-": 
			birth_date = ""
			current_age = ""
			birth_place = ""

		elif re.search(r'\d(?=[^0-9]*$)', p_tags[1].contents[1].strip()):
			match = re.search(r'\d(?=[^0-9]*$)', p_tags[1].contents[1].strip())
			if match:
				position = match.end()
				result =  p_tags[1].contents[1].strip()[:position]
				birth_date_raw = result


				birth_date = datetime.strptime(birth_date_raw, "%d %b %Y").strftime('%d %B %Y')
				current_age = str(datetime.today().year - datetime.strptime(birth_date_raw, "%d %b %Y").year) + " years"
				birth_place = p_tags[1].contents[1].strip()[position:]

		else:
			birth_date = ""
			current_age = ""
			birth_place = p_tags[1].contents[1].strip().replace("- ", "")

		if p_tags[3].contents[1].strip().replace(", ", ",").split(",")[0] == "-":
			teams = ""
		else:
			teams = p_tags[3].contents[1].strip().replace(", ", ",").split(",")

		if p_tags[4].contents[1].strip() == "-":
			bat_style = ""
		else:
			bat_style = p_tags[4].contents[1].strip()
		
		if p_tags[5].contents[1].strip() == "-":
			bow_style = ""
		else:
			bow_style = p_tags[5].contents[1].strip()


		print("player_id: " + str(record[0:][0]))
		print("player_name: " + str(record[1:][0]))
		print("birth_date: " + str(birth_date))
		print("current_age: " + str(current_age))
		print("birth_place: " + str(birth_place))
		print(teams)
		print("bat_style: " + str(bat_style))
		print("bowl_style: " + str(bow_style))


	for a_tag in soup.find_all("a", string="Matches Detail"):
		match_details = a_tag["href"]
		raw_data = requests.get(match_details)
		raw_html = raw_data.text

		soup = BeautifulSoup(raw_html, "html.parser")

		match_types = ["TEST matches", "First-class matches", "ODI matches", "List A matches", "T20I matches", "T20 matches", "Four Day matches", "Three Day matches", "Two Day matches", "One Day matches"]
			
		for match_type in match_types:
			for a_tag in soup.find_all("a", string=match_type):
				format_link = a_tag["href"]
				