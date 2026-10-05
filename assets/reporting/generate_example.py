"""Generate a small report from invented records. Run with pandas and numpy installed."""
from pathlib import Path

import pandas as pd
import workflow_examples as m

contacts=pd.DataFrame([dict(customer_id=f'C{i:03}',account_id=f'000-{i:03}',postal_code='1000 AA',contact_date='2024-01-10',window_end='2024-01-20',campaign='Campaign A' if i<=4 else 'Campaign B',channel='Email' if i<=4 else 'Phone',contacted=1) for i in range(1,9)])
activities=pd.DataFrame([dict(customer_id=f'C{i:03}',activity_id=n,activity_date=date,postal_code='1000 AA',decision=decision,status=status,approved_value=value) for n,(i,date,decision,status,value) in enumerate([(1,'2024-01-12','APPROVED','COMPLETED',100),(1,'2024-01-13','APPROVED','COMPLETED',150),(2,'2024-01-15','DECLINED','OPEN',0),(3,'2024-02-01','APPROVED','COMPLETED',100),(5,'2024-01-11','APPROVED','COMPLETED',200),(6,'2024-01-16','APPROVED','OPEN',150)],1)])
contacts,activities=m.clean_tables(contacts,activities)
matched=m.add_response_flags(contacts.merge(activities.drop(columns='postal_code'),on='customer_id',how='left'))
summary=m.response_summary(m.customer_campaign_rows(matched))
summary.to_csv(Path(__file__).with_name('example_response_summary.csv'), index=False)
print(summary.to_string(index=False))
