from dbt.cli.main import dbtRunner, dbtRunnerResult
from loguru import logger


def run_dbt() -> None:
    logger.info("Running dbt")

    dbt = dbtRunner()

    cli_args = [
        "run",
        "--project-dir=src/transform/zurich_local",
        "--profiles-dir=src/transform/zurich_local",
    ]

    res: dbtRunnerResult = dbt.invoke(cli_args)

    for r in res.result:
        logger.info(f"{r.node.name}: {r.status}")


if __name__ == "__main__":
    run_dbt()
