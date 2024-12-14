import yaml
from loguru import logger

import airbyte as ab


def get_zurich_source(streams: str = "*") -> ab.Source:
    logger.info("Loading Zurich Data Source")

    with open("airbyte/sources/stadt_zuerich.yaml") as stream:
        try:
            source_manifest = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(f"Failed to load Zurich Source YAML: {exc}")

    source = ab.get_source(
        "stadt_zuerich", config={}, source_manifest=source_manifest, streams=streams
    )

    source.check()
    return source


def read_source(source: ab.Source) -> ab.ReadResult:
    logger.info("Read Zurich Data Source")

    res = source.read()
    return res


def get_md_destination(destination_path: str = "md:zuerich_db") -> ab.Destination:
    logger.info("Loading MotherDuck Destination")

    md_destination = ab.get_destination(
        "destination-motherduck",
        config={
            "motherduck_api_key": ab.get_secret("MD_ACCESS_TOKEN"),
            "destination_path": destination_path,
            "schema": "raw",
        },
    )

    md_destination.check()

    return md_destination


def write_destination(destination: ab.Destination, res: ab.ReadResult) -> None:
    logger.info("Writing to MotherDuck Destination")

    destination.write(res)


def load_data() -> None:
    source = get_zurich_source("shopping")
    destination = get_md_destination()

    source_results = read_source(source)
    write_destination(destination=destination, res=source_results)


if __name__ == "__main__":
    load_data()
