
from pathlib import Path
from zipfile import ZipFile
from loguru import logger
import requests

def download():
    
    data_dir = Path('./data')

    try:

        for i in range(4, 13):
            dest_file = data_dir / f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2022_{i}.zip"
            r = requests.get(
                f"https://transtats.bts.gov/PREZIP/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2022_{i}.zip",
                verify=False,
                stream=True,
            )
    
            data_dir.mkdir(exist_ok=True)
    
            with dest_file.open('wb') as f:
                for chunk in r.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
                logger.debug('Downloaded file: {}', dest_file)
    
            with ZipFile(dest_file) as zf:
                zf.extract(zf.filelist[0].filename, path=data_dir)
                logger.debug('Extracted file: {}', data_dir / f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2022_{i}.csv")
    
    except Exception as e:
        print("An unexpected error occurred:", e)


if __name__ == '__main__':
    download()