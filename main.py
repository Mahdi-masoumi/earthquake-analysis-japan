from emsc_crawler import run_emsc_scraper


def main_panel():
    while True:
        print("-------main menu-------")
        main_menu_choice = input(
            "enter 1-4:\n 1.get data\n 2.show query results\n 3.visualisations\n 4.unit testing\n")
        if main_menu_choice not in [str(i) for i in range(1, 5)]:
            raise ValueError(
                "Invalid choice. Please enter a number between 1 and 4.")
            break
        elif main_menu_choice == "1":
            run_emsc_scraper()


main_panel()
