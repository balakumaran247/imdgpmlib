import requests, os
from datetime import datetime
from datetime import timedelta as td
from typing import Optional, Iterator


class IMD:

    __IMDURL = {
        "raingpm": "https://www.imdpune.gov.in/Seasons/Temperature/gpm/",
        "tmax": "https://www.imdpune.gov.in/Seasons/Temperature/max/",
        "tmin": "https://www.imdpune.gov.in/Seasons/Temperature/min/",
        "rain": "https://www.imdpune.gov.in/Seasons/Temperature/Rainfall/",
        "tmaxone": "https://www.imdpune.gov.in/Seasons/Temperature/max/",
        "tminone": "https://www.imdpune.gov.in/Seasons/Temperature/min/",
    }  # https://www.imdpune.gov.in/Seasons/Temperature/temp.html
    __IMDFMT = {
        "raingpm": ("", "%d%m%Y", "raingpm_"),
        "tmax": ("max", "%d%m%Y", "tmax_"),
        "tmin": ("min", "%d%m%Y", "tmin_"),
        "rain": ("rain_ind0.25_", "%y_%m_%d", "rain_"),
        "tmaxone": ("max1_", "%d%m%Y", "tmaxone_"),
        "tminone": ("min1_", "%d%m%Y", "tminone_"),
    }

    def __init__(self, var_type: str) -> None:
        self.var_type = var_type
        self.__imdurl = IMD.__IMDURL[self.var_type]
        self.__pfx, self.__dtfmt, self.__opfx = IMD.__IMDFMT[self.var_type]

    def _download_grd(self, date: datetime, path: str) -> Optional[str]:
        url = f"{self.__imdurl}{self.__pfx}{date.strftime(self.__dtfmt)}.grd"
        filename = f"{self.__opfx}{date.strftime('%Y%m%d')}.grd"
        out_file = os.path.join(path, filename)
        if os.path.exists(out_file):
            return filename
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            return filename
        with open(out_file, "wb") as f:
            f.write(r.content)
        return None

    def _check_path(self, path: str) -> str:
        check_path = os.path.normpath(path)
        if not os.path.isdir(check_path):
            raise OSError(f"{check_path} does not exist.")
        return check_path

    def _check_dates(self, start_date: datetime, end_date: datetime) -> datetime:
        self.__imd_first_date = {
            "raingpm": datetime.strptime('20151001', '%Y%m%d'),
            "tmax": datetime.strptime('20150601','%Y%m%d'),
            "tmin": datetime.strptime('20150601','%Y%m%d'),
            "rain": datetime.strptime('20181209', '%Y%m%d'),
            "tmaxone": datetime.strptime('20190101','%Y%m%d'),
            "tminone": datetime.strptime('20190101','%Y%m%d'),
        }
        self.__first_date = self.__imd_first_date[self.var_type]
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        if self.__first_date > start_date:
            raise ValueError(
                f'Data available after {self.__first_date.strftime("%Y-%m-%d")}')
        return start_date, end_date

    def _dtrgen(self, start: datetime, end: datetime) -> Iterator[datetime]:
        return ((start+td(days=x)) for x in range((end-start).days+1))

# class MultiDateData(IMD):
#     """get the start date and end date as datetime and path
#     loop through the dates and call download_grd
#     and assign download_failed
#     also check if file aready exist and assign skipped"""
#     pass