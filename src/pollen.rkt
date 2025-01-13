#lang racket/base

(require txexpr
         pollen/decode)
(require pollen/core)
(provide (all-defined-out))
(require racket/string)
(require racket/list)

(module setup racket/base
  (provide (all-defined-out))
  (require racket/path)
  (define command-char #\@)
  ; TODO: ignore template files
  (define omitted-path? (lambda (path?) (member (path-get-extension path?) (list #".css")))))

(struct header-link (name target))
(define header-entries
  (list (header-link "About Me" "about_me.html")
        (header-link "Resume" "resume.html")
        (header-link "Github" "https://github.com/Kxnr")))

(define (knockout content . classes)
  `(div #:class
        (string-join `("border-inherit bg-background bg-clip-text text-transparent" ,@classes))
        content))

(define (classes . classes)
  `(class ,(string-join (flatten classes) " ")))

(define (filter-empty . items)
  (filter (lambda (item)
            (and (non-empty-string? item) (not (andmap char-whitespace? (string->list item)))))
          (flatten items)))

(define (title . content)
  ; TODO: use box function(s)
  `(div (,(classes "text-4xl" "w-full" "border-inherit" "text-bone" "mb-2")) ,@content))

(define (box . content)
  `(div (,(classes "w-full" "border-inherit")) ,@content))

(define (shadow-box . content)
  `(div (,(classes "border-inherit" "md:shadow-2xl" "md:p-2")) ,@content))

(define (section-box . content)
  `(div (,(classes "p-4" "border-t" "border-inherit" "first:border-none")) ,(apply box content)))

(define (outlined . content)
  (shadow-box `(div (,(classes "bg-background-fade" "m-2"))
                    ; TODO: inherit parent background rather than setting here
                    (div (,(classes "bg-charcoal"
                                    "bg-clip-padding"
                                    "p-2"
                                    "border-4"
                                    "border-transparent"
                                    "border-solid"))
                         ,@content))))

(define (vertical-list . items)
  `(ul ((class "list-disc list-inside")) ,@(map (lambda (item) `(li ,item)) (filter-empty items))))

(define (horizontal-list #:separator [separator "//"] . items)
  ; &#9679; default bullet?
  ; need to create a block element to prevent default decoding creating a paragraph here
  `(div (ul ((class "inline list-none"))
            ,@(map (lambda (item)
                     `(li ((class (format "inline after:content-['_%s_'] last:after:content-none"
                                          separator)))
                          ,item))
                   (filter-empty items)))))

(define (header)
  (box
   `(div
     #:class
     "no-print border-inherit flex items-center justify-center text-center bg-background p-4 border-b min-h-aspect"
     (div #:class "bg-charcoal border-inherit border-2 shadow-sm max-w-4xl grow p-4"
          ,(knockout "Connor Keane" "text-6xl")
          ; TODO: use horizontal-list
          ,(knockout "Developer | tinkerer | science enthusiast" "text-xl")))))

(define (links)
  `(div
    #:class
    "no-print border-inherit sticky top-0 w-full bg-copper shadow-sm content-center items-center border-b z-10 text-l"
    ,(box `(div #:class "relative flex px-4 py-2 items-center"
                (div #:class "flex-none" (a #:href "/" "KXNR"))
                ,(map (lambda (list-items) `(ol ,@list-items))
                      #:class "flex space-x-8 ml-auto"
                      (map (lambda (link-struct)
                             `(li (a #:href ,(header-link-target link-struct)
                                     ,(header-link-name link-struct))))
                           header-entries))))))

(define (image . content)
  '())

(define (page-title . content)
  `(title ,@content))

(define (break)
  '(br))

(define (root . elements)
  ; FIXME: splice root into body
  (txexpr 'root
          '((class "border-inherit"))
          (decode-elements elements #:txexpr-elements-proc decode-paragraphs)))

; TODO: article function to define title, published date, modified date, and summary/subtitle

; TODO: save preview to metas, have a function here that takes title, image, etc. as args
; TODO: having a single make-preview function that introspects an s-expr takes away ownership
; TODO: from the individual formats
(define (make-preview path)
  ; title is required, image and summary are optional
  (let* ([doc '()]
         [metas '()]
         [title (select-from-doc 'title doc)]
         [image (select-from-doc 'image doc)]
         [summary (select-from-metas 'summary metas)])
    '()))
