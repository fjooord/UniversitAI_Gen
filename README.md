# UniversitAI_Gen

# Using GPT to simulate answering questions for UniversitAI

# Problem

- UniversitAI is attempting to build a system where students could get a custom tailored teaching experience led by an AI teacher
- To start this, they are trying to collect responses from people that give insights as to what people would want from a perfect professor
    - “**How would your perfect professor provide constructive feedback on your assignments and projects?”**
- Anyone with experience building a SaaS and trying to get feedback knows, that even getting people to answer questions such as this can be a hassle
- Along with this, we may not know the demographics or qualifications of people providing answers, and thus have to verify data
    - People input random characters or answers that don’t mean anything
    - Someone that is one race or age may have a different perspective and it would be good to know these factors for developing a system that could best teach a specific individual
    - Knowing someones level of education would be highly useful as it would give some insight into how well they know the topic
        - IE someone with PhD will have had more professors and thus more experience to know what good professors vs bad professors do
- These question and answer pairs are needed to get this project moving

# Proposed Solution

- Simulate the question answer using synthetic personas to create a bootstrap dataset that can be used to start building the rest of the system

# Experiment Design

## Building the personas

- Personas are built using random draws for each characteristic is order to try to create a group the matches the stratification of real world distributions and census information.
- Note:  For current testing, the system only considers US universities and population breakdowns.  This reduces complexity of accounting for different languages and population breakdown of various world universities

### Distributing Universities

- Using GPT-4 with web search enabled, a list of the top 44 universities in US was compiled
    - University List
        
        ```
        "Massachusetts Institute of Technology (MIT)",
            "Stanford University",
            "Harvard University",
            "California Institute of Technology (Caltech)",
            "University of Chicago",
            "University of Pennsylvania",
            "Princeton University",
            "Yale University",
            "Cornell University",
            "Columbia University",
            "Johns Hopkins University",
            "University of Michigan-Ann Arbor",
            "University of California Berkeley (UCB)",
            "Northwestern University",
            "New York University (NYU)",
            "University of California, Los Angeles (UCLA)",
            "Duke University",
            "Carnegie Mellon University",
            "University of California, San Diego (UCSD)",
            "Brown University",
            "University of Texas at Austin",
            "University of Washington",
            "University of Wisconsin-Madison",
            "University of Illinois at Urbana-Champaign",
            "Georgia Institute of Technology (Georgia Tech)",
            "Pennsylvania State University",
            "Rice University",
            "University of California, Davis (UCD)",
            "University of North Carolina, Chapel Hill",
            "Boston University",
            "Michigan State University",
            "Texas A&M University",
            "University of Maryland, College Park",
            "Case Western Reserve University",
            "University of Pittsburgh",
            "University of Minnesota, Twin Cities",
            "University of Florida",
            "Vanderbilt University",
            "Dartmouth College",
            "Arizona State University",
            "University of California, Irvine (UCI)",
            "University of Notre Dame",
            "Yeshiva University",
            "University of Massachusetts, Amherst"
        ```
        
- Note: When distributing currently, each university has an equal chance of being selected, which is not truly accurate

### Distributing Majors

- Using GPT-4 with web search enabled, a list of the top 25 majors in US was compiled
    - Major List
        
        ```
        "Business Administration",
            "Accounting",
            "Nursing",
            "Psychology",
            "Communications",
            "Marketing",
            "Education",
            "Elementary Education",
            "English",
            "Computer Science",
            "Finance",
            "Criminal Justice",
            "Biology",
            "Political Science",
            "Economics",
            "Electrical Engineering",
            "History",
            "Liberal Arts",
            "Sociology",
            "Fine Arts",
            "Commercial Art & Graphic Design",
            "General Engineering",
            "Journalism",
            "Computer and Information Systems",
            "Social Work"
        ```
        
- Note: When distributing currently, each major has an equal chance of being selected, which is not truly accurate

### Distributing Gender

- Gender was assigned to personas using a random draw

### Distributing Ethnicity and Names

- Using data online of the ethnicity of college students in the US, each persona was randomly assigned an ethnicity
    - Distribution Source
        - https://www.equityinhighered.org/indicators/enrollment-in-undergraduate-education/race-and-ethnicity-of-u-s-undergraduates/
