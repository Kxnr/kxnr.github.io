#lang pollen
@(require racket/string)
@(require racket/list)

@(define-meta template "templates/resume.html")

@(define (classes . classes) `(class ,(string-join (flatten classes) " ")))

@(define (filter-empty . items)
  (filter 
    (lambda (item) 
            (and 
              (non-empty-string? item) 
              (not (andmap char-whitespace? (string->list item)))
            )
    ) 
    (flatten items)
  )
)

@(define (box #:class-lst [class-lst '()] . content) 
  `(div (,(classes "p-4" "w-full" "border-b-2" "border-black" class-lst)) ,@content)
)

@(define (header-items #:class-lst [class-lst '()] . items) 
  `(div (,(classes class-lst)) 
    ,(string-join items (format "\t~a\t" separator))
  )
)

@(define (centered #:class-lst [class-lst '()] . content)
  `(div (,(classes "mx-auto" "my-auto" "text-center" class-lst)) ,@content)
)

@(define (header #:class-lst [class-lst '()] name . content)
  (box #:class-lst class-lst
    (apply centered
      `(div (,(classes "text-2xl" "font-thin")) ,(string-upcase name))
      content
    )
  )
)

@(define (section #:class-lst [class-lst '()] name . content)
  (apply box #:class-lst class-lst
    `(div ((class "text-lg font-thin mb-2")) ,(string-upcase name))
    content
  )
)

@(define (job-header #:class-lst [class-lst '()] what where when)
  `(div (,(classes "text-base" class-lst))
    (div (strong ,what) ,(format "\t~a\t" separator) ,where) 
    (div (em ,when))
  )
)

@(define (job-description #:class-lst [class-lst '()] . description)
  `(div (,(classes class-lst)) ,@description)
)

@(define (bullet-list #:class-lst [class-lst '()] . items)
 `(ul ((class "list-disc list-inside")) 
  ,@(map (lambda (item) 
          `(li ,item))
         (filter-empty  items)
    )
  )
)

@(define (skills-list category . skills)
  ; &#9679; default bullet?
  ; need to create a block element to prevent default decoding creating a paragraph here
  `(div (div ((class "inline")) (strong ,category) ,(format "\t~a\t" separator))
     (ul ((class "inline list-none")) 
      ,@(map (lambda (item) 
              `(li ((class "inline after:content-['_•_'] last:after:content-none")) ,item))
             (filter-empty skills)
      )
    )
  )
)


@define[separator]{//}
@define[job-break]{@div[#:class "my-2"]{}}

@div[#:class "text-sm"]{
  @header[]{
    Connor Keane
    @; TODO: link if html
    @header-items[#:class-lst "text-lg" "Berkeley, CA" "connor.keane@kxnr.me" "github.com/kxnr"]{}
  }

  @section["Summary"]{
    Lorem Ipsum Summary
  }

  @section["Experience"]{
    @job-header["Staff Software Engineer" "Ascend Analytics" "January 2024 - Present"]{}
    @job-header["Senior Software Engineer" "Ascend Analytics" "July 2022 - January 2024"]{}
    @job-header["Software Engineer" "Ascend Analytics" "August 2021 - July 2022"]{}
    @job-description[]{Job description here}
    @job-break

    @job-header["Data and Programming Specialist""University of Pennsylvania" "2019-2021"]{}
    @job-description[]{Job description here}
    @bullet-list[]{
      First bullet
      Second bullet
      Third bullet
    }
    @job-break
    @; @job-description[]{}

    @job-header["Research Assistant" "Swarthmore College" "Spring & Summer 2018"]{}
    @; @job-description[]{}
    @job-break

    @job-header["Human Computer Interaction Intern" "NASA Ames" "Summer 2015 & 2016"]{}
    @; @job-description[]{}
  }


  @div[#:class "flex flex-row"]{
    @; FIXME: little wonky to disable border this way

    @section["Education" #:class-lst '("border-none" "basis-1/3")]{
      @strong[]{Swarthmore College}
      BA in Cognitive Science
      Minor in Physics
    }

    @section["Skills" #:class-lst "border-none"]{
      @skills-list["Programming"]{
        Python
        Rust
        Racket
      }
    }
  }
}
