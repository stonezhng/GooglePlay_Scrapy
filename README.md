# GooglePlay_Scrapy
Fetch all the reviews on the GooglePlay App stores based on Scrapy


You should first fill in the blanks in settings.py about the information of the database 

Then jump to the project file and run the command


`scrapy crawl google
`

The result contains the following columns:
 
 `app_name`, `app_category`, `developer`, `reviewer_name`, `reviewer_link`, `title`,
                `date`, `content`, `rank`