- Then using the specified ethnicities, a list of 100 common first and last names
- Then the logic for how a name was made is as follows
    - Gender is randomly assigned
    - Ethnicity is randomly assigned
    - Based on these gender and ethnicity, a first name is selected from a list for the gender and ethnicity, then a last name for that ethnicity is selected
- Note: Naming the personas appears to provide better results in past experiments

### Distributing Degree Level and Age

- First a degree level of Bachelor’s, Master’s, PhD is selected
- Then based on the average ages of people in those programs and age is selected
    - Bachelor’s → 18-22
    - Master’s → 22-30
    - PhD → 26-35

### Resulting Persona

- This results in personas of the following form
    
    ```json
    "Name": "Jazlyn Phillips",
            "Age": "29",
            "Ethnicity": "Black or African American",
            "Gender": "Female",
            "Degree": "Master's Degree",
            "Major": "Accounting",
            "University": "University of Washington",
            "QA": [ ]
    ```
    

## Questioning the Personas

- Every personas was asked the same 2 questions to start
    - How would your perfect professor provide constructive feedback on your assignments and projects?
    - What is your best thing a professor has done to aid in your learning during your college career?
- Then the user can specify a number of follow up questions to ask:
    - The past 2 questions are given to a GPT-4 prompt that creates a follow up question
    - The persona is asked the question
    - The result is saved and the loop continues
- The Question/Answer pairs are saved as a tuple where the first value is the question and second is the answer.  The resulting persona with QA is as follows:

```json
{
        "Name": "Jazlyn Phillips",
        "Age": "29",
        "Ethnicity": "Black or African American",
        "Gender": "Female",
        "Degree": "Master's Degree",
        "Major": "Accounting",
        "University": "University of Washington",
        "QA": [
            [
                "How would your perfect professor provide constructive feedback on your assignments and projects?",
                "In my opinion, my perfect professor would provide constructive feedback on my assignments and projects by being specific, objective, and supportive. They would clearly identify areas of improvement and provide suggestions for how to enhance my work. They would also explain the rationale behind their feedback, helping me understand the reasoning behind their suggestions. Additionally, my perfect professor would offer encouragement and highlight my strengths to motivate me to continue growing and excelling in my studies."
            ],
            [
                "What is your best thing a professor has done to aid in your learning during your college career?",
                "The best thing a professor has done to aid in my learning during my college career was providing a supportive and inclusive learning environment. This professor encouraged open discussions, valued diverse perspectives, and fostered a sense of belonging for all students. They also offered additional resources and personalized feedback to help me succeed in the course. Overall, their dedication to creating an inclusive and engaging learning experience greatly enhanced my education."
            ],
            [
                "How did this professor create an inclusive and engaging learning experience for you?",
                "During my time at the University of Washington, my professor created an inclusive and engaging learning experience by fostering a supportive and diverse classroom environment. They encouraged open dialogue and respected different perspectives, ensuring that all students felt valued and heard. The professor incorporated a variety of teaching methods, such as group discussions and case studies, to promote active learning and critical thinking. They also incorporated real-world examples and practical applications of accounting principles to make the material more relatable and interesting. Overall, the professor's approach created an inclusive space where I felt motivated to participate and learn."
            ]
        ]
    }
```

# Results

- The overall results were promising.  The answers were are valid and could be used to some level for bootstrapping a system to get started.  The answers tending to feel generic to some of the questions, which points to a need for more nuanced prompts and better developed personas

## Cons

- Efficacy is the big one.  How do we know that these answers are valid?
    - I have experimented with simulating polling to try to validate to real data the responses
- Underlying bias in a model could play a major role in the validity of the answers, we want the “truth” and not to have a model impart its own bias onto a dataset that will be used
- Properly modeling a population will be very important and if the population is misrepresented then this system could skew in an unwanted direction

## Pros

- System is very scalable and can always create new, different, and better personas
- Using different prompts, the questions can be generated to provide more nuanced and specific answers to questions
- With proper prompting, the need for sifting through answers to verify their validity will not be needed
- The speed and price of this method are unparalleled to that of acquiring real feedback
    - GPT-3.5-Turbo
        - 10 Personas, 3 Questions each → $0.01
    - GPT-4
        - 10 Personas, 3 Questions each → $0.20

# Future Work

- Developing better personas that answer in a less static way
- Experimenting with the temperature of models to see what produces optimal results
- Designing a prompt chain that creates follow up questions that are more nuanced and dig into what we may want to know for creating an AI professor
