import pandas as pd

# data = [
#     {
#         "link": "https://www.quebecmedecin.com/medecin/medecin-begin-louis-r-9188.htm",
#         "Doctor_name": "Dr Bégin Louis R.",
#         "category": "Anatomopathologiste",
#         "Address": "Hôpital du Sacré-Coeur de Montréal dép d'anatomo-pathologie 5400 boul Gouin O Montréal QC H4J 1C5 Canada",
#         "phone_number": "514-338-2222 #2965",
#         "Specialites": [
#             "Anatomopathologiste"
#         ],
#         "permis": "76445",
#         "Statut": " Inscrit ",
#         "Assurance": " Avec assurance responsabilité professionnelle",
#         "Recommandation": [
#             {
#                 "name": "Sylvie Gagnon",
#                 "Date": "10 June 2023",
#                 "Description": "Super bon md , très dédié, vaillant , professionnel , fameux ..et tout ! À être très recommandé, .."
#             }
#         ]
#     },
#     {
#         "link": "https://www.quebecmedecin.com/medecin/medecin-temmar-rabia-2308.htm",
#         "Doctor_name": "Dr Temmar Rabia",
#         "category": "Anatomopathologiste",
#         "Address": "CHUS - Hôpital Fleurimont 3001 12e Avenue N Sherbrooke QC J1H 5N4 Canada",
#         "phone_number": "819-346-1110 #22908",
#         "Specialites": [
#             "Anatomopathologiste"
#         ],
#         "permis": "05302",
#         "Statut": " Inscrit ",
#         "Assurance": " Avec assurance responsabilité professionnelle",
#         "Recommandation": [
#             {
#                 "name": "AICHA",
#                 "Date": "11 July 2019",
#                 "Description": "Dr Temmar est très professionnel et d'une très grande compétence. Excellent médecin que je recommande vivement."
#             }
#         ]
#     },
#     {
#         "link": "https://www.quebecmedecin.com/medecin/medecin-nobert-gagne-suzanne-7796.htm",
#         "Doctor_name": "Dr Nobert-Gagné Suzanne",
#         "category": "Anatomopathologiste",
#         "Address": "Polyclinique Saint-Martin 307-1435 boul Saint-Martin O Laval QC H7S 2C6 Canada",
#         "phone_number": "450-667-2664",
#         "Specialites": [
#             "Anatomopathologiste"
#         ],
#         "permis": "",
#         "Statut": "",
#         "Assurance": "",
#         "Recommandation": []
#     }
    
# ]

# df = pd.DataFrame(data)

# df = df.explode('Recommandation')

# df.to_csv('all.csv', index=False)




data = [
    {
        "link": "https://www.quebecmedecin.com/medecin/medecin-begin-louis-r-9188.htm",
        "Doctor_name": "Dr Bégin Louis R.",
        "category": "Anatomopathologiste",
        "Address": "Hôpital du Sacré-Coeur de Montréal dép d'anatomo-pathologie 5400 boul Gouin O Montréal QC H4J 1C5 Canada",
        "phone_number": "514-338-2222 #2965",
        "Specialites": [
            "Anatomopathologiste"
        ],
        "permis": "76445",
        "Statut": " Inscrit ",
        "Assurance": " Avec assurance responsabilité professionnelle",
        "Recommandation": [
            {
                "name": "Sylvie Gagnon",
                "Date": "10 June 2023",
                "Description": "Super bon md , très dédié, vaillant , professionnel , fameux ..et tout ! À être très recommandé, .."
            },
            {
                "name": " Gagnon",
                "Date": "8 June 2023",
                "Description": " , très dédié, vaillant , professionnel , fameux ..et tout ! À être très recommandé, .."
            }
        ]
    },
    {
        "link": "https://www.quebecmedecin.com/medecin/medecin-temmar-rabia-2308.htm",
        "Doctor_name": "Dr Temmar Rabia",
        "category": "Anatomopathologiste",
        "Address": "CHUS - Hôpital Fleurimont 3001 12e Avenue N Sherbrooke QC J1H 5N4 Canada",
        "phone_number": "819-346-1110 #22908",
        "Specialites": [
            "Anatomopathologiste"
        ],
        "permis": "05302",
        "Statut": " Inscrit ",
        "Assurance": " Avec assurance responsabilité professionnelle",
        "Recommandation": [
            {
                "name": "AICHA",
                "Date": "11 July 2019",
                "Description": "Dr Temmar est très professionnel et d'une très grande compétence. Excellent médecin que je recommande vivement."
            }
        ]
    },
]

df = pd.DataFrame(data)

df = df.explode('Recommandation')

# Extract information from the nested "Recommandation" dictionary
df['Recommandation_Name'] = df['Recommandation'].apply(lambda x: x['name'] if isinstance(x, dict) else None)
df['Recommandation_Date'] = df['Recommandation'].apply(lambda x: x['Date'] if isinstance(x, dict) else None)
df['Recommandation_Description'] = df['Recommandation'].apply(lambda x: x['Description'] if isinstance(x, dict) else None)

# Drop the original "Recommandation" column
df = df.drop(columns=['Recommandation'])

# Convert the "Specialites" list to a string
df['Specialites'] = df['Specialites'].apply(lambda x: ', '.join(x) if isinstance(x, list) else None)

print(df)
df.to_csv('all.csv', index=False)