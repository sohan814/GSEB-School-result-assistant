# GSEB-School-result-assistant
A python script to get result of all the students in a school from the board website 

**How to use it**

So there are 3 things you need to get results of your school students in a matter of seconds
- **Python** installed in you PC for that you can go to [Python Download](https://www.python.org/downloads/) I recommend version 3.6 or 3.7 . Check if pip is working in cmd or watch this tutorial at [Pip installation Tutorial](https://www.youtube.com/watch?v=AVCcFyYynQY)

Then you need to enter the following commands at -
``` 
pip install pandas
pip install beautifulsoup4
pip install html-table-extractor
pip install selenium

```

- Chrome Driver for your PC that you can get at [Chrome Driver Link](https://chromedriver.chromium.org/downloads)

- Now you are done for the setup part , so just keep ready the list of seat numbers that you may need

[![](http://img.youtube.com/vi/I5SSQqDlX4M/0.jpg)](http://www.youtube.com/watch?v=I5SSQqDlX4M "Example of the Tool")

Then you need to change the seat numbers in the ```__main__()``` function
```
numbers=[roll1,roll2...] 
subjects = ['Gujarati FL', 'Social Science', 'Science', 'Mathematics', 'English SL', 'Sanskrit SL']
```

Hope it may help all the schools that waste time visiting these sites and manually entering results for each student and also there may be some mistakes while entering data. This does 250ms for one result and hence near to 1200 students result may be there in the time equivalent to time taken by teacher in entering one data.

Respect and Gratitude to all the teachers and hence this is something to give back for the years you have generoulsy tought us !!

