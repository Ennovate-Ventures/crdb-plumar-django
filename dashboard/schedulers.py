from django.db import transaction
from django.utils import timezone

from dashboard.models import PackagePayment
from dashboard.utils import send_sms
from startups.models import ZoomMeeting
from userauth.utils import email_sender


def zoom_meeting_reminder():
    print("Zoom Meeting Scheduler Is Running...")
    waiting_meetings = ZoomMeeting.objects.filter(status="waiting", first_reminder_sent=False,
                                                  second_reminder_sent=False)
    print(f"Waiting Meetings: {waiting_meetings.count()}")
    for meeting in waiting_meetings:
        start_time = meeting.start_time
        now = timezone.now()
        difference = start_time - now
        seconds_in_day = 24 * 60 * 60

        minutes_diff = divmod(difference.days * seconds_in_day + difference.seconds, 60)[0]

        company = meeting.interviewer
        talent = meeting.interviewee

        try:

            if 1440 > minutes_diff > 30:
                # send sms and email to both talent and company
                # 1. send sms to talent
                send_sms(f"Hello, {talent.full_name}.\nYour have less than 24 hours to prepare for your interview "
                         f"meeting with {company.name.title()} for the opportunities you applied on plumar platform.\n"
                         f"Thanks and All the best.", [talent.phone])

                # 2. send sms to company
                send_sms(f"Hello, {company.name.title()}.\nYour have less than 24 hours to prepare for your interview "
                         f"meeting with {talent.full_name} for the opportunities you posted on plumar platform.\n"
                         f"Thanks and All the best.", [company.phone_number])

                # 3. send email to talent
                email_sender(talent.user.email, "Plumar Interview Reminder",
                             f"Hello, {talent.user.username}.\nYour have less than 24 hours to prepare for your interview "
                             f"meeting with {company.name.title()} for the opportunities you applied on plumar platform.\n"
                             f"Thanks and All the best.")

                # 4. send email to company
                email_sender(company.user.email, "Plumar Interview Reminder",
                             f"Hello, {company.name.title()}.\nYour have less than 24 hours to prepare for your interview "
                             f"meeting with {talent.full_name} for the opportunities you posted on plumar platform.\n"
                             f"Thanks and All the best.")
                meeting.first_reminder_sent = True
                meeting.save()

            elif minutes_diff < 1440 and minutes_diff < 30:
                send_sms(f"Hello, {talent.user.username}.\nYour interview meeting with {company.name.title()} for the "
                         f"opportunities you applied on plumar platform starts in 30 minutes.\nJoin Link: "
                         f"{meeting.join_url}\n Password: {meeting.password}\n"
                         f"Thanks and All the best.", [talent.phone])

                # 2. send sms to company
                send_sms(f"Hello, {company.name.title()}.\nYour interview meeting with {talent.full_name} for the "
                         f"opportunities you applied on plumar platform starts in 30 minutes.\nJoin Link: "
                         f"{meeting.join_url}\n Password: {meeting.password}\n"
                         f"Thanks and All the best.", [company.phone_number])

                # 3. send email to talent
                email_sender(talent.user.email, "Plumar Interview Reminder",
                             f"Hello, {talent.user.username}.\nYour interview meeting with {company.name.title()} for the "
                             f"opportunities you applied on plumar platform starts in 30 minutes.\nJoin Link: "
                             f"{meeting.join_url}\n Password: {meeting.password}\n"
                             f"Thanks and All the best.")

                # 4. send email to company
                email_sender(company.user.email, "Plumar Interview Reminder",
                             f"Hello, {company.name.title()}.\nYour interview meeting with {talent.full_name} for the "
                             f"opportunities you applied on plumar platform starts in 30 minutes.\nJoin Link: "
                             f"{meeting.join_url}\n Password: {meeting.password}\n"
                             f"Thanks and All the best.")
                meeting.second_reminder_sent = True
                meeting.save()
        except Exception as e:
            print(e.__str__())
            continue


def disable_unpaid_opportunities():
    print("Checking for unpaid opportunities")
    payments = PackagePayment.objects.filter(active_payment=True, verified=False)

    with transaction.atomic(savepoint=True):
        for payment in payments:
            if payment.matched_count > 0 and not payment.closed:
                for opportunity in payment.opportunities.all():
                    opportunity.active = False
                    opportunity.save()
