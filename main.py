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
            visualizations()
        elif main_menu_choice == "4":
            pass
        elif main_menu_choice == "0":
            break


def visualizations():
    print("-------visualisations menu-------")
    while True:
        vis_menu_choice = input(
            "enter 0-3:\n 1.histogram for distribution of each city earthquakes magnitude\n 2.line graph for number of eqs per week or month and their mean magnitude\n 3.scatter graph for depth or magnitude per time\n 4. box plot for EQs magnitude per depth\n 5.heatmap for EQs locations\n 0. EXIT\n")
        if vis_menu_choice not in [str(i) for i in range(0, 6)]:
            raise ValueError(
                "Invalid choice. Please enter a number between 0 and 3.")
        elif vis_menu_choice == "1":
            pass
        elif vis_menu_choice == "2":
            pass
        elif vis_menu_choice == "3":
            pass
        elif vis_menu_choice == "4":
            pass
        elif vis_menu_choice == "5":
            pass
        elif vis_menu_choice == "0":
            break


main_panel()
