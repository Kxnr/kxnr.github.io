@(require racket/file racket/system)

@(struct header-link (name target))
@(define header-entries
   (list
    (header-link "About Me" "about_me.html")
    (header-link "Resume" "resume.html")
    (header-link "Github" "https://github.com/Kxnr")
    )
   )

<!DOCTYPE html>
@(->html
  (html
   (head
    (meta #:charset "UTF-8")
    (page-title "Connor Keane")
    (meta #:name "robots" #:content "noai, noimageai")
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
   (footer (p "© 2024 Connor Keane.") (p "I don't use AI in my work, so don't use my work for your AI. Fair?"))
   )
  )
