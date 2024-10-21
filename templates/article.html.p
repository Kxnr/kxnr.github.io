@(require racket/file racket/system)

@(struct header-link (name target))
@(define header-entries
   (list
    (header-link "About Me" "about_me.html")
    (header-link "Resume" "resume.html")
    (header-link "Github" "https://github.com/Kxnr")
    )
   )

@; TODO: this will send the entirety of a file as a preview, which is less than desirable
@(define preview-file
   (path-replace-extension
       (let-values ([(path name flag) (split-path (symbol->string here))]) name)
       #".preview")
   )
@(define (save-preview) (display-to-file (->html (div doc)) preview-file #:exists 'replace))

@save-preview[]{}

<!DOCTYPE html>
@(->html
  (html
   (head
    (meta #:charset "UTF-8")
    (page-title "Connor Keane")
    (link #:rel "stylesheet" #:type "text/css" #:media "all" #:href "/css/output.css")
    )
   (body #:class "bg-charcoal text-bone border-bone z-0 h-dvh text-md"
         @; Links
         (div #:class "sticky top-0 w-full bg-copper shadow-sm content-center items-center border-b z-10 text-l"
              (div #:class "relative flex px-4 py-2 items-center"
                   (div #:class "flex-none" (a #:href "/" "KXNR"))
                   (apply ol #:class "flex space-x-8 ml-auto"
                          (map
                           (lambda (link-struct) (li (a #:href (header-link-target link-struct) (header-link-name link-struct))))
                           header-entries
                           )
                          )
                   )
              )
         (div #:class "container mx-auto shadow-2xl p-4 m-4"
              (outlined
               doc
               )
              )
         )
   )
  )
