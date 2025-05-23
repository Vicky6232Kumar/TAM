import os

print("\nChoose an analysis to perform:")
print("1 - Effect of Gender on ADAS (Both Original & Perceived Data)")
print("2 - Effect of Age on ADAS (Both Original & Perceived Data)")
print("3 - Effect of Driving Experience of Drivers on ADAS (Both Original & Perceived Data)")
print("4 - Effect of Education on ADAS (Both Original & Perceived Data)")
print("5 - Effect of Crash Experience of Driver on ADAS (Both Original & Perceived Data)")
print("6 - Effect of Age x Gender on ADAS (Both Original & Perceived Data)")
print("7 - Effect of Age x Crash Experience on ADAS (Both Original & Perceived Data)")
print("8 - Effect of Age x Driver Education on ADAS (Both Original & Perceived Data)")
print("9 - Effect of Age x Drving Experience on ADAS (Both Original & Perceived Data)")
print("10 - Effect of Gender x Crash Experience on ADAS (Both Original & Perceived Data)")
print("11 - Effect of Gender x Driver Education on ADAS (Both Original & Perceived Data)")
print("12 - Effect of Gender x Driving Experience on ADAS (Both Original & Perceived Data)")
print("13 - Effect of Driving Experience x Crash Experience on ADAS (Both Original & Perceived Data)")
print("14 - Effect of Driving Experience x Driver Education on ADAS (Both Original & Perceived Data)")
print("15 - Effect of Driver Education x Crash Experience on ADAS (Both Original & Perceived Data)")
os.makedirs("plot", exist_ok=True)

choice = input("\nEnter your choice: ")

if choice == "1":
    os.system("python3 gender_effect_analysis.py")
elif choice == "2":
    os.system("python3 age_effect_analysis.py")
elif choice == "3":
    os.system("python3 driving_experience_analysis.py")
elif choice == "4":
    os.system("python3 education_effect_analysis.py")
elif choice == "5":
    os.system("python3 crash_experience_effect_analysis.py")
elif choice == "6":
    os.system("python3 age_gender_effect_analysis.py")
elif choice == "7":
    os.system("python3 age_crash_effect_analysis.py")
elif choice == "8":
    os.system("python3 age_education_effect_analysis.py")
elif choice == "9":
    os.system("python3 age_driving_effect_analysis.py")
elif choice == "10":
    os.system("python3 gender_crash_effect_analysis.py")
elif choice == "11":
    os.system("python3 gender_education_effect_analysis.py")
elif choice == "12":
    os.system("python3 gender_driving_effect_analysis.py")
elif choice == "13":
    os.system("python3 driving_crash_effect_analysis.py")
elif choice == "14":
    os.system("python3 driving_education_effect_analysis.py")
elif choice == "15":
    os.system("python3 education_crash_effect_analysis.py")
else:
    print("Invalid choice! Please run the script again.")
