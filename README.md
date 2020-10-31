# Python-Project
CS 3080 final project repository

**Summary:**
Create a program that scrapes posts from social media platforms, categorizes posts based on the content via Natural Language Processing, and also determines an aggregate "reaction score" based on the comments of the post. Data is retrieved from the social media platforms using "data scraping" APIs and is stored in a backend database. The categorization and scoring is conducted via various data analytics methodologies, and presented to a web server which will provide the user access to the program output.
	
**Tasks and Objectives:**
- Data scraping 
	- Retrieving data from web using supplied APIs
	- Configuring tool to retrieve relevant content
- Natural Language Processing
	- Analyze data to categorize and classify postings based on content type (news, sports, etc.)
- Classifying how individual words affect score, i.e. which words are positive/negative 
- Backend database services
	- How to efficiently store, query, and access database records
- Client/server network principles
	- Ensure web server has connection to local database to retrieve data
	- Establish and maintain connection to social media platforms
- Web server data presentation
	- Present ideas in a clear, user-friendly method
	- Add visuals and graphs to inform user of results
	

**Basic Server Operation:**
- Navigate to '{repo}\production'
- In CLI, execute 'python couchdb-server.py'
- In a web browser, navigate to 'localhost:3000' to get to the landing page.

**Twitter API Access Keys:**
- To ensure the security of the repo, the access keys and tokens are stored on the local machine.
- To edit: nav to 'C:\CS3080\twitter_api' and create or open 'keys.txt' with your favorite text editor.
- The program only reads in the first four lines, and the order is critical.
- Format
	Line 1: API Key
	Line 2: API Secret Key				
	Line 3: Access Token
	Line 4: Access Token Secret
- No whitespace may occur at the beginning of the line.
- The program assumes there is a trailing '\n' character, and thus removes it. If editing on a non-Windows system, ensure the string is read in full.




