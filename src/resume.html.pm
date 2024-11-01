#lang pollen
@; TODO: make the template a "page size" template
@(define-meta template "templates/resume.html")

@(define (header-items items) '@div[(string-join items "|")]{})
@(define hrule '(hr))

@(define (section-header content) @div[content @hrule ]{})
@; @(define (job-header what when))
@; @(define (job-subtitle where))
@; @(define (job-description content)
@; @(define (skills-list category skills))

@centered[]{
  @h1[]{Connor Keane}
  Boulder, CO | connor.keane@"@"kxnr.me | github.com/Kxnr
}

@section-header[]{Education}
@job-header[]{Swarthmore College 2019}

@section-header[]{Experience}
@job-header["Staff Software Engineer" "January 2024 - Present"]{}
@job-header["Senior Software Engineer" "July 2022 - January 2024"]{}
@job-header["Software Engineer" "August 2021 - July 2022"]{}
@job-subtitle[]{Ascend Analytics}
@job-description[]{}

@job-header["Data and Programming Specialist" "2019-2021"]{}
@job-subtitle[]{University of Pennsylvania}
@job-description[]{}

@job-header["Research Assistant" "Spring & Summer 2018"]
@job-subtitle[]{Swarthmore College}
@job-description[]{}

@job-header["Human Computer Interaction Intern" "Summer 2015 & 2016"]{}
@job-subtitle[]{NASA Ames}
@job-description[]{}

@section-header[]{Skills}
@skills-list[]{}


