# from flask import render_template
# from flask_login import login_required
# from views import main, db
# from models import Project, Activity, Report, FinancialReport  # Make sure these are imported correctly
# from .utils import render_pdf  # Assuming this utility function is defined to handle PDF rendering
# from flask_weasyprint import HTML, render_pdf

# @main.route('/generate_pdf_project_report')
# @login_required
# def generate_pdf_project_report():
#     projects = Project.query.all()
#     html = render_template('pdf_report_project_template.html', projects=projects)
    
#     return render_pdf(HTML(string=html))


# @main.route('/generate_pdf_activity_report')
# @login_required
# def generate_pdf_activity_report():
#     activities = Activity.query.all()
    
#     html = render_template('reports/pdf_report_activity_template.html', activities=activities) 

#     return render_pdf(HTML(string=html))

# @main.route('/generate_pdf_report')
# @login_required
# def generate_report():
#     reports = Report.query.all()
    
#     html = render_template('pdf_report_activity_template.html', reports=reports,) 

#     return render_pdf(HTML(string=html))