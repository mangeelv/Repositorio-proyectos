import time
from grandprixs_reports import report_csvs
from pitstops_api import obtain_pitstops
from reports_pitstops_work import time_formater, reports_pits_merge, csv_concater


if __name__ == "__main__":
    t0 = time.time()

    report_csvs()
    obtain_pitstops()
    time_formater()
    reports_pits_merge()
    csv_concater()

    t1 = time.time()    
    print(f"Tiempo de ejecución: {t1-t0} segundos.")