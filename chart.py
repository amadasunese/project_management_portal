from models import User, db
from models import Project, Activity
from collections import defaultdict
import matplotlib.pyplot as plt

from flask import Flask, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

# # Dictionary to hold project budget and total approved activity budget
# project_budgets = defaultdict(lambda: {'project_amount': 0, 'approved_activity_budget': 0})

# # Populate the dictionary
# for project in Project.query.all():
#     project_budgets[project.id]['project_amount'] = project.project_amount
#     approved_activity_budget = sum(activity.approved_budget_amount for activity in project.activities)
#     project_budgets[project.id]['approved_activity_budget'] = approved_activity_budget

# # Calculate the percentage of expenditure
# for project_id, budgets in project_budgets.items():
#     expenditure_percentage = (budgets['approved_activity_budget'] / budgets['project_amount']) * 100 if budgets['project_amount'] > 0 else 0
#     project_budgets[project_id]['expenditure_percentage'] = expenditure_percentage

# At this point, 'project_budgets' contains all the data needed to create the chart

def get_project_data():
    from models import Project, Activity
    project_names = []
    expenditure_percentages = []

    projects = Project.query.all()  # Fetch all projects
    for project in projects:
        # Ensure there's a project amount to avoid division by zero
        if project.project_amount > 0:
            total_approved_budget = sum(activity.approved_budget_amount for activity in project.activities)
            expenditure_percentage = (total_approved_budget / project.project_amount) * 100

            project_names.append(project.name)
            expenditure_percentages.append(expenditure_percentage)

    return project_names, expenditure_percentages


@app.route('/dynamic_chart.png')
def dynamic_chart():
    # Assuming you have a function to calculate your data
    project_names, expenditure_percentages = get_project_data()

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(project_names, expenditure_percentages)
    axis.set_title('Project Expenditure as a Percentage of Total Budget')
    axis.set_ylabel('Percentage')
    axis.set_xticks(range(len(project_names)))
    axis.set_xticklabels(project_names, rotation=45, ha="right")

    # Convert plot to PNG image
    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)

    # Return PNG image as response
    return Response(png_image.getvalue(), mimetype='image/png')


# # Assuming you have fewer projects, or you'll filter them for this example
# project_names = [Project.query.get(pid).name for pid in project_budgets.keys()]
# expenditure_percentages = [info['expenditure_percentage'] for info in project_budgets.values()]

# plt.figure(figsize=(10, 8))
# plt.bar(project_names, expenditure_percentages, color='blue')
# plt.xlabel('Projects')
# plt.ylabel('Expenditure Percentage')
# plt.title('Project Expenditure as a Percentage of Total Budget')
# plt.xticks(rotation=45, ha="right")
# plt.tight_layout()

# plt.savefig('static/project_expenditure_chart.png')  # Saving the chart to be used in the Flask app
