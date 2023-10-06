import json

# with open('AllDoctorsData_unique.json', 'r', encoding='utf-8') as f:
#     input_data = json.load(f)

# transformed_data = []

# total = 0

# for index, doctor in enumerate(input_data):
#     print(f"{index + 1}...{doctor['link']}")
#     try:
#         common_attributes = {
#             "link": doctor["link"],
#             "Doctor_name": doctor["Doctor_name"],
#             "category": doctor["category"],
#             "Address": doctor["Address"],
#             "phone_number": doctor["phone_number"],
#             "Specialites": doctor["Specialites"],
#             "permis": doctor["permis"],
#             "Status": doctor["Status"],
#             "Assurance": doctor["Assurance"],
#             "Active": doctor["Active"],
#             "Status_discription": doctor["Status_discription"],
#             "Statut": doctor.get("Statut", ""),
#             "Statut_discription": doctor["Statut_discription"]
#         }

#         if not doctor.get("Recommandation"):
#             transformed_review = common_attributes.copy()
#             transformed_review["reviewer_name"] = ""
#             transformed_review["reviewe_date"] = ""
#             transformed_review["text"] = ""
#             transformed_data.append(transformed_review)
#             total += 1
#         else:
#             for review in doctor["Recommandation"]:
#                 transformed_review = common_attributes.copy()
#                 transformed_review["reviewer_name"] = review["name"]
#                 transformed_review["reviewe_date"] = review["Date"]
#                 transformed_review["text"] = review["Description"]
#                 transformed_data.append(transformed_review)
#                 total += 1
        
#     except Exception as e:
#         print(f"Error processing doctor {index + 1}: {str(e)}")
#         print(f"Doctor Data: {doctor}")

# with open('AllDoctorsData_new.json', 'w', encoding='utf-8') as o:
#     json.dump(transformed_data, o, indent=4)

# print('data:', len(input_data), '...', 'transformed:', len(transformed_data), "...", "total:", total)



import pandas as pd
with open('AllDoctorsData_new.json', 'r') as json_file:
    data = pd.read_json(json_file)

data.to_csv('AllDoctorsData_new.csv', index=False)