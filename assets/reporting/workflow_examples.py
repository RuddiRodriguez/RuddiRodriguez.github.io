"""Anonymised examples adapted from historical reporting scripts.

Names, paths, status codes, and configuration are generic. Supply your own
SQLAlchemy connections, SOAP client, authentication, and Excel template.
No private database or API is contacted when this module is imported.
"""
from pathlib import Path

import numpy as np
import pandas as pd

CALLBACK_QUERY = """
SELECT c.callback_id,
       c.scheduled_at,
       CAST(c.scheduled_at AS date) AS contact_date,
       a.account_id
FROM dbo.scheduled_callbacks AS c
LEFT JOIN dbo.accounts AS a
    ON SUBSTRING(c.attributes, 12, 10) = a.account_number
WHERE CAST(c.scheduled_at AS date) > :start_date
"""


def load_callbacks(connection, start_date):
    from sqlalchemy import text
    return pd.read_sql_query(
        text(CALLBACK_QUERY), connection,
        params={'start_date': start_date},
    )


def match_selection(callbacks, batches):
    selection = pd.concat(batches, ignore_index=True)
    return callbacks.merge(selection, on='account_id', how='inner')


def clean_tables(contacts, activities):
    contacts = contacts.copy()
    activities = activities.copy()
    contacts['account_id'] = contacts['account_id'].str.replace('-', '', regex=False)
    contacts['postal_code'] = contacts['postal_code'].str.replace(' ', '', regex=False)
    activities['postal_code'] = activities['postal_code'].str.replace(' ', '', regex=False)
    for column in ['contact_date', 'window_end']:
        contacts[column] = pd.to_datetime(contacts[column])
    activities['activity_date'] = pd.to_datetime(activities['activity_date'])
    return contacts, activities


def add_response_flags(matched):
    matched = matched.copy()
    responded = (
        matched['activity_date'].ge(matched['contact_date'])
        & matched['activity_date'].le(matched['window_end'])
        & matched['activity_id'].notna()
    )
    approved = responded & matched['decision'].eq('APPROVED')
    completed = responded & matched['status'].isin(['COMPLETED', 'FINALISED'])
    matched['responded'] = responded.astype(int)
    matched['approved'] = approved.astype(int)
    matched['completed'] = completed.astype(int)
    matched['response_days'] = np.where(
        responded,
        (matched['activity_date'] - matched['contact_date']).dt.total_seconds() / 86400,
        np.nan,
    )
    matched['completed_value'] = np.where(completed, matched['approved_value'], np.nan)
    return matched


def customer_campaign_rows(matched):
    return matched.groupby(
        ['contact_date', 'campaign', 'channel', 'customer_id'],
    ).agg({
        'contacted': 'max',
        'responded': 'max',
        'approved': 'max',
        'completed': 'max',
        'completed_value': 'max',
    }).reset_index()


def response_summary(customer_rows):
    summary = customer_rows.groupby(
        ['contact_date', 'campaign', 'channel'],
    ).agg({
        'contacted': 'sum',
        'responded': 'sum',
        'approved': 'sum',
        'completed': 'sum',
        'completed_value': 'sum',
    }).reset_index()
    summary['response_rate'] = summary['responded'] / summary['contacted']
    summary['year'] = summary['contact_date'].dt.year
    summary['month'] = summary['contact_date'].dt.month
    return summary


def prepare_reporting_tables(engine, sql_files):
    with engine.begin() as connection:
        for path in sql_files:
            sql = Path(path).read_text(encoding='utf-8-sig')
            connection.exec_driver_sql(sql)


def reminder_selection(selection, exclusions, closed_accounts):
    joined = selection.merge(exclusions, on='customer_id', how='left')
    joined = joined.merge(closed_accounts, on='customer_id', how='left')
    return joined.loc[
        joined['email_available'].eq(1)
        & joined['excluded'].isna()
        & joined['closed'].isna()
    ].copy()


def save_selection(selection, engine, table_name, output_file):
    selection.to_sql(table_name, con=engine, schema='dbo', index=False, if_exists='replace')
    selection.to_csv(output_file, index=False, sep=';')


def campaign_catalog(client, authentication):
    request = client.factory.create('GetCampaignsReq')
    request.header = authentication
    response = client.service.GetCampaigns(request)
    return pd.DataFrame({
        'campaign_id': [item[0] for item in response.campaignTypeItems],
        'campaign_name': [item[1] for item in response.campaignTypeItems],
        'sent_at': [item[3] for item in response.campaignTypeItems],
    })


def tracking_hits(client, authentication, campaign_id):
    request = client.factory.create('GetCampaignTrackingLinksReq')
    request.header = authentication
    request.campaignId = campaign_id
    response = client.service.GetCampaignTrackingLinks(request)
    return sum(item[3] for item in response.trackingLinkTypeItems)


def add_campaign_hits(campaigns, client, authentication):
    campaigns = campaigns.copy()
    campaigns['tracking_hits'] = [
        tracking_hits(client, authentication, campaign_id)
        for campaign_id in campaigns['campaign_id']
    ]
    campaigns['sent_at'] = pd.to_datetime(campaigns['sent_at'])
    campaigns['year'] = campaigns['sent_at'].dt.year
    campaigns['month'] = campaigns['sent_at'].dt.month
    return campaigns


def write_excel_template(summary, template_file, output_file):
    import xlwings as xw
    app = xw.App(visible=False)
    workbook = app.books.open(str(template_file))
    sheet = workbook.sheets['Data']
    sheet.range('A1').expand('table').clear_contents()
    sheet.range('A1').options(index=False, header=True).value = summary
    workbook.save(str(output_file))
    workbook.close()
    app.quit()


def export_report(summary, template_file, output_directory):
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_directory / 'response_summary.csv', index=False)
    write_excel_template(
        summary, template_file, output_directory / 'response_report.xlsx',
    )
