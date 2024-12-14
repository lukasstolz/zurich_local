import datetime
import re
from pathlib import Path
from time import sleep
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
from loguru import logger
from numpy.random import default_rng


def get_simple_timestamp_from_datetime(dt: datetime.datetime) -> str:
    return dt.strftime("%Y%m%d-%H%M%S")


def camel_to_snake(name: str) -> str:
    """Converts CamelCase strings to snake_case.

    Args:
        name (str): string you want to convert

    Returns:
        name (str): Passed string as camel_case
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    name = re.sub("[^0-9A-Za-z]+", r"_", name)
    return name


def get_character_replacement_dict() -> Dict[int, str]:
    character_replacement_dict = {
        "Ä": "Ae",
        "Ö": "Oe",
        "Ü": "Ue",
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
    }
    return {ord(k): v for k, v in character_replacement_dict.items()}


def normalize_string(string: str) -> str:
    """Converts string to standard form

    Normal form is defined as alphanumeric, lower case and containing only
    interior underscores, i.e. not on the edges.

    Args:
        string (str): string you want to convert

    Returns:
        string (str): Passed string in normal form
    """
    string = string.translate(get_character_replacement_dict())
    string = camel_to_snake(string)
    string = string.strip("_")

    return string


@logger.catch(reraise=True)
def load_environment_variables() -> None:
    """Load .env file in project root folder.

    Loads environment variables from .env file

    Args:
        None

    Raises:
        ValueError: If env_file is not a file
    """
    env_file = Path("./.env")

    if not env_file.is_file():
        raise ValueError("You need to add a .env file to the project root folder.")
    else:
        load_dotenv(env_file)


def get_week_start_date(yearweek: int) -> datetime.datetime:
    """
    Return date of starting the week (Monday)
    i.e: 201944 returns datetime.datetime(2019, 11, 4, 0, 0)

    %G -> ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V).
    %u -> ISO 8601 weekday as a decimal number where 1 is Monday.
    %V -> ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.

    Arguments:
        yearweek (int): year to be calculated

    Returns:
        datetime.datetime: Date of starting the week in passed year, week
    """
    return datetime.datetime.strptime(f"{yearweek}-1", "%G%V-%u")


def get_week_start_date_from_date(dt: datetime.datetime) -> datetime.datetime:
    """
    Return date of last Monday prior to input date
    i.e: '2022-01-21' returns datetime.datetime(2019, 11, 4, 0, 0)

    Args:
        dt (datetime.datetime): input date

    Returns:
        datetime.datetime: Date of last Monday prior to input date
    """

    return dt - datetime.timedelta(days=dt.weekday())


def get_year_week(dt: Union[datetime.datetime, datetime.date]) -> str:
    """
    Return yearwk of given week
    i.e: datetime.datetime(2019, 11, 4, 0, 0) returns 201944

    %G -> ISO 8601 year with century representing the year that contains the greater part of the ISO week (%V).
    %V -> ISO 8601 week as a decimal number with Monday as the first day of the week. Week 01 is the week containing Jan 4.

    Args:
        dt (Union[datetime.datetime, datetime.date]): Input datetime

    Returns:
        str: year week of the form YYYYWW
    """
    return dt.strftime("%G%V")


def get_current_year_week(weeks_offset: int = 0, today: Optional[Any] = None) -> int:
    """Return yearweek of current week or current week +/- year or week offset.

    Args:
        weeks_offset (int): Add or subtract weeks. Defaults to 0.
        today (Optional[str]): yearweek in format YYYYWW to be consider as today.
            When set to None the date of now is taken. Default to None.

    Returns:
        int: yearweek in format YYYYWW
    """

    if today is None:
        today = datetime.date.today()
    else:
        today = get_week_start_date(today)
    delta = datetime.timedelta(weeks=weeks_offset)

    date = today + delta
    year, week_num, _ = date.isocalendar()
    return int(f"{year}{week_num:02d}")


def random_sleep(max_wait_sec: int = 60) -> None:
    """Sleep for some max random time

    Args:
        max_wait_sec (int): max possible time to sleep for. Defaults to 60.
    """
    rng = default_rng()
    random_factor = rng.random()
    sleeping_time = random_factor * max_wait_sec

    logger.info(f"Sleeping for {sleeping_time} seconds")
    sleep(sleeping_time)
