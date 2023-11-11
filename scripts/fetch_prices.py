import argparse
import datetime
import logging
import re
import subprocess
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Update commodity prices in ledger",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--commodities-path",
        required=True,
        help="""Path to the commodities file. Must follow beancount commodity format with `price` metadata. For example:
    ```
    2019-01-01 commodity USD
        price: "EUR:yahoo/USDEUR=X"
    2020-08-01 commodity BTC
        price: "EUR:coinbase/BTC-EUR USD:coinbase/BTC-USD"
    ```
        """,
    )
    parser.add_argument(
        "-s",
        "--beanprice-script-path",
        required=True,
        help="Path to the bean-price script",
    )
    parser.add_argument(
        "-p", "--prices-path", required=True, help="Path to the prices file"
    )
    parser.add_argument(
        "--start-date", help="Start date for price updates (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        default=datetime.date.today() - datetime.timedelta(days=2),
        help="End date for price updates (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
    )
    return parser.parse_args()


def configure_logging(log_level):
    logging.basicConfig(level=log_level)
    return logging.getLogger(__name__)


def determine_start_date(prices_path):
    date_template = "([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
    with open(prices_path, "r") as f:
        for line in reversed(f.readlines()):
            x = re.search(date_template, line)
            if x:
                try:
                    return datetime.datetime.strptime(x.group(1), "%Y-%m-%d").date() + datetime.timedelta(days=1)
                except ValueError:
                    continue
    return None


def update_prices(
    beanprice_script_path, commodities_path, start_date, end_date, logger
):
    delta = datetime.timedelta(days=1)
    date = start_date
    output = ""
    cmd = [
        str(beanprice_script_path),
        str(commodities_path),
        "--date",
        date.strftime("%Y-%m-%d"),
        "-i",
    ]

    while date <= end_date:
        try:
            cmd[3] = date.strftime("%Y-%m-%d")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output += result.stdout + "\n"
            logger.info(f"Updated prices for {date}")
            date += delta
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update prices for {date}: {e}")
            break
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break

    return output


def write_to_file(prices_path, output, logger):
    try:
        with open(prices_path, "a") as f:
            f.write(output)
        logger.info("Price update completed successfully.")
    except Exception as e:
        logger.error(f"Failed to write to file: {e}")


if __name__ == "__main__":
    args = parse_arguments()
    logger = configure_logging(args.log_level)

    commodities_path = Path(args.commodities_path).resolve()
    beanprice_script_path = Path(args.beanprice_script_path).resolve()
    prices_path = Path(args.prices_path).resolve()

    if not commodities_path.exists():
        logger.error(f"Commodities file not found at {commodities_path}")
        exit(1)
    if not beanprice_script_path.exists():
        logger.error(f"Bean-price script not found at {beanprice_script_path}")
        exit(1)
    if not prices_path.exists():
        logger.error(f"Prices file not found at {prices_path}")
        exit(1)

    end_date = args.end_date
    start_date = (
        args.start_date if args.start_date else determine_start_date(prices_path)
    )
    if not start_date:
        logger.error("Failed to determine start date for price updates.")
        logger.error(
            "Please specify a start date using the --start-date option. (YYYY-MM-DD)"
        )
        exit(1)

    output = update_prices(
        beanprice_script_path, commodities_path, start_date, end_date, logger
    )
    write_to_file(prices_path, output, logger)
