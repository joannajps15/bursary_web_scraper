from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timezone

import threading

from app import app, scrape, create_award_info_tables

worker_class = 'geventwebsocket.gunicorn.workers.GeventWebSocketWorker'
workers = 1
bind = '0.0.0.0:5000'
keepalive = 65

scheduler=None

# run functions on server start and exit through gunicorn master process
def on_starting(server):
    global scheduler
    
    # --- On Start App Configs ---
    def on_startup_setup():
        with app.app_context():
            try:
                create_award_info_tables() #ingest program-faculty table on start
                scrape() # run once on start
            except Exception as e:
                app.logger.error("Error during startup setup:", e)

    def scrape_job():
        with app.app_context():
            try:
                app.socketio.emit('scrape_status', {'status': 'true'})
                scrape()
                app.socketio.emit('scrape_status', {'status': 'false'})
            except Exception as e:
                app.socketio.emit('scrape_status', {'status': 'error'})
    
    on_startup_setup()

    # scrape cron job
    scheduler = BackgroundScheduler(timezone=timezone.utc)
    scheduler.add_job(scrape_job, 'cron', day=1, hour=0) # reschedule monthly
    scheduler.start()

def on_exit(server):
    if scheduler:
        scheduler.shutdown()