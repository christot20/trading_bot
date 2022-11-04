# R.A.M. Trading
## Purpose
This project works to find what stock trading strategy is the most successful when given the choice between
a machine, people on a subreddit, and company/stock metrics. An LSTM Neural Network was used to predict stocks for the
machine learning method, [WSB](https://www.reddit.com/r/wallstreetbets/) was used to make the decisions for the reddit
method, and value metrics such as price-to-earnings and price-to-book were used for the algorithmic value investing
strategy. You can check out my live dashboard and the performance/holdings of each account [here](https://ramtrading.streamlitapp.com/).

### To use for youself, make sure you have:
1. A MYSQL Database named purchase_history
2. Initialized tables under the aliases:
    - algo_method
    - net_method
    - reddit_method
        - Can be done by calling 'db_initializer' and changing the table name at the bottom
3. Run 'pip install -e .'
4. Run 'pip install -r requirements.txt'
5. Have filled in all the necessary information from 'config_template.py'

### To run bot:
1. Call bot.py
2. Choose which method to run
    - R = Reddit Method (WSB)
    - A = Algorithmic Method (Value Trading Strategy)
    - M = Machine Learning Method (LSTM time-series predictions)
3. Allow loading time to finish and purchases to be made
4. Check MYSQL tables to make sure purchases went through

### To run streamlit app:
1. Run 'sheet_writer.py' by 4 a.m. (When account monitoring begins)
2. Run 'streamlit run app.py'
    - Local and remote links will be given once run to check the app


