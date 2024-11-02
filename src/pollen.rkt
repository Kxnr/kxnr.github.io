#lang racket/base

(require txexpr pollen/decode)
(provide (all-defined-out))

(module setup racket/base
  (provide (all-defined-out))
  (require racket/path)
  (define command-char #\@)
  (define omitted-path? (lambda (path?) (member (path-get-extension path?) (list #".css"))))
)


(define (outlined . content)
	(txexpr* 'div '((class "bg-background-fade m-4"))
	  (txexpr 'div '((class "bg-charcoal bg-clip-padding p-4 border-4 border-transparent border-solid")) content)
	)
)

(define (title . content)
	(txexpr 'div '((class "text-4xl border-b w-full border-bone text-bone mb-2")) content)
)

(define (page-title . content)
  (txexpr 'title empty content)
)

(define (break)
  (txexpr 'br empty empty)
)

(define (root . elements)
   (txexpr 'root empty (decode-elements elements
     #:txexpr-elements-proc decode-paragraphs)))

; (define (preview path)
;   ; TODO: parse html into txepr
;   ; TODO: get title and body
;   ; TODO: read more button

;   ()
;   )
