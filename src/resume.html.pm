#lang pollen
@(require racket/string)
@(require racket/list)

@(define-meta template "templates/resume.html")


@(define (header-items #:class-lst [class-lst '()] . items) 
  `(div (,(classes class-lst)) 
    ,(string-join items (format "\t~a\t" separator))
  )
)

@(define (centered . content)
  `(div (,(classes "mx-auto" "my-auto" "text-center")) ,@content)
)

@(define (header name . content)
  (box
    (apply centered
      `(div (,(classes "text-2xl" "font-thin")) ,(string-upcase name))
      content
    )
  )
)

@(define (section name . content)
  (apply box
    `(div (,(classes "text-lg" "font-thin" "mb-2")) ,(string-upcase name))
    content
  )
)

@(define (job-header what where when)
  `(div (,(classes "flex text-base"))
    (div (strong ,what) ,(format "\t~a\t" separator) ,where) (div ((class "ml-auto")) (em ,when))
  )
)

@(define (job-description . description)
  `(div ,@description)
)

@(define (bullet-list . items)
  `(div ((class "pl-4"))
   (ul ((class "list-disc list-outside")) 
    ,@(map (lambda (item) 
            `(li ,item))
           (filter-empty  items)
      )
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
@; TODO: replace with box
@define[job-break]{@div[#:class "my-2"]{}}

  @div[#:class "text-sm border-inherit"]{
  @section-box{
    @header[]{
      Connor Keane
      @; TODO: link if html
      @header-items["Berkeley, CA" "github.com/kxnr"]{}
    }
  }

  @section-box{
    @section["Summary"]{
      Curious Software Engineer with broad data engineering and system design experience in both large codebases and greenfield development. Adept at creating software that uplifts team productivity and streamlines existing workflows.
    }
  }

  @section-box{
    @section["Experience"]{
      @job-header["Staff Software Engineer" "Ascend Analytics" "February 2024 - Present"]{}
      @job-header["Senior Software Engineer" "Ascend Analytics" "July 2022 - January 2024"]{}
      @job-header["Software Engineer" "Ascend Analytics" "August 2021 - June 2022"]{}
      @job-description[]{Responsible for development of data infrastructure and integration with electrical grid systems for a real-time optimization platform}
      @bullet-list{
        Used Apache Datafusion to increase data throughput by 400% at half the original cost

        Created structures for integration with client and grid systems, enabling a team of three developers to write and maintain over a dozen integrations

        Led development of two greenfield projects and supported launch to clients

        Presented 4 internal talks and run a monthly continuing education forum

        Built developer tooling for deployment to and management of Azure cloud resources enabling entirely automated release process
      }
      @job-break

      @job-header["Data and Programming Specialist""University of Pennsylvania" "June 2019 - March 2021"]{}
      @job-description[]{Solo maintainer of neuroscience research applications and data analysis software}
      @bullet-list[]{
        Maintained analysis pipeline for human behavior and electrophysiology data, including voice recognition and both supervised and unsupervised classification of neural time series data

        Extended internally developed libraries to support a novel type of memory experiment and deployed this experiment to online, scalp EEG, and intracranial EEG participants

        Re-implemented or adapted existing experiments to run online during the COVID-19 pandemic
      }
      @job-break

      @job-header["Research Assistant" "Swarthmore College" "January 2018 - August 2018"]{}
      @job-description[]{Studied mouth opening dynamics of freshwater round worms}
      @job-break

      @job-header["Human Computer Interaction Intern" "NASA Ames" "Summer 2015 & 2016"]{}
      @job-description[]{Prototyped user interfaces for distributed sensor data using IoT and Augmented Reality technologies under the guidance of graduate students}
    }
  }

  @section-box{
    @; FIXME: move formatting into tag
    @div[#:class "flex flex-row"]{
      @; FIXME: doesn't show border in not wrapped

      @div[#:class "basis-1/3"]{
        @section["Education"]{
          @strong[]{Swarthmore College}
          BA in Cognitive Science
          Minor in Physics
        }
      }

      @div[#:class "basis-2/3 flex-shrink"]{
        @section["Skills"]{
          @skills-list["Languages"]{
            Python
            Rust
            SQL
            HTML/CSS
            C#
            Javascript
            Racket
          }
          @skills-list["Libraries"]{
            Flask
            Datafusion
            Starlette
            Pandas 
            Tailwind
            NumPy
          } 
          @skills-list["Tools"]{
            Azure
            Docker
            git
            Terraform
            Linux
          }
        }
      }
    }
  }
}
