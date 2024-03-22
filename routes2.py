@main.route('/project', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        new_project = Project(
            name=request.form['name'],
            donor=request.form['donor'],
            thematic_area=request.form['thematic_area'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            project_amount=float(request.form['project_amount'])
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('main.project'))

    projects = Project.query.all()
    return render_template('project.html', projects=projects)


@main.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.donor = request.form['donor']
        project.thematic_area = request.form['thematic_area']
        project.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        project.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        project.project_amount = float(request.form['project_amount'])

        db.session.commit()
        return redirect(url_for('main.project'))  # Replace with your view function

    return render_template('edit_project.html', project=project)



@main.route('/delete_project/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.project'))



# Activities Routes
@main.route('/activity', methods=['GET', 'POST'])
def activity():
    if request.method == 'POST':
        new_activity = Activity(
            project_id=request.form['project_id'],
            name=request.form['name'],
            target_beneficiaries=request.form['target_beneficiaries'],
            target_beneficiaries_male=int(request.form['target_beneficiaries_male']),
            target_beneficiaries_female=int(request.form['target_beneficiaries_female']),
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            budget_amount=float(request.form['budget_amount']),
            approved_budget_amount=float(request.form['approved_budget_amount'])
        )
        db.session.add(new_activity)
        db.session.commit()
        return redirect(url_for('main.activity'))

    activities = Activity.query.all()
    return render_template('activity.html', activities=activities)


@main.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        written_report_file = request.files.get('written_report')
        photos_file = request.files.get('photos')

        written_report_path = None
        photos_path = None

        if written_report_file:
            written_report_filename = secure_filename(written_report_file.filename)
            written_report_file.save(os.path.join(app.config['UPLOAD_FOLDER'], written_report_filename))
            written_report_path = os.path.join(app.config['UPLOAD_FOLDER'], written_report_filename)

        if photos_file:
            photos_filename = secure_filename(photos_file.filename)
            photos_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photos_filename))
            photos_path = os.path.join(app.config['UPLOAD_FOLDER'], photos_filename)

        new_report = Report(
            activity_id=request.form['activity_id'],
            donor=request.form['donor'],
            date_from=datetime.strptime(request.form['date_from'], '%Y-%m-%d'),
            date_to=datetime.strptime(request.form['date_to'], '%Y-%m-%d'),
            number_reached_male=int(request.form['number_reached_male']),
            number_reached_female=int(request.form['number_reached_female']),
            written_report=written_report_path,
            photos=photos_path
        )
        db.session.add(new_report)
        db.session.commit()
        return redirect(url_for('main.report'))

    reports = Report.query.all()
    return render_template('report.html', reports=reports)

@main.route('/edit_report/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    report = Report.query.get_or_404(report_id)

    written_report_path = None
    photos_path = None

    if request.method == 'POST':
        # Assuming your report model has fields such as donor, date_from, etc.
        report.donor = request.form['donor']
        report.start_date = datetime.strptime(request.form['date_from'], '%Y-%m-%d')
        report.end_date = datetime.strptime(request.form['date_to'], '%Y-%m-%d')
        report.number_reached_male=int(request.form['number_reached_male'])
        report.number_reached_female=int(request.form['number_reached_female'])
        report.written_report=written_report_path
        report.photos=photos_path
        # ... handle other fields similarly

        db.session.commit()
        flash('Report updated successfully!', 'success')
        return redirect(url_for('main.report'))  # Replace with your actual list view route

    return render_template('edit_report.html', report=report)



@main.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)

    db.session.delete(report)
    db.session.commit()
    flash('Report deleted successfully!', 'info')
    return redirect(url_for('main.report'))  # Replace with your actual list view route




# Financial Report Routes
@main.route('/financial_report', methods=['GET', 'POST'])
def financial_report():
    if request.method == 'POST':
        new_financial_report = FinancialReport(
            project_id=request.form['project_id'],
            activity_id=request.form['activity_id'],
            budget=float(request.form['budget']),
            expenditure=float(request.form['expenditure'])
        )
        db.session.add(new_financial_report)
        db.session.commit()
        return redirect(url_for('main.financial_report'))

    financial_reports = FinancialReport.query.all()
    return render_template('financial_report.html', financial_reports=financial_reports)

@main.route('/analysis')
def analysis():
    # Example of fetching data for analysis
    project_count = Project.query.count()
    total_budget = db.session.query(db.func.sum(Project.project_amount)).scalar()
    
    # More complex queries can be added here for detailed analysis
    
    return render_template('analysis.html', project_count=project_count, total_budget=total_budget)



@main.route('/generate_pdf_report')
def generate_pdf_report():
    # Fetch data for the report
    projects = Project.query.all()
    
    # Render a HTML template with this data
    html = render_template('pdf_report_template.html', projects=projects)
    
    # Convert HTML to PDF
    return render_pdf(HTML(string=html))


@main.route('/generate_excel_report')
def generate_excel_report():
    # Fetch data for the report
    projects = Project.query.all()

    # Convert data to a DataFrame
    data = [{'donor': project.donor, 'thematic_area': project.thematic_area, 'start_date': project.start_date, 'end_date': project.end_date, 'project_amount': project.project_amount } for project in projects]  # Add all relevant fields
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')

    # Get the Excel file content
    excel_data = output.getvalue()

    # Return the Excel file in the response
    return Response(
        excel_data,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment;filename=report.xlsx"}
    )


@main.route('/generate_word_report')
def generate_word_report():
    # Fetch data for the report
    projects = Project.query.all()

    # Create a Word document
    doc = Document()
    doc.add_heading('Project Report', level=1)

    # Define table headers
    headers = ['Project ID', 'Project Name', 'Donor', 'Thematic Area', 'Project Start Date', 'Project End Date', 'Project Amount']

    # Add a table to the document
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = 'Table Grid'  # Add basic style to the table

    # Populate header row
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        hdr_cells[i].text = header

    # Add data to the table
    for project in projects:
        row_cells = table.add_row().cells
        row_cells[0].text = str(project.id)
        row_cells[1].text = project.name
        row_cells[2].text = project.donor  # Assuming 'donor' is a string
        row_cells[3].text = project.thematic_area  # Assuming 'thematic_area' is a string
        row_cells[4].text = project.start_date.strftime('%Y-%m-%d')  # Format the date
        row_cells[5].text = project.end_date.strftime('%Y-%m-%d')    # Format the date
        row_cells[6].text = str(project.project_amount)  # Convert float to string
    


    # Save the document in memory
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    # Return the Word document as a response
    return send_file(
        file_stream,
        as_attachment=True,
        download_name='project_report.docx',
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'