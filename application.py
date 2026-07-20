from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)

app=application

## Route for home page 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        print("Route Entered")

        if request.method == 'GET':
            return render_template('home.html')

        print("POST Request")

        try:
            reading_score = float(request.form.get('reading_score', ''))
            writing_score = float(request.form.get('writing_score', ''))
        except (TypeError, ValueError):
            return render_template(
                'home.html',
                error='Please enter numeric reading and writing scores.'
            ), 400

        if not 0 <= reading_score <= 100 or not 0 <= writing_score <= 100:
            return render_template(
                'home.html',
                error='Reading and writing scores must be between 0 and 100.'
            ), 400

        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=reading_score,
            writing_score=writing_score
        )

        print("CustomData Created")

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        print(results)

        return render_template('home.html', results=results[0])

    except Exception as e:
        print("ERROR OCCURRED:", e)
        raise

if __name__=="__main__":
    app.run(host="0.0.0.0") 

          
# For now use   http://127.0.0.1:5001/predictdata
        
      
