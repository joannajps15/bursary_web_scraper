from app import test
from flask import render_template, request, flash, redirect, url_for, send_file
from app.forms import EnterData

import subprocess
import os
import sys
import scrape

#main route!!
@test.route('/', methods=['GET', 'POST'])
def index():
    title = {'words': 'UW SAFA Database Web-Scraper'}
    form = EnterData()

    if request.method == 'POST' and form.validate():

        #process form values
        year = form.year.data
        term = form.term.data
        program = form.program.data
        athlete = str(form.athlete.data)

        # Run the Python script using subprocess, so it is compatible with Windows
        python_executable = sys.executable  # Get the path to the current Python executable
        script_path = os.path.join(os.getcwd(), "scrape.py")  # Full path to the script

        # Run the script
        subprocess.run([python_executable, script_path, year, term, program, athlete], shell=True, check=True)
        

        # Flash a success message
        flash('Script has been run successfully! The file is ready for download.')

        #Re-Direct page
        return redirect(url_for('download'))


    return render_template('form.html', title=title, form=form)

@test.route('/download')
def download():
    path = os.path.join(os.getcwd(), "test.xlsx")
    return send_file(path, as_attachment=True)

