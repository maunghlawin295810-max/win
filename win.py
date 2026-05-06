import os
import sys

def main():
    os.system('clear')
    # အရောင်နဲ့ Banner လှလှလေး ပေါ်အောင် လုပ်ထားပါတယ်
    print("\033[1;36m==================================")
    print("      WIN CUSTOM TOOL v1.0        ")
    print("      Created by Maung Hla Win    ")
    print("==================================\033[0m")
    
    print("\n[1] Termux Update လုပ်ရန်")
    print("[2] Storage ခွင့်ပြုချက်တောင်းရန်")
    print("[3] Tool မှ ထွက်ရန်")
    
    choice = input("\nနံပါတ်တစ်ခု ရွေးပါ (1/2/3): ")
    
    if choice == '1':
        print("\nစနစ်ကို Update လုပ်နေပါပြီ...")
        os.system('pkg update && pkg upgrade -y')
    elif choice == '2':
        os.system('termux-setup-storage')
    elif choice == '3':
        print("\nအသုံးပြုပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်!")
        sys.exit()
    else:
        print("\nမှားယွင်းနေပါသည်။ ပြန်စမ်းကြည့်ပါ။")
        main()

if __name__ == "__main__":
    main()
