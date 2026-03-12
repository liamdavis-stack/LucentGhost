from glassbit import run_glassbit

def banner():
    print("=" * 54)
    print("LUCENTGHOST v0.2".center(54))
    print("=" * 54)

def main():
    while True:
        banner()
        print("[1] Map Randomizer: 777")
        print("[2] Map Randomizer: 12-14-17-21")
        print("[3] List WADs")
        print("[4] HillGenPro receipt demo")
        print("[5] Empyrean Winter: Anathema")
        print("[6] Lucent-C")
        print("[7] TempleBuilderPlus")
        print("[8] GlassBitToolKit")
        print("[0] Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            print("Map Randomizer: 777 placeholder")
        elif choice == "2":
            print("Map Randomizer: 12-14-17-21 placeholder")
        elif choice == "3":
            print("List WADs placeholder")
        elif choice == "4":
            print("HillGenPro receipt demo placeholder")
        elif choice == "5":
            print("Empyrean Winter: Anathema placeholder")
        elif choice == "6":
            print("Lucent-C placeholder")
        elif choice == "7":
            print("TempleBuilderPlus placeholder")
        elif choice == "8":
            run_glassbit()
        elif choice == "0":
            print("Exiting LucentGhost.")
            break
        else:
            print("Invalid choice.")
        print()

if __name__ == "__main__":
    main()
