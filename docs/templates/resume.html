@(require racket/string)

@(struct header-link (name target))
@(define header-entries
  (list (header-link "About Me" "about_me.html")
        (header-link "Resume" "resume.html")
        (header-link "Github" "https://github.com/Kxnr")))

@(define (knockout content . classes)
  (div #:class (string-join `("bg-background bg-clip-text text-transparent" ,@classes)) content))

<!DOCTYPE
html>
@(->html
 (html
  (head (meta #:charset "UTF-8")
        (page-title "Connor Keane Resume")
        (link #:rel "stylesheet"
              #:type "text/css"
              #:media "all"
              #:href "css/resume.css")
        (meta #:name "viewport" #:content "width=device-width, initial-scale=1"))
  (body
   #:class "w-full screen:bg-charcoal screen:text-bone print:bg-white print:text-black "
   @; Banner
   (div
    #:class
    "no-print flex items-center justify-center text-center bg-background p-4 border-b min-h-aspect"
    (div #:class "bg-charcoal border-2 shadow-sm max-w-4xl grow p-4"
         (knockout "Connor Keane" "text-6xl")
         (knockout "Developer | tinkerer | science enthusiast" "text-xl")))
   @; Links
   (div
    #:class
    "no-print sticky top-0 w-full bg-copper shadow-sm content-center items-center border-b z-10 text-l"
    (div #:class "relative flex px-4 py-2 items-center"
         (div #:class "flex-none" (a #:href "/" "KXNR"))
         (apply ol
                #:class "flex space-x-8 ml-auto"
                (map (lambda (link-struct)
                       (li (a #:href (header-link-target link-struct)
                              (header-link-name link-struct))))
                     header-entries))))
   @; Resume Content
   (div #:class "container mx-auto" doc))))
