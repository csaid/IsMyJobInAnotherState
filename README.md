IsMyJobInAnotherState
=====================

I used this for my website: www.ismyjobinanotherstate.com.

* job\_reader.py gathers unemployment data from the Bureau of Labor Statistics and job posting data from Indeed.com. 
* results.json contains the number of job postings for each job subcategory and state, as of February 2014.
* scores.json contains the number of job postings for each job subcategory and state divided by the unemployment count for that state, again as of February 2014.


If you are happy with data from Februrary 2014, just use results.json and scores.json. If you want newer data and want to run job\_reader.py, you will first need to [get a publisher ID from Indeed.com](https://ads.indeed.com/jobroll/xmlfeed) to access to their XML Feed. Then, edit this line in job_reader.py...
```
client = IndeedClient(publisher=EnterYourOwnPublisherIDHere)
```
... so that your publisher ID is used instead.

Job categories and subcategories [come from Indeed.com](http://www.indeed.com/find-jobs.jsp). I don't know how they decided on these categories.




