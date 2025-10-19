from scraping import scrape
from final_Preprocessing import preprocessing
from db_create_read import run_database_final
from data_analysis import plot_histogram, plot_line, plot_scatter, plot_boxplot, plot_heatmap
import test
import unittest
import os


def run_tests():
    print("🔍 Running unit tests...\n")
    loader = unittest.TestLoader()
    tests = loader.discover(
        start_dir=os.path.dirname(__file__), pattern="test.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(tests)
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed. Check details above.")


def main_panel():
    data_ready = False
    db_ready = False

    while True:
        print("-------main menu-------")
        main_menu_choice = input(
            "enter 0-4:\n 1.get data\n 2.show query results\n 3.visualisations\n 4.unit testing\n 0.EXIT\n"
        )

        if main_menu_choice not in [str(i) for i in range(0, 5)]:
            raise ValueError(
                "Invalid choice. Please enter a number between 0 and 4.")

        elif main_menu_choice == "1":
            scrape()
            preprocessing()
            data_ready = True

        elif main_menu_choice == "2":
            # if not data_ready:
            #     print("⚠️ You must run data collection (option 1) first.")
            #     continue
            run_database_final()
            # db_ready = True

        elif main_menu_choice == "3":
            # if not (data_ready and db_ready):
            #     print("⚠️ Please complete steps 1 and 2 before visualisations.")
            #     continue
            visualizations()

        elif main_menu_choice == "4":
            run_tests()

        elif main_menu_choice == "0":
            break


def visualizations():
    print("-------visualisations menu-------")
    while True:
        vis_menu_choice = input(
            "enter 0-3:\n 1.histogram for distribution of each city earthquakes magnitude\n 2.line graph for number of eqs per week or month and their mean magnitude\n 3.scatter graph for depth or magnitude per time\n 4. box plot for EQs magnitude per depth\n 5.heatmap for EQs locations\n 0. EXIT\n")
        if vis_menu_choice not in [str(i) for i in range(0, 6)]:
            raise ValueError(
                "Invalid choice. Please enter a number between 0 and 5.")
        elif vis_menu_choice == "1":
            plot_histogram()
        elif vis_menu_choice == "2":
            plot_line(freq="D")
        elif vis_menu_choice == "3":
            plot_scatter("depth", "magnitude", "scatter_depth_mag.png")
            plot_scatter("time", "magnitude", "scatter_time_mag.png")
        elif vis_menu_choice == "4":
            plot_boxplot()
        elif vis_menu_choice == "5":
            plot_heatmap()
        elif vis_menu_choice == "0":
            break


main_panel()
