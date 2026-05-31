from __future__ import annotations

from app.scheduler.job_runner import run_daily_job


def main() -> None:
    run_daily_job()


if __name__ == "__main__":
    main()
