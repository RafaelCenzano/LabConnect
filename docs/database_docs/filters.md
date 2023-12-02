Filter Implementation and Expected Format

JSON File (ie. Python Dictionary):
This is data aggregated from the HTML

{
    departments: [Computer Science, Biology, Physics], 
    Opportunities.recommends_majors
    
    
    salary: 15,
    Opportunities.has_salary_comp
    
    
    upfrontPay: 20,
    Opportunities.has_upfront_pay_comp
    
    
    credit_comp: 4,
    Opportunities.has_credit_comp
    
    
    name: "",
    Opportunities.name,
    
    
    years:["Freshman", "Sophomore", "Junior" ]
    Opportunities.recommends_class_years
    
    
    courses: ["data_structures", "focs", "computer_organization"],
    Opportunities.recommends_courses
    
    
    application_due: "#DATETIME FORMAT#",
    Opportunities.application_due
    
    
    semesters: ["Spring", "Summer", "Winter"],
    Opportunities.active_semesters
    
}

Implementation of Filters in HTML:
Upfront Pay, Salary, credits - slider or number with buttons to go up and down

years, departments - checkboxes

courses - dropdown

application due date: Choose by month and year (two dropdowns??)

name: search box