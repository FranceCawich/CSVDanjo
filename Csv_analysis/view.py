from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        data = pd.read_csv(uploaded_file)

        # Perform analysis and create the first chart
        passing_mark = 70
        passed_students = data[data['mark'] >= passing_mark]
        gender_count = passed_students['gender'].value_counts()

        plt.figure(figsize=(6, 6))
        plt.subplot(1, 2, 1)
        gender_count.plot(kind='pie')
        plt.xlabel('Gender')
        plt.ylabel('Number of Students')
        plt.title('Number of Males and Females Who Passed')

        # Perform analysis and create the second chart
        data['pass_status'] = data['mark'].apply(lambda x: 'Passed' if x >= passing_mark else 'Failed')
        status_counts = data['pass_status'].value_counts()

        plt.subplot(1, 2, 2)
        status_counts.plot(kind='bar')
        plt.xlabel('Pass Status')
        plt.ylabel('Number of Students')
        plt.title('Number of Students Who Passed and Failed')

        # Convert the charts to a base64-encoded image string
        chart1 = io.BytesIO()
        plt.savefig(chart1, format='png')
        chart1.seek(0)
        chart_data1 = base64.b64encode(chart1.read()).decode('utf-8')

        chart2 = io.BytesIO()
        plt.savefig(chart2, format='png')
        chart2.seek(0)
        chart_data2 = base64.b64encode(chart2.read()).decode('utf-8')

        # Render the template with the chart images
        return render(request, 'result.html', {'chart_data1': chart_data1, 'chart_data2': chart_data2})

    return render(request, 'upload.html')
