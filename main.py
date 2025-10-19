from scraping import scrape
from final_Preprocessing import preprocessing
from db_create_read import run_database_final


def main_panel():
    while True:
        print("-------main menu-------")
        main_menu_choice = input(
            "enter 0-4:\n 1.get data\n 2.show query results\n 3.visualisations\n 4.unit testing\n 0.EXIT\n")
        if main_menu_choice not in [str(i) for i in range(0, 5)]:
            raise ValueError(
                "Invalid choice. Please enter a number between 0 and 4.")
        elif main_menu_choice == "1":
            scrape()
            preprocessing()
        elif main_menu_choice == "2":
            run_database_final()
        elif main_menu_choice == "3":
            pass
        elif main_menu_choice == "4":
            pass
        elif main_menu_choice == "0":
            break


main_panel()
