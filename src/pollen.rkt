#lang racket/base

(require txexpr
         pollen/decode)
(require pollen/core)
(provide (all-defined-out))

(module setup racket/base
  (provide (all-defined-out))
  (require racket/path)
  (define command-char #\@)
  ; TODO: ignore template files
  (define omitted-path? (lambda (path?) (member (path-get-extension path?) (list #".css")))))

(define (outlined . content)
  `(div 
    ((class "md:shadow-2xl md:p-2"))
    (div 
     ((class "bg-background-fade m-2"))
     (div
      ((class "bg-charcoal bg-clip-padding p-2 border-4 border-transparent border-solid"))
        ,@content)
       )
    )
)

(define (title . content)
  (txexpr 'div '((class "text-4xl border-b w-full border-bone text-bone mb-2")) content))

(define (image . content)
  '())

(define (page-title . content)
  (txexpr 'title empty content))

(define (break)
  (txexpr 'br empty empty))

(define (root . elements)
  (txexpr 'root empty (decode-elements elements #:txexpr-elements-proc decode-paragraphs)))

; TODO: article function to define title, published date, modified date, and preview

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
