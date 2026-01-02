import json


with open("SniperHire-V1/api/resume_tailor/master_resume.json", "r") as file:
    master_resume = json.load(file)



print(master_resume)




if __name__ == "__main__":
    print("file: ", master_resume)