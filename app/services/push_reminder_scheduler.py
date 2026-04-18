import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

from app.config import settings
from app.crud.depression_test import has_user_submitted_test_on_date
from app.database import SessionLocal
from app.models.user import User
from app.services.push_notification_service import PushSendResult, send_push_notification

logger = logging.getLogger(__name__)

_scheduler = None


def _today_in_configured_timezone() -> date:
    tz = ZoneInfo(settings.TIMEZONE)
    return datetime.now(tz).date()


def run_daily_depression_test_push_job() -> None:
    if not settings.PUSH_REMINDER_ENABLED:
        logger.info("push_reminder_status=disabled")
        return

    db: Session = SessionLocal()

    try:
        today_local = _today_in_configured_timezone()
        counters = {
            "sent": 0,
            "skipped_completed_today": 0,
            "skipped_no_token": 0,
            "skipped_push_disabled": 0,
            "skipped_already_sent_today": 0,
            "invalid_token": 0,
            "failed_send": 0,
        }

        users = db.query(User).all()

        for user in users:
            if not user.is_push_reminder_enabled:
                counters["skipped_push_disabled"] += 1
                logger.info("push_reminder user_id=%s status=skipped_push_disabled", user.id)
                continue

            token = (user.fcm_token or "").strip()
            if not token:
                counters["skipped_no_token"] += 1
                logger.info("push_reminder user_id=%s status=skipped_no_token", user.id)
                continue

            if user.last_push_reminder_date == today_local:
                counters["skipped_already_sent_today"] += 1
                logger.info("push_reminder user_id=%s status=skipped_already_sent_today", user.id)
                continue

            completed_today = has_user_submitted_test_on_date(
                db=db,
                user_id=user.id,
                local_date=today_local,
                timezone_name=settings.TIMEZONE,
            )
            if completed_today:
                counters["skipped_completed_today"] += 1
                logger.info("push_reminder user_id=%s status=skipped_completed_today", user.id)
                continue

            result = send_push_notification(
                token=token,
                title="Daily Reminder",
                body="Please complete today's depression test.",
                data={"screen": "depression-test"},
            )

            if result == PushSendResult.SENT:
                user.last_push_reminder_date = today_local
                counters["sent"] += 1
                logger.info("push_reminder user_id=%s status=sent", user.id)
            elif result == PushSendResult.INVALID_TOKEN:
                user.fcm_token = None
                counters["invalid_token"] += 1
                logger.info("push_reminder user_id=%s status=invalid_token", user.id)
            else:
                counters["failed_send"] += 1
                logger.info("push_reminder user_id=%s status=failed_send", user.id)

        db.commit()
        logger.info(
            "push_reminder_summary date=%s sent=%s skipped_completed_today=%s skipped_no_token=%s "
            "skipped_push_disabled=%s skipped_already_sent_today=%s invalid_token=%s failed_send=%s",
            today_local,
            counters["sent"],
            counters["skipped_completed_today"],
            counters["skipped_no_token"],
            counters["skipped_push_disabled"],
            counters["skipped_already_sent_today"],
            counters["invalid_token"],
            counters["failed_send"],
        )
    except Exception as exc:
        db.rollback()
        logger.error("Daily push reminder job failed: %s", exc, exc_info=True)
    finally:
        db.close()


def start_push_reminder_scheduler() -> None:
    global _scheduler

    if _scheduler is not None:
        return

    timezone = ZoneInfo(settings.TIMEZONE)
    _scheduler = BackgroundScheduler(timezone=timezone)
    _scheduler.add_job(
        run_daily_depression_test_push_job,
        CronTrigger(hour=settings.PUSH_REMINDER_HOUR, minute=settings.PUSH_REMINDER_MINUTE, timezone=timezone),
        id="daily_depression_test_push_reminder",
        replace_existing=True,
    )
    _scheduler.start()


def stop_push_reminder_scheduler() -> None:
    global _scheduler

    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
