from dags.src.database.database_management import DBConnection
from src.web_srapping.cv_online import CvOnline

db_conn = DBConnection()
print(db_conn.get_values_from_job_table())


# cv_online = CvOnline()
# cv_online.run_scrap()
