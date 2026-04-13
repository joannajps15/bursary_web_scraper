from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timezone

import logging

from app import app, scrape
from routes.create_award_info_tables import *
from routes.create_scrape_result_tables import *

worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
workers = 1
bind = '0.0.0.0:5000'
keepalive = 65

logger = logging.getLogger('gunicorn.error')
scheduler = None

# run functions on server start and exit through gunicorn master process
def on_starting(server):
    global scheduler
    
    # --- On Start App Configs ---
    def on_startup_setup():
        with app.app_context():
            try:
                create_award_info_tables() #ingest program-faculty table on start
                logger.info("Program-faculty tables created successfully.")
                create_scrape_result_tables() # create tables for scraped data on start
                logger.info("Scrape result tables created successfully.")
                logger.info("Running initial scrape on startup...")
                scrape() # run once on start
            except Exception as e:
                logger.error("Error during startup setup:", e)

    def scrape_job():
        with app.app_context():
            try:
                app.socketio.emit('scrape_status', {'status': 'true'})
                scrape()
                app.socketio.emit('scrape_status', {'status': 'false'})
            except Exception as e:
                app.socketio.emit('scrape_status', {'status': 'error'})
    
    logging.info("Starting server and running startup setup...")
    on_startup_setup()
    logging.info("Startup setup completed. Server is ready to accept requests.")   

    # scrape cron job
    scheduler = BackgroundScheduler(timezone=timezone.utc)
    scheduler.add_job(scrape_job, 'cron', day=1, hour=0) # reschedule monthly
    scheduler.start()

def on_exit(server):
    if scheduler:
        scheduler.shutdown()