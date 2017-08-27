# GooglePlay_Scrapy
Fetch all the reviews on the GooglePlay App stores based on Scrapy

## Usage

*  Requires the python tool `scrapy` to be installed first.

* You should first fill in the blanks in settings.py about the information of the database 

Then jump to the project file and run the command


`scrapy crawl google
`

The result contains the following columns:
 
 `app_name`, `app_category`, `developer`, `reviewer_name`, `reviewer_link`, `title`,
                `date`, `content`, `rank`
                
## Warning
* API may be unavailable nowadays.
* The IP address may be blocked during a long time running process.
* It can take huge amount of time to finish scrapping.

## Update
* A Java version is available, which is more flexible and easy to use.
* This Java bot refers to a program on Github which I now fail to find out, therefore it's improper to post this part without explicit reference.
