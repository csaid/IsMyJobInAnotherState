IsMyJobInAnotherState
=====================

I used this for my website: www.ismyjobinanotherstate.com.

job_reader.py gathers unemployment data from the Bureau of Labor Statistics and job posting data from Indeed.com. 

For this to work, you will first need to get a publisher ID from Indeed.com to access to their XML Feed (https://ads.indeed.com/jobroll/xmlfeed). Then, edit this line in job_reader.py...

client = IndeedClient(publisher=EnterYourOwnPublisherIDHere)

... so that your publisher ID is used instead.

Job categories and subcategories come from Indeed.com (http://www.indeed.com/find-jobs.jsp). I don't know how they decided on these categories.

results.json contains the number of job posting for each job subcategory and state.
scores.json contains the number of job postings for each job subcategory and state divided by the unemployment count for that state.



