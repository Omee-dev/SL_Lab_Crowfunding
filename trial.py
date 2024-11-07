from flask import Flask, render_template, request, redirect, url_for
import csv
from pymongo import MongoClient

app = Flask(__name__)
#Static data so as to not needing access from real people and all are from unsplash.com
client = MongoClient('mongodb://localhost:27017/')
db = client['Crowdfund']
campaigns_collection = db['Campaigns']
campaigns= list(campaigns_collection.find())
@app.route('/')
def index():
    # Assuming the first campaign is the featured one for this example
    #featured_campaign = campaigns[0]
    return render_template('index.html', campaigns=campaigns)

@app.route('/campaign/<int:campaign_id>')
def campaign_page(campaign_id):
    campaign = next((c for c in campaigns if c['_id'] == campaign_id), None)
    if campaign:
        return render_template('campaign.html', campaign=campaign)
    else:
        return redirect(url_for('index'))

@app.route('/thankyou/<string:donor_name>')
def thankyou(donor_name):
    # Filter out the campaign that was just donated to (you might want to pass this info)
    other_campaigns = campaigns[:3]  # Just showing first 3 campaigns as suggestions
    return render_template('thankyou.html', donor_name=donor_name, other_campaigns=other_campaigns)
# @app.route('/donate/<int:campaign_id>', methods=['GET', 'POST'])
# def donate(campaign_id):
#     if request.method == 'POST':
#         name = request.form['name']
#         amount = float(request.form['amount'])
#         campaign = next((c for c in campaigns if c['id'] == campaign_id), None)
#         if campaign:
#             campaign['raised'] += amount
#             with open('donations.csv', 'a', newline='') as csvfile:
#                 writer = csv.writer(csvfile)
#                 writer.writerow([campaign['title'], name, amount])
#         return redirect(url_for('index'))
#     campaign = next((c for c in campaigns if c['id'] == campaign_id), None)
#     if campaign:
#         return render_template('donate.html', campaign=campaign)
#     else:
#         return redirect(url_for('index'))

@app.route('/donate/<int:campaign_id>', methods=['GET', 'POST'])
def donate(campaign_id):
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        campaign = next((c for c in campaigns if c['_id'] == campaign_id), None)
        if campaign:
            campaign['raised'] += amount
            with open('donations.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([campaign['title'], name, amount])
            return redirect(url_for('thankyou', donor_name=name))  #Changed this line
    campaign = next((c for c in campaigns if c['_id'] == campaign_id), None)
    if campaign:
        return render_template('donate.html', campaign=campaign)
    else:
        return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(debug=True)