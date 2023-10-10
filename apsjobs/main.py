from apscheduler.schedulers.background import BackgroundScheduler

from dashboard.schedulers import zoom_meeting_reminder, disable_unpaid_opportunities
from opportunity.schedulers import check_expired_opportunity


def start():
    print("Jobs Running...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(zoom_meeting_reminder, 'interval', minutes=31)
    scheduler.add_job(check_expired_opportunity, 'interval', minutes=60)
    scheduler.add_job(disable_unpaid_opportunities, 'interval', minutes=3)
    scheduler.start()
