#!/usr/bin/python3

import os
import smtplib

import job


def main():
    """Main function: collect available job offers links and send email then."""

    # Create a file if doesn't exists and doesn't overwrite if exists.
    filename = 'job_links_old'
    with open(filename, 'a') as file:
        pass

    job_links_old = job.read_job_links_from_file(filename)
    job_links = job.job_search(LOCATION, TECHNOLOGY)
    job_links_new = job_links - job_links_old
    job.write_job_links_to_file(filename, job_links)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = 'New job offers are available!'
        body = f'Hi me,\nI have found some new job {TECHNOLOGY.capitalize()} offers in {job.remove_accents(LOCATION)} for you:\n\n'
        if len(job_links_new) != 0:
            for job_link in job_links_new:
                body += f'{job_link}\n'

            msg = f'Subject: {subject}\n\n{body}'
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)


if __name__ == '__main__':
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    LOCATION = 'Wrocław'
    TECHNOLOGY = 'python'
    main()
